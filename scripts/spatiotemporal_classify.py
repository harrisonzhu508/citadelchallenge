import gpytorch
from gpytorch.models import AbstractVariationalGP
from gpytorch.variational import CholeskyVariationalDistribution
from gpytorch.variational import VariationalStrategy
from gpytorch.mlls.variational_elbo import VariationalELBO
from gpytorch.variational import GridInterpolationVariationalStrategy
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


class KISS_Spatiotemporal_GP(AbstractVariationalGP):
    """KISS_Spatiotemporal_GP Gaussian Process model class

    input:

        mean_function: mean function - from gpytorch classes or torch.nn
        train_x: training features: Nxp dimensions
        train_y: training labels: Nx1 dimensions
        likelihood: Specify the likelihood function - from gpytorch classes
    """
    def __init__(self, grid_size=128, grid_bounds=[(0, 1), ()]):
        variational_distribution = CholeskyVariationalDistribution(grid_size)
        variational_strategy = GridInterpolationVariationalStrategy(self, 
                              grid_size, grid_bounds, variational_distribution)
        super(KISS_Spatiotemporal_GP, self).__init__(variational_strategy)

        self.mean_module = gpytorch.means.ZeroMean()
        #self.covar_season = gpytorch.kernels.PeriodicKernel(
                          #period_length_prior=gpytorch.priors.NormalPrior(
                          #loc=Tensor([1]), scale=Tensor([0.1])
                          #  ))
        #self.covar_season = gpytorch.kernels.PeriodicKernel()
        #self.covar_week = gpytorch.kernels.RBFKernel()
        #self.covar_spatial = gpytorch.kernels.MaternKernel()
        #self.covar_remote = gpytorch.kernels.MaternKernel()
        self.covar = gpytorch.kernels.MaternKernel()

        #self.mean_module = torch.nn.Linear(train_x.shape[1], 1)
    
    def forward(self, x):
        """forward pass of GP model

        """
        #year = x.narrow(1,0,1)
        #week = x.narrow(1,1,1)
        #spatial = x.narrow(1,2,2)
        #remote = x.narrow(1,4,1)
        # prevent period to reset
        mean = self.mean_module(x).view(-1)

        #compute covariances
        #covar_season = self.covar_season(year)
        #covar_week = self.covar_week(week)
        #covar_spatial = self.covar_spatial(spatial)
        #covar_remote = self.covar_remote(remote)
        #covar_social = self.covar_social(social)
        
        #covariance = (covar_season + covar_week)*(covar_remote + covar_spatial)\
        covariance = self.covar(x)

        return gpytorch.distributions.MultivariateNormal(mean, covariance)

class Spatiotemporal_GP(AbstractVariationalGP):
    """Spatiotemporal Gaussian Process model class

    input:

        mean_function: mean function - from gpytorch classes or torch.nn
        train_x: training features: Nxp dimensions
        train_y: training labels: Nx1 dimensions
        likelihood: Specify the likelihood function - from gpytorch classes
    """
    def __init__(self, train_x, likelihood):
        variational_distribution = CholeskyVariationalDistribution(train_x.size(0))
        variational_strategy = VariationalStrategy(self, train_x, variational_distribution)
        super(Spatiotemporal_GP, self).__init__(variational_strategy)

        self.mean_module = gpytorch.means.ZeroMean()
        self.covar_season = gpytorch.kernels.PeriodicKernel()
        self.covar_week = gpytorch.kernels.RBFKernel()
        self.covar_spatial = gpytorch.kernels.MaternKernel()
        self.covar_remote = gpytorch.kernels.MaternKernel()
        #self.covar = gpytorch.kernels.MaternKernel()

        #self.mean_module = torch.nn.Linear(train_x.shape[1], 1)
    
    def forward(self, x):
        """forward pass of GP model

        """
        year = x.narrow(1,0,1)
        week = x.narrow(1,1,1)
        spatial = x.narrow(1,2,2)
        remote = x.narrow(1,4,1)
        # prevent period to reset
        mean = self.mean_module(x).view(-1)

        #compute covariances
        covar_season = self.covar_season(year)
        covar_week = self.covar_week(week)
        covar_spatial = self.covar_spatial(spatial)
        covar_remote = self.covar_remote(remote)
        
        covariance = (covar_season + covar_week)*(covar_remote + covar_spatial)
        #covariance = self.covar(x)

        return gpytorch.distributions.MultivariateNormal(mean, covariance)

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
    """main method

    """
    
    train = pd.read_csv("weekly_SWEurope_train.csv")
    train = train.dropna()
    test = pd.read_csv("weekly_SWEurope_test.csv")
    test = test.dropna()


    print("Number train:{}".format(train.shape))
    print("Number test:{}".format(test.shape))

    train_x = Tensor(train.iloc[:, :-2].values)
    train_y = Tensor(train.iloc[:, -1].values)

    test_x = Tensor(test.iloc[:, :-2].values)
    test_y = Tensor(test.iloc[:, -1].values)

    if torch.cuda.is_available():
        train_x = train_x.cuda()
        train_y = train_y.cuda()
        test_x = test_x.cuda()
    
    # initialize likelihood and model
    # initialize likelihood and model and feature extractor
    # initialize likelihood and model and feature extractor
    likelihood = gpytorch.likelihoods.BernoulliLikelihood()
    gp_model = Spatiotemporal_GP(train_x, likelihood)
    likelihood = likelihood.cuda()
    gp_model = gp_model.cuda()

    print("Start Training \n")
    gp_model = train_model(train_x, train_y, gp_model, likelihood, epochs=500)
    # posterior prediction
    posterior_pred = predict(test_x, gp_model, likelihood)

    with torch.no_grad():
        pred_labels = posterior_pred.mean.ge(0.5).float()
        print(confusion_matrix(test_y.cpu().numpy(), posterior_pred.mean.ge(0.5).cpu().numpy()))
    
if __name__ == "__main__":
    main()   