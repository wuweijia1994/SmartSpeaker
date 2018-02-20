import DenoisingNetwork as denn
import AudioDataset as ad
import numpy as np
import os
import matplotlib.pyplot as plt

from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch

import torch.optim as optim
import torch.optim.lr_scheduler as lr

import ProcessDataset.AudioSynthesis
from torchvision import transforms

audio_transform = transforms.Compose([
    transforms.Normalize((0.5), (0.5))
    # transforms.ToTensor()
])

# root_dir_wuweijia = './20171114_morning/'
input_data_path = "./ProcessDataset/small_mix_npy/"
input_files = ProcessDataset.AudioSynthesis.get_subfolders(input_data_path)
label_data_path = "./ProcessDataset/small_wav_npy/"
# label_files = AudioSynthesis.get_subfolders(label_data_path)

net = denn.DenoiseNN()

# criterion = F.cross_entropy()
optimizer = optim.Adam(net.parameters(), lr=0.03)
my_loss_data = []
standard_loss_data = []

scheduler = lr.StepLR(optimizer, step_size=1, gamma=0.1)

for file in input_files:
    input_file_path = os.path.join(input_data_path, file)
    label_file_path = os.path.join(label_data_path, file)

# input_dir = "./ProcessDataset/small_mix_npy/a0001.npy"
# label_dir = "./ProcessDataset/small_wav_npy/a0001.npy"

    transformed_dataset = ad.audio_dataset(input_dir=input_file_path, label_dir=label_file_path)


    train_data_loader = torch.utils.data.DataLoader(dataset=transformed_dataset, batch_size=10,
                            shuffle=True, num_workers=4)

    # for epoch in range(50):  # loop over the dataset multiple times

    loss_recorder = []
    running_loss = 0.0
    for i, data in enumerate(train_data_loader, 0):
        # get the inputs
        inputs, labels = data['input'], data['label']

        # wrap them in Variable
        inputs, labels = Variable(inputs), Variable(labels)

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = F.mse_loss(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.data[0]
        loss_recorder.append(loss.data[0])

        if i % 10 == 9:    # print every 120 mini-batches
            print('[%d, %5d] loss: %.30f' %
                  (0 + 1, i + 1, loss.data[0]))
            running_loss = 0.0
            _, predicted = torch.max(outputs.data, 1)
            pre = predicted.numpy()
            # s =
            # if(epoch > 35):
                # show_picture(np.concatenate((pre[0], labels.data.numpy()[0]), 1))
            # show_picture(labels.data.numpy()[0])
            # show_picture(img_as_ubyte(inputs.data.numpy()[0]/255.0))
            # show_picture(pre[1])
            # show_picture(pre[2])
            # show_picture(pre[3])

            # output_debug = labels.data.numpy()
            # predicted = show_output_data(outputs, 3, 0.3)
            # labels = show_output_data(labels, 3, 0.3)
            # plt.plot(range(len(loss_recorder)), loss_recorder)
            # plt.show();

            # a = (a - a.min()) / (a.max() - a.min())
            # viewer = ImageViewer(img_as_ubyte(a))
            # viewer.show()

            # b = labels.view([-1, 54, 54])
            # b = b.data.numpy()[0, :, :]
            # b = (b - b.min())/(b.max() - b.min())
            #
            # c = a - b
            # c = c**2
            # c = c.sum()
            # view_b = ImageViewer(img_as_ubyte(b))
            # view_b.show()
            # my_loss_data.append(c/2916.0)
            # standard_loss_data.append(loss.data[0])

print(i)
print('Finished Training')

def cross_entropy2d(input, target, weight=None, size_average=True):
    # input: (n, c, h, w), target: (n, h, w)
    n, c, h, w = input.size()
    # log_p: (n, c, h, w)
    log_p = F.log_softmax(input)
    # log_p: (n*h*w, c)
    log_p = log_p.transpose(1, 2).transpose(2, 3).contiguous().view(-1, c)
    # a = target.view(n, h, w, -1)
    log_p = log_p[target.view(n, h, w, 1).repeat(1, 1, 1, c) >= 0]
    log_p = log_p.view(-1, c)
    # target: (n*h*w,)
    mask = target >= 0
    target = target[mask]
    loss = F.nll_loss(log_p, target, weight=weight, size_average=False)
    if size_average:
        loss /= mask.data.sum()
    return loss

def show_output_data(outputs, mean, dev):
    outputs_data = outputs.view([-1, 54, 54])
    # demo = predicted.data.numpy();
    outputs_data = outputs_data.data.numpy()[0, :, :]
    outputs_data[outputs_data > (mean + dev)] = 0
    outputs_data[outputs_data < (mean - dev)] = 0
    return outputs_data