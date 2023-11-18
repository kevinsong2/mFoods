import os
import torch
import random
import numpy as np
import pandas as pd

import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

np.random.seed(42)

# initalize pretrained cnn
vgg11 = models.vgg16(preTrained=True).eval()


def preproocess_image(image_path):
    # TODO
    image = Image.open(image_path)
    return image


def predict(image_path, model):
    image = preprocess_image(image_path)
    outputs = model(image)



