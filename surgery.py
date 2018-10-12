import caffe

import numpy as np
from PIL import Image
import scipy.io

import random

class NYUDSegDataLayer(caffe.Layer): # Continued from class 'caffe.Layer' 
    """
    Load (input image, label image) pairs from NYUDv2
    one-at-a-time while reshaping the net to preserve dimensions.
    The labels follow the 40 class task defined by
        S. Gupta, R. Girshick, p. Arbelaez, and J. Malik. Learning rich features
        from RGB-D images for object detection and segmentation. ECCV 2014.
    with 0 as the void label and 1-40 the classes.
    Use this to feed data to a fully convolutional network.
    """

    def setup(self, bottom, top):
        """
        Setup data layer according to parameters:
        - nyud_dir: path to NYUDv2 dir
        - split: train / val / test
        - tops: list of tops to output from {color, depth, hha, label}
        - randomize: load in random order (default: True)
        - seed: seed for randomization (default: None / current time)
        for NYUDv2 semantic segmentation.
        example: params = dict(nyud_dir="/path/to/NYUDVOC2011", split="val",
                               tops=['color', 'hha', 'label'])
        """
        # config
        params = eval(self.param_str)               # returns output inside bracket
        self.nyud_dir = params['nyud_dir']          # dir of NYUD dataset 
        self.split = params['split']                # dir of validation/train/test dataset
        self.tops = params['tops']                  #
        self.random = params.get('randomize', True) # load images in random order
        self.seed = params.get('seed', None)

        # store top data for reshape + forward
        self.data = {}                              # dir of data

        # means
        self.mean_bgr = np.array((116.190, 97.203, 92.318), dtype=np.float32)
        self.mean_hha = np.array((132.431, 94.076, 118.477), dtype=np.float32)
        self.mean_logd = np.array((7.844,), dtype=np.float32)

        # tops: check configuration
        if len(top) != len(self.tops):
            raise Exception("Need to define {} tops for all outputs.")
        # data layers have no bottoms
        if len(bottom) != 0:
            raise Exception("Do not define a bottom.")

        # load indices for images and labels
        split_f  = '{}/{}.txt'.format(self.nyud_dir, self.split) """ e.g. 'self.nyud_dir /                                                                      self.split.txt'       """
        self.indices = open(split_f, 'r').read().splitlines()    """indices means number of data 
                                                                open([file],[read_only])
                                                                .read() all bytes are read 
                                                                .splitlines() split line as  one element                        """
        self.idx = 0

        # make eval deterministic
        if 'train' not in self.split:          # if train folder not exist 
            self.random = False

        # randomization: seed and pick
        if self.random:
            random.seed(self.seed)
            self.idx = random.randint(0, len(self.indices)-1)# random.randit() is to generate a                                                    # random number between 0 and len()

    def reshape(self, bottom, top):
        # load data for tops and  reshape tops to fit (1 is the batch dim)
        for i, t in enumerate(self.tops):     # enumerate() used to output sequence of index obj.s
            self.data[t] = self.load(t, self.indices[self.idx]) # input data in sequence of t
            top[i].reshape(1, *self.data[t].shape)

    def forward(self, bottom, top):
        # assign output
        for i, t in enumerate(self.tops):
            top[i].data[...] = self.data[t]

        # pick next input
        if self.random:
            self.idx = random.randint(0, len(self.indices)-1)
        else:
            self.idx += 1
            if self.idx == len(self.indices):
                self.idx = 0

    def backward(self, top, propagate_down, bottom):
        pass

    def load(self, top, idx): # input data type selection
        if top == 'color':
            return self.load_image(idx)
        elif top == 'label':
            return self.load_label(idx)
        elif top == 'depth':
            return self.load_depth(idx)
        elif top == 'hha':
            return self.load_hha(idx)
        else:
            raise Exception("Unknown output type: {}".format(top))

    def load_image(self, idx):                  # Activated when 'color' input
        """
        Load input image and preprocess for Caffe:
        - cast to float
        - switch channels RGB -> BGR
        - subtract mean
        - transpose to channel x height x width order
        """
        im = Image.open('{}/data/images/img_{}.png'.format(self.nyud_dir, idx))
        in_ = np.array(im, dtype=np.float32)    # set image as array
        in_ = in_[:,:,::-1]                     # read until last element downcount
        in_ -= self.mean_bgr
        in_ = in_.transpose((2,0,1))            # 转置矩阵，（0,1,2）变为（2，0,1）行变换
        return in_

    def load_label(self, idx):
        """
        Load label image as 1 x height x width integer array of label indices.
        Shift labels so that classes are 0-39 and void is 255 (to ignore it).
        The leading singleton dimension is required by the loss.
        """
        label = scipy.io.loadmat('{}/segmentation/img_{}.mat'.format(self.nyud_dir, idx))['segmentation'].astype(np.uint8)       # switch .mat to np type
        label -= 1                              # rotate labels
        label = label[np.newaxis, ...]          # add new axis
        return label

    def load_depth(self, idx):
        """
        Load pre-processed depth for NYUDv2 segmentaltion set.
        """
        im = Image.open('{}/data/depth/img_{}.png'.format(self.nyud_dir, idx))
        d = np.array(im, dtype=np.float32)
        d = np.log(d)
        d -= self.mean_logd
        d = d[np.newaxis, ...]
        return d

    def load_hha(self, idx):
        """
        Load HHA features from Gupta et al. ECCV14.
        See https://github.com/s-gupta/rcnn-depth/blob/master/rcnn/saveHHA.m
        """
        im = Image.open('{}/data/hha/img_{}.png'.format(self.nyud_dir, idx))
        hha = np.array(im, dtype=np.float32)
        hha -= self.mean_hha
        hha = hha.transpose((2,0,1))
return hha
