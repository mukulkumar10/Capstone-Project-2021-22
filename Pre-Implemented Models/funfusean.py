# -*- coding: utf-8 -*-
"""FunFuseAn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Am4Wifbv7CnoDPJOyAWsRk4AqztQc-Nm

# This is the pytorch implementation of the paper "Structural Similarity based Anatomical and Functional Brain Imaging Fusion"
"""

#Import packages
import time
import torch.nn as nn
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.datasets as datasets
import numpy as np
from torchvision import transforms
from torch.autograd import Variable
from PIL import Image
import torchvision.transforms.functional as TF
from torchvision.models.vgg import vgg19
import torch.nn as nn
import torch.nn.functional as F
import torch
from skimage import img_as_ubyte
import torch.nn as nn
import torch.utils.data as Data
import torchvision      # dataset
import matplotlib.pyplot as plt
import scipy
import numpy as np
import argparse
import glob
import imageio
from skimage import color
import numpy
import natsort
import scipy
import pprint
from scipy.ndimage import correlate
from scipy.ndimage.filters import gaussian_gradient_magnitude
import torchvision.datasets as dset
import torch.utils.data as data
import os
import os.path
from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
from PIL import ImageTk, Image
import pylab
import cv2
import h5py
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.font_manager import FontProperties
import torch  
import torch.nn.functional as F 
import numpy as np
import math
from PIL import Image
import cv2
from google.colab.patches import cv2_imshow
import matplotlib
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/drive')

import math
!nvidia-smi

# Commented out IPython magic to ensure Python compatibility.
# %cd drive/MyDrive/Capstone Dataset

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(torch.cuda.get_device_properties(0).total_memory)

import multiprocessing

multiprocessing.cpu_count()

#define the hyperparameters
image_length = 256
image_width  = 256
mr_channels  = 1
gray_channels = 1
pet_channels = 4    
rgb_channels = 3     
batch_size   = 1
EPOCH = 50
learning_rate = 0.002
import torch.nn.functional as F
import sys
np.set_printoptions(threshold=sys.maxsize)

#load the train mri data

filenames = os.listdir('MRIGIF')
dataset = os.path.join(os.getcwd(), 'MRIGIF')
data = glob.glob(os.path.join(dataset, "*.gif"))
data = natsort.natsorted(data,reverse=False)
train_mri = np.zeros((len(data),image_width,image_length))
for i in range(len(data)):
      train_mri[i] =(imageio.imread(data[i]))
      train_mri[i,:,:] =(train_mri[i,:,:] - np.min(train_mri[i,:,:])) / (np.max(train_mri[i,:,:]) - np.min(train_mri[i,:,:]))
      #train_mri[i,:,:] = np.float32(train_mri[i,:,:])

#expand dimension to add the channel
train_mri = np.expand_dims(train_mri,axis=1)
#expand dimension to add the channel
train_mri = np.expand_dims(train_mri,axis=1)

#verify the shape matches the pytorch standard
train_mri.shape

#convert the MRI training data to pytorch tensor
train_mri_tensor = torch.from_numpy(train_mri).float()
train_mri_tensor.shape

#load the train pet data
filenames = os.listdir('CTGIF')
dataset = os.path.join(os.getcwd(), 'CTGIF')
data = glob.glob(os.path.join(dataset, "*.gif"))
data = natsort.natsorted(data,reverse=False)
train_other = np.zeros((len(data),image_width,image_length,pet_channels),dtype=float)
train_pet = np.zeros((len(data),image_width,image_length),dtype=float)
for i in range(len(data)):
    
      train_pet[i,:,:] =(imageio.imread(data[i]))
      #train_pet[i,:,:] = 0.2989 * train_other[i,:,:,0] + 0.5870 *  train_other[i,:,:,1]  + 0.1140 * train_other[i,:,:,2]
      #train_pet[i,:,:] = train_pet[i,:,:].astype(np.uint8)
      train_pet[i,:,:] =(train_pet[i,:,:] - np.min(train_pet[i,:,:])) / (np.max(train_pet[i,:,:]) - np.min(train_pet[i,:,:]))
      #train_pet[i,:,:] = np.float32(train_pet[i,:,:])

#expand the dimension to add the channel
train_pet = np.expand_dims(train_pet,axis=1)#expand the dimension to add the channel
train_pet = np.expand_dims(train_pet,axis=1)

#verify the shape matches the pytorch standard
train_pet.shape

#convert the PET training data to pytorch tensor
train_pet_tensor = torch.from_numpy(train_pet).float()
train_pet_tensor.shape

