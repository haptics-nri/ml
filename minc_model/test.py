#!/usr/bin/env python2

from __future__ import division
from __future__ import with_statement
from __future__ import print_function

import sys
sys.path.insert(0, '/home/alexburka/caffe/python')

import caffe
import numpy
import glob
import os
import os.path
import sys
from contextlib import contextmanager

# from http://stackoverflow.com/a/24176022/1114328
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
        
def resize_image(image, new_shape):
    old_shape = image.shape[0:2]
    if abs(old_shape[0] - new_shape[0]) > abs(old_shape[1] - new_shape[1]):
        intermediate_shape = (round(old_shape[0] * new_shape[1] / old_shape[1]), new_shape[1])
        intermediate = caffe.io.resize_image(image, intermediate_shape)
        start = int(round((intermediate_shape[0] - new_shape[0])/2))
        return intermediate[start:(start+224),:,:]
    else:
        intermediate_shape = (new_shape[0], round(old_shape[1] * new_shape[0] / old_shape[0]))
        intermediate = caffe.io.resize_image(image, intermediate_shape)
        start = int(round((intermediate_shape[1] - new_shape[1])/2))
        return intermediate[:,start:(start+224),:]

def classify_images(arch):
    with cd(os.path.dirname(__file__)):
        if not os.path.exists('images'):
            print('Place images to be classified in images/brick/*.jpg, images/carpet/*.jpg, ...')
            sys.exit(1)
        categories=[x.strip() for x in open('categories.txt').readlines()]

        #arch='googlenet' # googlenet, vgg16 or alexnet
        net=caffe.Classifier('deploy-{}.prototxt'.format(arch),'minc-{}.caffemodel'.format(arch),channel_swap=(2,1,0),mean=numpy.array([104,117,124]))

        answers = []
        confusion = {}
        for i,x in enumerate(categories):
            confusion[i]=[0]*len(categories)
            for j,y in enumerate(sorted(glob.glob('images/{}/*'.format(x)))):
                z=net.predict([resize_image(caffe.io.load_image(y), net.image_dims)*255.0])[0]
                k=z.argmax()
                print(arch,y,categories[k],z[k],k==i)
                confusion[i][k] += 1
                answers.append((y, z, k))
        return answers, confusion, categories, net
    
def transfer_learning(arch):
    with cd(os.path.dirname(__file__)):
        if not os.path.exists('images'):
            print('Place images to be classified in images/brick/*.jpg, images/carpet/*.jpg, ...')
            sys.exit(1)
        categories=[x.strip() for x in open('categories.txt').readlines()]

        #arch='googlenet' # googlenet, vgg16 or alexnet
        net=caffe.Classifier('deploy-{}.prototxt'.format(arch),'minc-{}.caffemodel'.format(arch),channel_swap=(2,1,0),mean=numpy.array([104,117,124]))
