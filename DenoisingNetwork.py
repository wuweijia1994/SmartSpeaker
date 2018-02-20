import torch.nn as nn


class DenoiseNN(nn.Module):
    def __init__(self):
        super(DenoiseNN, self).__init__()

        #Input layer
        self.conv1 = nn.Conv2d(1, 1, 3, padding=1)
        self.relu_0 = nn.ReLU()

        self.linear_1 = nn.Linear(161*11, 1600)
        self.relu_1 = nn.ReLU()

        self.linear_2 = nn.Linear(1600, 1600)
        self.relu_2 = nn.ReLU()

        self.linear_3 = nn.Linear(1600, 1600)
        self.relu_3 = nn.ReLU()

        self.linear_4 = nn.Linear(1600, 1600)
        self.relu_4 = nn.ReLU()

        #output layer
        self.linear_5 = nn.Linear(1600, 161)
        self.relu_5 = nn.ReLU()


    def forward(self, x):
        result = x.view(-1, 161 * 11)
        # result = self.relu_0(self.conv1(result))
        result = self.relu_1(self.linear_1(result))

        result = self.relu_2(self.linear_2(result))

        result = self.relu_3(self.linear_3(result))

        result = self.relu_4(self.linear_4(result))

        result = self.relu_5(self.linear_5(result))

        return result