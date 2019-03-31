import gpytorch
from gpytorch.models import AbstractVariationalGP
from gpytorch.variational import CholeskyVariationalDistribution
from gpytorch.variational import VariationalStrategy
from gpytorch.mlls.variational_elbo import VariationalELBO
import torch
import gc   
import numpy as np
from torch import Tensor
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
plt.style.use('seaborn-darkgrid')
import gc
gc.collect()

train = pd.read_csv("weekly_SWEurope_train.csv")
train = train.dropna()
test = pd.read_csv("weekly_SWEurope_test.csv")
test = test.dropna()


print("Number train:{}".format(train.shape))
print("Number test:{}".format(test.shape))

train_x = Tensor(train.iloc[:, :9].values)
train_y = Tensor(train.iloc[:, -1].values)

test_x = Tensor(test.iloc[:, :9].values)
test_y = Tensor(test.iloc[:, -1].values)

if torch.cuda.is_available():
    train_x = train_x.cuda()
    train_y = train_y.cuda()
    test_x = test_x.cuda()

data_dim = train_x.size(-1)

class LargeFeatureExtractor(torch.nn.Sequential):
    def __init__(self):
        super(LargeFeatureExtractor, self).__init__()
        self.add_module('linear1', torch.nn.Linear(data_dim, 100))
        self.add_module('relu1', torch.nn.ReLU())
        self.add_module('linear2', torch.nn.Linear(100, 2))

class DKL(gpytorch.models.AbstractVariationalGP):
    """Spatiotemporal Gaussian Process model class

    input:

        mean_function: mean function - from gpytorch classes or torch.nn
        kernel: temporal kernel - from gpytorch classes
        train_x: training features: Nxp dimensions
        train_y: training labels: Nx1 dimensions
        likellihood: Specify the likelihood function - from gpytorch classes
    """
    def __init__(self, train_x, likelihood, feature_extractor):
        variational_distribution = CholeskyVariationalDistribution(train_x.size(0))
        variational_strategy = VariationalStrategy(self, train_x, variational_distribution)
        super(DKL, self).__init__(variational_strategy)
        self.mean_module = gpytorch.means.ConstantMean()
        self.covar_module = gpytorch.kernels.ScaleKernel(
                            gpytorch.kernels.MaternKernel())
        self.feature_extractor = feature_extractor
    
    def forward(self, x):
        """forward pass of GP model

        """
        # We're first putting our data through a deep net (feature extractor)
        # We're also scaling the features so that they're nice values
        projected_x = self.feature_extractor(x)
        projected_x = projected_x - projected_x.min(0)[0]
        projected_x = 2 * (projected_x / projected_x.max(0)[0]) - 1
        mean = self.mean_module(projected_x)
        covar = self.covar_module(projected_x)  
        latent_pred = gpytorch.distributions.MultivariateNormal(mean, covar)
        
        return latent_pred


def train_model(train_x, train_y, model, likelihood, epochs = 50):
    """training procedure

    input:

        model: model object
        likelihood: likelihood object
        epochs: number of training epochs

    output:

        model: trained posterior model

    """
    # Find optimal model hyperparameters
    if torch.cuda.is_available():
        gc.collect()
        torch.cuda.empty_cache()
    
    model.train()
    likelihood.train()

    # Use the adam optimizer
    optimizer = torch.optim.Adam([
        {'params': model.parameters()},  # Includes GaussianLikelihood parameters
    ], lr=0.1)

    # "Loss" for GPs - the marginal log likelihood
    mll = VariationalELBO(likelihood, model, train_y.numel())

    for i in range(epochs):
        # Zero gradients from previous iteration
        optimizer.zero_grad()
        # Output from model
        output = model(train_x)
        # Calc loss and backprop gradients
        loss = -mll(output, train_y)
        loss.backward()
        print("Iter {}/{} - Loss: {}".format(
            i + 1, epochs, loss.item()
        ))

        # if you are using lengthscale kernels
        #print("Iter {}/{} - Loss: {} lengthscale_s {}, lengthscale_t {}".format(
        #    i + 1, epochs, loss.item(),
        #    model.covar_module_s.lengthscale.item(),
        #    model.covar_module_t.lengthscale.item()
        #))
        
        optimizer.step()

    return model


def predict(test_x, model, likelihood):
    """compute posterior predictive mean and variance

    input:

        test_x: covariates of test in matrix form
        model: GP model object
        likelihood: likelihood object

    output:

        posterior_pred: return posterior prediction objected

    """

    # Get into evaluation (predictive posterior) mode
    model.eval()
    likelihood.eval()

    # Make predictions by feeding model through likelihood
    # gpytorch.settings.fast_pred_var() for LOVE prediction
    with torch.no_grad():
        posterior_pred = likelihood(model(test_x))

    return posterior_pred
  
def main():
    # initialize likelihood and model and feature extractor
    likelihood = gpytorch.likelihoods.BernoulliLikelihood()
    feature_extractor = LargeFeatureExtractor()
    feature_extractor = feature_extractor.cuda()    
    gp_model = DKL(train_x, likelihood, feature_extractor)
    likelihood = likelihood.cuda()
    gp_model = gp_model.cuda()

    print("Start Training \n")
    gp_model = train_model(train_x, train_y, gp_model, likelihood, epochs=100)
    # posterior prediction
    posterior_pred = predict(test_x, gp_model, likelihood)

    #plt.figure(0)
    #plt.scatter([i for i in range(1,223)], test_y.cpu(), marker = ".")
    #plt.scatter([i for i in range(1,223)], posterior_pred.mean.cpu().numpy())
    #plt.show()
    # Go into eval mode
    likelihood.eval()

    with torch.no_grad():
        pred_labels = posterior_pred.mean.ge(0.5).float()
        print(confusion_matrix(test_y.cpu().numpy(), posterior_pred.mean.ge(0.5).cpu().numpy()))
    