#define the network
class FunFuseAn(nn.Module):
    def  __init__(self):
        super(FunFuseAn, self).__init__()
        #####mri lf layer 1#####
        self.mri_lf = nn.Sequential( #input shape (,1,256,256)
                         nn.Conv2d(in_channels=1, out_channels=16, kernel_size=9, stride=1, padding=4),
                         nn.BatchNorm2d(16),
                         nn.LeakyReLU(0.2,inplace=True)) #output shape (,16,256,256)   
        #####mri hf layers#####
        self.mri_hf = nn.Sequential(  #input shape (,1,256,256)
                         nn.Conv2d(in_channels = 1, out_channels = 16, kernel_size  = 3, stride= 1, padding = 1),
                         nn.BatchNorm2d(16),
                         nn.LeakyReLU(0.2,inplace=True),
                         nn.Conv2d(in_channels  = 16, out_channels = 32, kernel_size = 3, stride = 1, padding = 1),
                         nn.BatchNorm2d(32),
                         nn.LeakyReLU(0.2,inplace=True),
                         nn.Conv2d(in_channels  = 32, out_channels = 64, kernel_size  = 3, stride = 1, padding = 1),
                         nn.BatchNorm2d(64),
                         nn.LeakyReLU(0.2,inplace=True)) #output shape (,64,256,256)
        #####pet lf layer 1#####
        self.pet_lf = nn.Sequential( #input shape (,1,256,256)
                         nn.Conv2d(in_channels=1, out_channels=16, kernel_size=7, stride=1, padding=3),
                         nn.BatchNorm2d(16),
                         nn.LeakyReLU(0.2,inplace=True)) #output shape (,16,256,256)   
        #####pet hf layers#####
        self.pet_hf = nn.Sequential(  #input shape (,1,256,256)
                         nn.Conv2d(in_channels = 1, out_channels = 16, kernel_size  = 5, stride= 1, padding = 2),
                         nn.BatchNorm2d(16),
                         nn.LeakyReLU(0.2,inplace=True),
                         nn.Conv2d(in_channels  = 16, out_channels = 32, kernel_size = 5, stride = 1, padding = 2),
                         nn.BatchNorm2d(32),
                         nn.LeakyReLU(0.2,inplace=True),
                         nn.Conv2d(in_channels  = 32, out_channels = 64, kernel_size  = 3, stride = 1, padding = 1),
                         nn.BatchNorm2d(64),
                         nn.LeakyReLU(0.2,inplace=True)) #output shape (,64,256,256)
        #####reconstruction layer 1#####
        self.recon1 = nn.Sequential(  #input shape (, 64, 256, 256)
                          nn.Conv2d(in_channels  = 64,  out_channels = 32, kernel_size  = 5, stride = 1, padding = 2),
                          nn.BatchNorm2d(32),
                          nn.LeakyReLU(0.2,inplace=True),
                          nn.Conv2d(in_channels  = 32, out_channels = 16, kernel_size  = 5, stride = 1, padding = 2),
                          nn.BatchNorm2d(16),
                          nn.LeakyReLU(0.2,inplace=True)) #output shape (,16, 256, 256)
        
        #####reconstruction layer 2#####
        self.recon2 = nn.Sequential(      #input shape (,16, 256, 256)
                            nn.Conv2d(in_channels  = 16, out_channels = 1, kernel_size  = 5, stride = 1, padding = 2))   #output shape (,1,256,256)

    def forward(self, x, y):
        #mri lf layer 1
        x1 = self.mri_lf(x)
        #mri hf layers
        x2 = self.mri_hf(x)
        #pet lf layer 1
        y1 = self.pet_lf(y)
        #pet hf layers
        y2 = self.pet_hf(y)
        #high frequency fusion layer
        fuse_hf = x2 + y2     
        #reconstruction layer1
        recon_hf = self.recon1(fuse_hf)
        #low frequency fusion layer
        fuse_lf = (x1 + y1 + recon_hf)/3
        #reconstruction layer2
        recon3 = self.recon2(fuse_lf)
        #tanh layer
        fused = torch.tanh(recon3)      
        return fused
        #execute the network

cnn = FunFuseAn().to(device)
cnn = cnn.float()
print(cnn)

