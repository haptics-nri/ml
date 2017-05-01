#!/usr/bin/env python2

from __future__ import division
from __future__ import with_statement
from __future__ import print_function

import sys
sys.path.insert(0, '/home/haptics/proton/yang_icra2016/caffe-rc4/python')

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
            if x != 'ceramic':
                continue
            confusion[i]=[0]*len(categories)
            for j,y in enumerate(sorted(glob.glob('images/{}/*'.format(x)))):
                z=net.predict([caffe.io.load_image(y)*255.0])[0]
                k=z.argmax()
                print(arch,y,categories[k],z[k],k==i)
                confusion[i][k] += 1
                answers.append((y, z, k))
        return answers, confusion, categories, net

