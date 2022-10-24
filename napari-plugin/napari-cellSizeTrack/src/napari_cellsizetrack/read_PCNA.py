## PART 1 - extracting the cells

# Read the TIF image and the mask and separate the four channels
from calendar import c
import os
from symbol import single_input
import numpy as np
import tifffile
from tifffile import imread
from matplotlib import pyplot as plt
import cellpose
from cellpose import models

# Read the mask image

#Load all images
images = []
for i in range(180):
    path_to_img = os.getcwd() + '\Example_imgs\OneDrive_1_24-10-2022\\' + str(i) + '.tif'
    images.append(imread(path_to_img))
print(len(images))

#create a mask with cellpose of all of the images

path_to_mask = os.getcwd() + '\Example_imgs\Image20_cellpose_mask.tif'
cell_mask = imread(path_to_mask)

path_to_cell_img = os.getcwd() + '\Example_imgs\Image20.tiff'
cell_img = imread(path_to_cell_img)

singled_out_cells = []
for num in np.unique(cell_mask.data)[1:]:
    single_mask = np.where(cell_mask == num, cell_img, 0)
    singled_out_cells.append(single_mask)

#Now need to read the all of the images and get all of their singled_out_cells data

## PART 2 - centroids
# This will work on matching the cells on a sequence of images

def centeroidnp(arr):
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return sum_x/length, sum_y/length

centeroids = []
for singled_out_cell in singled_out_cells:
    coordinates_of_val = np.argwhere(singled_out_cell != 0)
    centeroids.append(centeroidnp(coordinates_of_val))


#Next need to compute centeroids between cells and compare them