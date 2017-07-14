import sys
sys.path.insert(0, '/home/alexburka/caffe/python')
import os.path
import caffe
import numpy as np
import json

# references:
#  - https://stackoverflow.com/questions/41344168/what-is-a-python-layer-in-caffe/41481539#41481539

class ImageDataWithRatingsLayer(caffe.Layer):
  def setup(self, bottom, top):
    print 'SETUP'
    assert len(bottom) == 0, 'no inputs expected (got %d)' % len(bottom)
    assert len(top) == 2, '2 outputs expected (got %d)' % len(top)

    class Object:
      pass

    params = json.loads(self.param_str)
    assert 'file' in params, 'file parameter missing'
    assert 'prefix' in params, 'prefix parameter missing'
    assert 'oversample' in params, 'oversample parameter missing'
    assert 'transform' in params, 'transform parameter missing'
    self.file = params['file']
    self.prefix = params['prefix']
    self.oversample = params['oversample']
    self.transform = Object
    self.transform.crop_size = params['transform']['crop_size']
    self.transform.mean_value = params['transform']['mean_value']

    assert os.path.isfile(os.path.join(self.prefix, self.file)), '%s does not exist' % os.path.join(self.prefix, self.file)
    assert isinstance(self.oversample, bool), 'oversample should be boolean'
    assert isinstance(self.transform.crop_size, int) and self.transform.crop_size > 0, 'transform.crop_size should be positive integer'
    assert isinstance(self.transform.mean_value, list) and len(self.transform.mean_value) == 3 and all(map(lambda v: isinstance(v, int) and 0 <= v <= 255, self.transform.mean_value)), 'transform.mean_value should be 3-element list of integers 0-255'

    top[0].reshape(10, 3, self.transform.crop_size, self.transform.crop_size)
    top[1].reshape(10)

    with open(os.path.join(self.prefix, self.file), 'r') as f:
      self.lines = f.readlines()
    self.i = 24

  def reshape(self, bottom, top):
    print 'RESHAPE'

  def forward(self, bottom, top):
    print 'FORWARD'

    line = self.lines[self.i]
    self.i = self.i + 1
    if self.i == len(self.lines):
        self.i = 0

    filename, prop = line.split()
    print filename
    img = caffe.io.load_image(os.path.join(self.prefix, filename))
    img = resize_image(img, (self.transform.crop_size, self.transform.crop_size))
    img = img[:, :, (2, 1, 0)]
    img = img*255 - self.transform.mean_value
    if self.oversample:
      # Generate center, corner, and mirrored crops.
      img = caffe.io.oversample([img], [self.transform.crop_size]*2)
    else:
      # Take center crop.
      center = np.array(self.transform.crop_size) / 2.0
      crop = np.tile(center, (1, 2))[0] + np.concatenate([
        -self.transform.crop_size / 2.0,
        self.transform.crop_size / 2.0
        ])
      crop = crop.astype(int)
      img = img[:, crop[0]:crop[2], crop[1]:crop[3], :]

    for i in range(10):
      top[0].data[i, ...] = img[i, ...].transpose((2, 0, 1))
      top[1].data[i] = float(prop)

  def backward(self, top, propagate_down, bottom):
    print 'BACKWARD'

def resize_image(image, new_shape):
    old_shape = image.shape[0:2]
    if abs(old_shape[0] - new_shape[0]) > abs(old_shape[1] - new_shape[1]):
        intermediate_shape = (round(old_shape[0] * new_shape[1] / old_shape[1]), new_shape[1])
        intermediate = caffe.io.resize_image(image, intermediate_shape) # TODO try different resample modes, try crop-only mode
        start = int(round((intermediate_shape[0] - new_shape[0])/2))
        return intermediate[start:(start+new_shape[0]),:,:]
    else:
        intermediate_shape = (new_shape[0], round(old_shape[1] * new_shape[0] / old_shape[0]))
        intermediate = caffe.io.resize_image(image, intermediate_shape)
        start = int(round((intermediate_shape[1] - new_shape[1])/2))
        return intermediate[:,start:(start+new_shape[1]),:]

