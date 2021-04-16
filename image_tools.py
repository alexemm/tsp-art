import numpy as np
from PIL import Image


def load_image(file: str):
    im = Image.open(file).convert('L')
    return im


def image_to_array(img):
    return np.asarray(img)


def array_to_image(arr):
    return Image.fromarray(np.uint8(arr))


def array_to_tsp_nodes(arr):
    return np.argwhere(arr == 0)
