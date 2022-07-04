# data loader
from __future__ import print_function, division
import torch
from skimage import transform
import numpy as np
from PIL import Image, ExifTags


# ==========================dataset load==========================
class RescaleT(object):

    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        self.output_size = output_size

    def __call__(self, sample):
        image, label = sample.get('image'), sample.get('label')

        img = transform.resize(image, (self.output_size, self.output_size), mode='constant')
        lbl = transform.resize(label, (self.output_size, self.output_size), mode='constant', order=0,
                               preserve_range=True)

        return img, lbl


class ToTensorLab(object):
    """Convert ndarrays in sample to Tensors."""

    def __init__(self, flag=0):
        self.flag = flag

    def __call__(self, sample):
        image, label = sample.get('image'), sample.get('label')
        tmp_lbl = np.zeros(label.shape)

        if np.max(label) < 1e-6:
            label = label
        else:
            label = label / np.max(label)

        # change the color space
        # with rgb color
        tmp_img = np.zeros((image.shape[0], image.shape[1], 3))
        image = image / np.max(image)
        if image.shape[2] == 1:
            tmp_img[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
            tmp_img[:, :, 1] = (image[:, :, 0] - 0.485) / 0.229
            tmp_img[:, :, 2] = (image[:, :, 0] - 0.485) / 0.229
        else:
            tmp_img[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
            tmp_img[:, :, 1] = (image[:, :, 1] - 0.456) / 0.224
            tmp_img[:, :, 2] = (image[:, :, 2] - 0.406) / 0.225

        tmp_lbl[:, :, 0] = label[:, :, 0]

        tmp_img = tmp_img.transpose((2, 0, 1))
        tmp_lbl = label.transpose((2, 0, 1))

        return torch.from_numpy(tmp_img), torch.from_numpy(tmp_lbl)


class SalObjData:
    def __init__(self, img_path, transform=None):
        self.image_path = img_path
        self.transform = transform

    def get(self):
        image = get_rotate_image(self.image_path)
        label = np.zeros(image.shape[0:2])

        if 3 == len(image.shape) and 2 == len(label.shape):
            label = label[:, :, np.newaxis]
        elif 2 == len(image.shape) and 2 == len(label.shape):
            image = image[:, :, np.newaxis]
            label = label[:, :, np.newaxis]

        sample = {'image': image, 'label': label}

        if self.transform:
            sample = self.transform(sample)

        return sample.get('image'), sample.get('label'), image.shape


def get_rotate_image(image_path):
    img = Image.open(image_path)
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(img._getexif().items())
        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
    except:
        pass

    return np.array(img)
