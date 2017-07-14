import sys
sys.path.insert(0, '/home/alexburka/caffe/python')
import caffe
import numpy as np

# setup Caffe
caffe.set_device(0)
caffe.set_mode_gpu()

# load network
categories=[x.strip() for x in open('minc_model/categories.txt').readlines()]
arch = 'alexnet'
minc_net = caffe.Classifier('minc_model/deploy-{}.finetune.prototxt'.format(arch),
                            'minc_model/minc-{}.caffemodel'.format(arch),
                            channel_swap=(2,1,0),
                            mean=np.array([104,117,124]),
                            phase=caffe.TRAIN)

outputs = minc_net.forward()
probs = outputs['prob'].mean(0)
top = (-probs).argsort()[:5]
print [(100*probs[i], categories[i]) for i in top]
for p in ['w', 'h', 'r', 'ss', 'so', 'sb']:
    out = outputs['prob-%s' % p][0]
    print p, out.argmax()+1

