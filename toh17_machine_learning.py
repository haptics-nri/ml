from __future__ import division
import minc_model.copy_minc_labeled_surface_images
import minc_model.test
import numpy as np

def original_minc_our_images():
    """Try the original MINC networks on our images"""

    minc_model.copy_minc_labeled_surface_images.go()
    answers, confusion, categories, net = minc_model.test.classify_images('googlenet')
    accuracy = np.sum(np.diag(np.array(confusion.values())))/np.sum(np.array(confusion.values()))

    return accuracy, (answers, confusion, categories, net)



if __name__ == '__main__':
    orig_minc_acc, orig_minc_stuff = original_minc_our_images()

