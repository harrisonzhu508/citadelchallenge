"""
Module for Gaussian process regression

"""
import gpytorch
import torch
import gc        
from torch import Tensor
import pandas as pd
from matplotlib import pyplot as plt
plt.style.use('seaborn-darkgrid')

class Simple_GP(gpytorch.models.ExactGP):
    """Spatiotemporal Gaussian Process model class

    input:

        mean_function: mean function - from gpytorch classes or torch.nn
        kernel: temporal kernel - from gpytorch classes
        train_x: training features: Nxp dimensions
        train_y: training labels: Nx1 dimensions
        likellihood: Specify the likelihood function - from gpytorch classes
    """
    def __init__(self, train_x, train_y, likelihood):
        super(Simple_GP, self).__init__(train_x, train_y, likelihood)
        #self.mean_module = gpytorch.means.ConstantMean()
        self.covar_module = gpytorch.kernels.MaternKernel()
        self.mean_module = torch.nn.Linear(train_x.shape[1], 1)
    
    def forward(self, x):
        """forward pass of GP model

        """
        mean = self.mean_module(x).view(-1)
        covar = self.covar_module(x)  
        
        return gpytorch.distributions.MultivariateNormal(mean, covar)

class Spatiotemporal_GP(gpytorch.models.ExactGP):
    """Spatiotemporal Gaussian Process model class

    input:

        mean_function: mean function - from gpytorch classes or torch.nn
        train_x: training features: Nxp dimensions
        train_y: training labels: Nx1 dimensions
        likelihood: Specify the likelihood function - from gpytorch classes
    """
    def __init__(self, train_x, train_y, likelihood, mean_function, temporal_kernel, spatial_kernel):
        super(Spatiotemporal_GP, self).__init__(train_x, train_y, likelihood)
        #self.mean_module = gpytorch.means.ConstantMean()

        self.covar_season = gpytorch.kernels.PeriodicKernel()
        self.covar_season.period_length(1) # year seasonality indicating 1

        self.covar_month = gpytorch.kernels.MaternKernel()
        self.covar_spatial = gpytorch.kernels.MaternKernel()
        self.covar_remote = gpytorch.kernels.MaternKernel()
        self.covar_social = gpytorch.kernels.MaternKernel()

        self.mean_module = torch.nn.Linear(train_x.shape[1], 1)
    
    def forward(self, x):
        """forward pass of GP model

        """
        year = x.narrow(1,0,1)
        month = x.narrow(1,1,1)
        spatial = x.narrow(1,2,2)
        remote = x.narrow(1,4,4)
        social = x.narrow(1,5,1)
        # prevent period to reset
        mean = self.mean_module(x).view(-1)

        #compute covariances
        self.covar_season.period_length(1) # year seasonality indicating 1
        covar_season = self.covar_season(year)
        covar_month = self.covar_month(month)
        covar_spatial = self.covar_spatial(spatial)
        covar_remote = self.covar_remote(remote)
        covar_social = self.covar_social(social)
        
        covariance = (covar_season + covar_month) * (covar_spatial + covar_remote)\
                    + covar_social + covar_month 

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
    mll = gpytorch.mlls.ExactMarginalLogLikelihood(likelihood, model)

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
    
    train = pd.read_csv("../../../data/processed/modelling_data/influenza_train.csv")
    train = train.dropna()
    test = pd.read_csv("../../../data/processed/modelling_data/influenza_test.csv")
    test = test.dropna()
    
    print("Number train:{}".format(train.shape[0]))
    print("Number test:{}".format(test.shape[0]))

    train_x = Tensor(train.iloc[:, :-1].values)
    train_y = Tensor(train.iloc[:, -1].values)

    test_x = Tensor(test.iloc[:, :-1].values)
    test_y = Tensor(test.iloc[:, -1].values)
    
    if torch.cuda.is_available():
        train_x = train_x.cuda()
        train_y = train_y.cuda()
        test_x = test_x.cuda()
    
    # initialize likelihood and model
    likelihood = gpytorch.likelihoods.GaussianLikelihood()
    gp_model = Simple_GP(train_x, train_y, likelihood)
    
    if torch.cuda.is_available():
        likelihood = likelihood.cuda()
        gp_model = gp_model.cuda()
    
    print("Start Training \n")
    gp_model = train_model(train_x, train_y, gp_model, likelihood, epochs=250)
    # posterior prediction
    posterior_pred = predict(test_x, gp_model, likelihood)
    
    if torch.cuda.is_available():
        posterior_mean = posterior_pred.mean.cpu()
        print("Test RSME:{}".format(torch.norm(test_y - posterior_mean)))

    else:
        posterior_mean = posterior_pred.mean
        print("Test RSME:{}".format((torch.norm(test_y - posterior_mean) / posterior_mean.shape[0])))
    
    #plt.figure(0)
    #plt.scatter([i for i in range(1,223)], test_y.cpu(), marker = ".")
    #plt.scatter([i for i in range(1,223)], posterior_pred.mean.cpu().numpy())
    #plt.show()

    with torch.no_grad():
    # Initialize plot
        f, ax = plt.subplots(1, 1, figsize=(12, 12))
        plt.plot(test_y.cpu().numpy(), test_y.cpu().numpy())
        ax.scatter(posterior_pred.mean.cpu().numpy(), test_y.cpu().numpy(), marker=".")
        #plt.ylim((0, 2000))
        #plt.xlim((0, 2000))
        plt.show()

if __name__ == "__main__":

    main()