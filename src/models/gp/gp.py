"""
Module for Gaussian process regression

"""
import gpytorch
import torch
import gc        

class Simple_GP(gpytorch.models.ExactGP):
    """Spatiotemporal Gaussian Process model class

    input:

        mean_function: mean function - from gpytorch classes or torch.nn
        kernel: temporal kernel - from gpytorch classes
        train_x: training features: Nxp dimensions
        train_y: training labels: Nx1 dimensions
        likellihood: Specify the likelihood function - from gpytorch classes
    """
    def __init__(self, train_x, train_y, likelihood, kernel, mean_function):
        super(Spatiotemporal_GP, self).__init__(mean_function, kernel, train_x, train_y, likelihood)
        #self.mean_module = gpytorch.means.ConstantMean()
        self.covar_module = kernel
        self.mean_module = mean_function
    
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
        temporal_kernel: temporal kernel - from gpytorch classes
        spatial_kernel: spatial kernel - from gpytorch classes
        train_x: training features: Nxp dimensions
        train_y: training labels: Nx1 dimensions
        likellihood: Specify the likelihood function - from gpytorch classes
    """
    def __init__(self, train_x, train_y, likelihood, mean_function, temporal_kernel, spatial_kernel):
        super(Spatiotemporal_GP, self).__init__(mean_function, temporal_kernel, spatial_kernel, train_x, train_y, likelihood)
        #self.mean_module = gpytorch.means.ConstantMean()
        self.covar_module_t = temporal_kernel
        self.covar_module_s = spatial_kernel
        self.mean_module = mean_function
    
    def forward(self, x):
        """forward pass of GP model

        """

        s = x.narrow(1, 1, x.shape[1]-1)
        t = x.narrow(1, 0, 1)

        mean = self.mean_module(x).view(-1)
        covar_s = self.covar_module_s(s)  
        covar_t = self.covar_module_t(t)  
        covar_x = covar_s*covar_t
        
        return gpytorch.distributions.MultivariateNormal(mean, covar_x)

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
    
