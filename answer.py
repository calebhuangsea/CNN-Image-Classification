import pdb

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torchvision import transforms


'''
NN model
'''
# %%
class NN(nn.Module):
    def __init__(self, arr=[]):
        super(NN, self).__init__()
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(30 * 30 * 3, 128)
        self.fc2 = nn.Linear(128, 5)

    def forward(self, x):
        batch_size = x.shape[0]
        x = x.view(batch_size, -1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


# Simple CNN model
# %%
class SimpleCNN(nn.Module):
    def __init__(self, arr=[]):
        super(SimpleCNN, self).__init__()
        self.conv_layer = nn.Conv2d(3, 8, 3)
        self.pool = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(1568, 5)

    def forward(self, x):
       x = self.conv_layer(x)
       x = F.relu(x)
       x = self.pool(x)
       x = x.view(x.shape[0], -1)
       x = self.fc1(x)
       return x


# %%
basic_transformer = transforms.Compose([transforms.ToTensor()])

# Apply Color Normalization with 0.5, 0.5, 0.5 mean and 0.5, 0.5, 0.5 std
norm_transformer = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])


# Deep CNN model
# %%
class DeepCNN(nn.Module):
    def __init__(self, arr=[]):
        super(DeepCNN, self).__init__()

        self.conv1 = nn.Conv2d(3, arr[0], 3)
        self.conv2 = nn.Conv2d(arr[0], arr[1], 3)
        self.conv3 = nn.Conv2d(arr[1], arr[2], 3)
        if arr[-1] == 'pool':
            self.pool = nn.MaxPool2d(2)
            self.fc = nn.Linear(12*12*arr[2], 5)
        else:
            self.pool = None
            self.fc = nn.Linear(24*24*arr[2], 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))

        if self.pool:
            x = self.pool(x)

        x = x.view(x.shape[0], -1)

        x = self.fc(x)

        return x

# Random data augmentation with random horizontal flip, random crop, and random affine transformation
# %%
"""Add random data augmentation to the transformer"""
aug_transformer = transforms.Compose([
    transforms.RandomAffine(5, shear=10),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])