def gaussian(window_size, sigma):
    """
    Generates a list of Tensor values drawn from a gaussian distribution with standard
    diviation = sigma and sum of all elements = 1.

    Length of list = window_size
    """    
    gauss =  torch.Tensor([math.exp(-(x - window_size//2)**2/float(2*sigma**2)) for x in range(window_size)])
    return gauss/gauss.sum()
def create_window(window_size, channel=1):

    # Generate an 1D tensor containing values sampled from a gaussian distribution
    _1d_window = gaussian(window_size=window_size, sigma=1.5).unsqueeze(1)
    
    # Converting to 2D  
    _2d_window = _1d_window.mm(_1d_window.t()).float().unsqueeze(0).unsqueeze(0)
     
    window = torch.Tensor(_2d_window.expand(channel, 1, window_size, window_size).contiguous())

    return window

def ssim(img1, img2, val_range, window_size=11, window=None, size_average=True, full=False):

    L = val_range # L is the dynamic range of the pixel values (255 for 8-bit grayscale images),

    pad = window_size // 2
    
    try:
        _, channels, height, width = img1.size()
    except:
        channels, height, width = img1.size()

    # if window is not provided, init one
    if window is None: 
        real_size = min(window_size, height, width) # window should be atleast 11x11 
        window = create_window(real_size, channel=channels).to(img1.device)
    
    # calculating the mu parameter (locally) for both images using a gaussian filter 
    # calculates the luminosity params
    mu1 = F.conv2d(img1, window, padding=pad, groups=channels)
    mu2 = F.conv2d(img2, window, padding=pad, groups=channels)
    
    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2 
    mu12 = mu1 * mu2

    # now we calculate the sigma square parameter
    # Sigma deals with the contrast component 
    sigma1_sq = F.conv2d(img1 * img1, window, padding=pad, groups=channels) - mu1_sq
    sigma2_sq = F.conv2d(img2 * img2, window, padding=pad, groups=channels) - mu2_sq
    sigma12 =  F.conv2d(img1 * img2, window, padding=pad, groups=channels) - mu12

    # Some constants for stability 
    C1 = (0.01 ) ** 2  # NOTE: Removed L from here (ref PT implementation)
    C2 = (0.03 ) ** 2 

    contrast_metric = (2.0 * sigma12 + C2) / (sigma1_sq + sigma2_sq + C2)
    contrast_metric = torch.mean(contrast_metric)

    numerator1 = 2 * mu12 + C1  
    numerator2 = 2 * sigma12 + C2
    denominator1 = mu1_sq + mu2_sq + C1 
    denominator2 = sigma1_sq + sigma2_sq + C2

    ssim_score = (numerator1 * numerator2) / (denominator1 * denominator2)

    if size_average:
        ret = ssim_score.mean() 
    else: 
        ret = ssim_score.mean(1).mean(1).mean(1)
    
    if full:
        return ret, contrast_metric
    
    return ret

import torch.nn as nn

optimizer = torch.optim.Adam(cnn.parameters(), lr=learning_rate)   # optimize all cnn parameters
l2_loss   = torch.nn.MSELoss()   #MSEloss

# Commented out IPython magic to ensure Python compatibility.
# perform the training
BS=2
counter = 0
start_time = time.time()
lamda = 0.5
gamma_ssim = 0.5
gamma_l2 = 0.5
ep_ssim_mri_loss = []
ep_ssim_pet_loss = []
ep_l2_mri_loss = []
ep_l2_pet_loss = []
ep_total_loss=[]
for epoch in range(EPOCH):
    ssim_mri_Loss = []
    ssim_pet_Loss = []
    l2_mri_Loss = []
    l2_pet_Loss = []
    total_loss=[]
    #run batch images
    batch_idxs = 64 // batch_size
    cnn.train(True)
    for idx in range(batch_idxs):
        b_x = train_mri_tensor[idx].to(device)
        b_y = train_pet_tensor[idx].to(device)
        #b_z = train_gt_tensor[idx].to(device)
        counter += 1
        output = cnn(b_x,b_y)
        # cnn output
        ssim_loss_mri = 1 - ssim(output, b_x,val_range=1)
        ssim_loss_pet = 1 - ssim(output, b_y,val_range=1)
        l2_loss_mri   = l2_loss(output,b_x)
        l2_loss_pet   = l2_loss(output,b_y)
        ssim_total = gamma_ssim*ssim_loss_mri + (1-gamma_ssim)*ssim_loss_pet
        l2_total = gamma_l2*l2_loss_mri + (1-gamma_l2)*l2_loss_pet
        loss_total = lamda*ssim_total + (1-lamda)*l2_total 
        #loss_total=l2_loss(output,b_z)
        optimizer.zero_grad()           # clear gradients for this training step
        loss_total.backward()          # backpropagation, compute gradients
        #ssim_total.backward()
        #l2_total.backward()
        optimizer.step()                # apply gradients
    
        #store all the loss values at each epoch
        ssim_mri_Loss.append(ssim_loss_mri.item())
        ssim_pet_Loss.append(ssim_loss_pet.item())
        l2_mri_Loss.append(l2_loss_mri.item())
        l2_pet_Loss.append(l2_loss_pet.item())
        total_loss.append(loss_total.item())
        # ssim_loss_mri=0
        # ssim_loss_pet=0
        # ssim_total=0
        # l2_total=0
        if counter % 100 == 0:
            print("Epoch: [%2d],step: [%2d], mri_ssim_loss: [%.8f], pet_ssim_loss: [%.8f],  total_ssim_loss: [%.8f], total_l2_loss: [%.8f], total_loss: [%.8f]" 
#             %(epoch, counter, ssim_loss_mri, ssim_loss_pet, ssim_total, l2_total, loss_total))
    cnn.train(False)
    av_ssim_mri_loss = np.average(ssim_mri_Loss)
    ep_ssim_mri_loss.append(av_ssim_mri_loss)
    
    av_ssim_pet_loss = np.average(ssim_pet_Loss)
    ep_ssim_pet_loss.append(av_ssim_pet_loss)
    
    av_l2_mri_loss = np.average(l2_mri_Loss)
    ep_l2_mri_loss.append(av_l2_mri_loss)
    
    av_l2_pet_loss = np.average(l2_pet_Loss)
    ep_l2_pet_loss.append(av_l2_pet_loss)
    av=np.average(total_loss)
    ep_total_loss.append(av)
    

    if(epoch == EPOCH -1):
      #Save a checkpoint
      torch.save(cnn.state_dict(), 'FunFuseAn50.pth')
for p in cnn.state_dict():
  print(p, "\t", cnn.state_dict()[p].size())

l1 = np.asarray(ep_ssim_mri_loss)
l2 = np.asarray(ep_ssim_pet_loss)
l3 = np.asarray(ep_l2_mri_loss)
l4 = np.asarray(ep_l2_pet_loss)
l5 = np.asarray(ep_total_loss)

h5f = h5py.File('gamma_0.5_0.5_ssim_mri.h5', 'w')
h5f.create_dataset('data', data=l1)
h5f.close()

h5f = h5py.File('gamma_0.5_0.5_ssim_pet.h5', 'w')
h5f.create_dataset('data', data=l2)
h5f.close()

h5f = h5py.File('gamma_0.5_0.5_l2_mri.h5', 'w')
h5f.create_dataset('data', data=l3)
h5f.close()

h5f = h5py.File('gamma_0.5_0.5_l2_pet.h5', 'w')
h5f.create_dataset('data', data=l4)
h5f.close()

#FunFuseAn SSIM gamma_ssim = 0.1 gamma_l2 = 0.1
fontP = FontProperties()
fontP.set_size('large')
plt.plot(l1,'b',label='$1-SSIM_{MRI}$')
plt.plot(l2,'c',label='$1-SSIM_{PET}$')
plt.plot(l5,'g',label='$Total_Loss$')
plt.xlabel('epoch',fontsize= 15)
plt.ylabel('Loss values',fontsize= 15)
plt.legend(loc=1, prop=fontP)
plt.title('FunFuseAn $\lambda = 0.08, \gamma_{ssim} = 0.5, \gamma_{l2} = 0.5$',fontsize='15')
plt.savefig('gamma_0.5_0.5_ssim.eps', format='eps', dpi=100)

#FunFuseAn L2 gamma_ssim = 0.1 gamma_l2 = 0.1
fontP = FontProperties()
fontP.set_size('large')
plt.plot(l3,'b',label='$l2_{MRI}$')
plt.plot(l4,'c',label='$l2_{PET}$')
plt.xlabel('epoch',fontsize= 15)
plt.ylabel('Loss values',fontsize= 15)
plt.legend(loc=1, prop=fontP)
plt.title('FunFuseAn $\lambda = 0.8, \gamma_{ssim} = 0.5, \gamma_{l2} = 0.5$',fontsize='15')
plt.savefig('gamma_0.5_0.5_l2.eps', format='eps', dpi=100)

from PIL import Image

model=FunFuseAn()
model.load_state_dict(torch.load('FunFuseAn50.pth'))
model.eval()
model=model.cuda()

from imageio.core.functions import imread
import numpy as np
img1=imread("c50_1.gif")
img2=imread("c50_2.gif")
img1=np.expand_dims(img1,axis=0)
img1=np.expand_dims(img1,axis=0)
img2=np.expand_dims(img2,axis=0)
img2=np.expand_dims(img2,axis=0)

img1=(img1-np.min(img1))/(np.max(img1)-np.min(img1))
img2=(img2-np.min(img1))/(np.max(img2)-np.min(img2))

tensorimg1=torch.from_numpy(img1).float().to(device)
tensorimg2=torch.from_numpy(img2).float().to(device)

fused=model(tensorimg1,tensorimg2)

nufu=fused.cpu().detach().numpy()

ffused=np.squeeze(nufu)

plt.rcParams['image.cmap'] = 'gray'
matplotlib.image.imsave('FunFuseAn50.gif', ffused)