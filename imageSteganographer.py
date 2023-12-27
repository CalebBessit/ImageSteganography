#Decription : Implementation of image steganography algorithm developed by Caleb Bessit
#Author     : Caleb Bessit
#Date       : 27 December 2023


import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def main():
    # Open the TIFF image and convert to RGB
    index = 4
    loadedImage = Image.open('TestImages/4.1.0{}.tiff'.format(index))
    rgbImage    = loadedImage.convert("RGB")

    #Get image layers and convert to numpy arrays
    r, g, b = rgbImage.split()
    r, g, b = map(np.array, (r,g,b))
    width, height = rgbImage.size


if __name__=="__main__":
    main()