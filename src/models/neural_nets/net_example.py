import numpy as np
import torch
from torch import nn
from torch import optim
from torch.nn import functional as F
from sklearn.preprocessing import RobustScaler
import torch.nn.init as init
from torch.autograd import Variable

# Net Structure #
# an example #
class Net(nn.Module):
    """Neural network baseline. Inherits nn.Module Class

    """
    def __init__(self,train_input_size,paras):
        """Initialisation of network parameters

        We define:
            - 2 convolutional layers
            - 2 xavier initialisation rules
            - biases.
            - 2 fcs, or fully connected layers
            - 1 dropout layer

        """
        super(Net, self).__init__()
        self.conv1 = nn.Conv1d(28, paras.c1out, kernel_size=paras.k1)
        # Initial the weights and bias
        init.xavier_uniform(self.conv1.weight, gain=np.sqrt(2))
        init.constant(self.conv1.bias, 0)
        self.conv2 = nn.Conv1d(paras.c1out, paras.c2out, kernel_size=paras.k2)
        init.xavier_uniform(self.conv2.weight, gain=np.sqrt(2))
        init.constant(self.conv2.bias, 0)
        # calculate the right length before passing linear layer
        self.le = ((train_input_size- paras.k1 + 1)//paras.p1 -paras.k2+1) *paras.c2out
        self.fc1 = nn.Linear(self.le, paras.h1)
        self.fc2 = nn.Linear(paras.h1, 2)
        self.p1 = paras.p1
        self.drop1 = nn.Dropout(p=paras.p)


    def forward(self, flag,x):
        """The forward pass or propagation

        Structure:
            conv1 -> maxpooling -> sigmoid
            -> conv2 -> fc1 -> flatten -> relu 
            -> (optional dropout) -> relu -> fc2

        """
        x = self.conv1(x)
        x = F.max_pool1d(F.sigmoid(x), kernel_size=self.p1, stride=self.p1)
        x = self.conv2(x)
        x = F.relu(self.fc1(x.view(-1, self.le)))
        if flag:
            x = self.drop1(x)
        x = self.fc2(F.relu(x))
        return x