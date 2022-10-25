## PART 1 - extracting the cells

# Read the TIF image and the mask and separate the four channels
from calendar import c
import os
from xml.etree import cElementTree
import numpy as np
import tifffile
from tifffile import imread
from matplotlib import pyplot as plt
import cellpose
from cellpose import models, core
import PIL
from PIL import Image
from scipy.spatial import distance

print('GPU activated',core.use_gpu())

## PART 0: Reading the images

#IMPORT IMAGES
def import_cell_images(path,num_images):
    images = []
    for i in range(num_images):
        if i % 50 == 0: print(str(i+1)+"/180")
        path_to_img = path + str(i) + '.tif'
        images.append(np.squeeze(imread(path_to_img)))
    return np.array(images)

images = import_cell_images(os.getcwd() + '\Example_imgs\data\images\\', 3)

#CREATE AND SAVE MASKS
def create_masks_and_save(path, images):
    model = models.Cellpose(gpu=True, model_type='nuclei')
    channels = [0,0]
    for i in range(len(images)):
        mask, flows, styles, diams = model.eval(images[i], diameter=None, flow_threshold=None, channels=channels)
        result = Image.fromarray(mask.astype(np.uint8))
        path_to_save = os.getcwd() + '\Example_imgs\data\masks\\' + str(i) + '.tif'
        result.save(path_to_save)

#create_masks_and_save(os.getcwd() + '\Example_imgs\data\masks\\', images)

#IMPORT MASKS
def import_masks(path,num_masks):
    masks = []
    for i in range(num_masks):
        path_to_mask = path + str(i) + '.tif'
        masks.append(np.squeeze(imread(path_to_mask)))
    return masks

masks = import_masks(os.getcwd() + '\Example_imgs\data\masks\\', 3)


# GET AN ARRAY OF ARRAYS THAT CONTAINS (IN EACH ARRAY) A SINGLED OUT CELL FROM EACH IMAGE
# EX: singled_out_cells_per_image[0][0]: in the first cell image, get the first image of the cell and just that
def single_out_cells_from_images(images,masks):
    singled_out_cells_per_mask = []
    for i in range(len(images)):
        singled_out_cells = []
        for num in np.unique(masks[i].data)[1:]:
            single_mask = np.where(masks[i] == num, images[i][...,3], 0)
            singled_out_cells.append(single_mask)
        singled_out_cells_per_mask.append(singled_out_cells)
    return np.array(singled_out_cells_per_mask)

singled_out_cells_per_image = single_out_cells_from_images(images, masks)

## PART 2 - centroids
# This will work on matching the cells on a sequence of images

# FROM A SET OF COORDINATES DETERMINE THE CENTER COORDINATE
def centeroidnp(arr):
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return np.array([sum_x/length, sum_y/length])

# CALCULATE ALL THE CENTEROIDS OF EVERY CELL IN EVERY IMAGE
def get_all_centeroids_per_mask(singled_out_cells_per_image):
    centeroids_per_mask = []
    for i in range(singled_out_cells_per_image.shape[0]):
        centeroids = []
        for singled_out_cell in singled_out_cells_per_image[i]:
            coordinates_of_val = np.argwhere(singled_out_cell != 0)
            centeroids.append(centeroidnp(coordinates_of_val))
        centeroids = np.array(centeroids)
        centeroids_per_mask.append(centeroids)
    centeroids_per_mask = np.array(centeroids_per_mask)
    return centeroids_per_mask

centeroids_per_mask = get_all_centeroids_per_mask(singled_out_cells_per_image)

# MATCH ALL OF THE CELLS IN TWO DIFFERENT ARRAYS
def match_points(points1, points2):
    matched_points = []
    for i in range(len(points1)):
        all_distances_from_point = []
        for j in range(len(points2)):
            dist = np.linalg.norm(points1[i] - points2[j])
            all_distances_from_point.append(dist)
        index_of_matched_point_from_points_2 = np.argmin(all_distances_from_point)
        matched_points.append({"index":(i,index_of_matched_point_from_points_2) , "coor":(points1[i],points2[index_of_matched_point_from_points_2])})    
    return matched_points

# FOR EACH CELL IMAGE MATCH EVERY CELL TOGETHER
def match_images(centeroids_per_mask):
    all_matched_points = []
    for i in range(len(centeroids_per_mask)-1):
        matched_points = match_points(centeroids_per_mask[i],centeroids_per_mask[i+1])
        all_matched_points.append(matched_points)
    #Right now it is of size 2, so we really only have to do 1 comparison
    #For each points in the second part of the first array, check if there is an equal one in the first part of the second array
    for i in range(len(all_matched_points[0])):
        all_pairs = []
        first_array_second_coor = all_matched_points[0][i]['coor'][1]
        #loop through second array's first coor until you find a match
        all_points_in_second_arr_first_coor = []
        for j in range(len(all_matched_points[1])):
            if all_matched_points[1][j]['coor'][0][0] == first_array_second_coor[0] and all_matched_points[1][j]['coor'][0][1] == first_array_second_coor[1]:
                pair = (all_matched_points[0][i]['coor'],all_matched_points[1][j]['coor'])
                all_pairs.append(pair)

all_pairs = match_images(centeroids_per_mask)

#matched_points = match_points(centeroids_per_mask[0],centeroids_per_mask[1])



#for i in range(len(matched_points)):
#    print(matched_points[i])
#print(matched_points)

#print('XXX',matched_points[i]["coor"][0][0])
#print('XXX',matched_points[i]["coor"][0][1])
#print('XXX',matched_points[i]["coor"][1][0])
#print('XXX',matched_points[i]["coor"][1][1])

#x = np.random.randn(60) 
#y = np.random.randn(60)

#plt.scatter(x, y, s=80, facecolors='none', edgecolors='r')
#plt.show()

#colors = ['b','g','r','c','m','y','k','w']
#plt.plot(100,100,'bo')
#plt.show()
#for i in range(len(matched_points)-1):
#    print(colors[i])
#    plt.plot(matched_points[i]["coor"][0][0],matched_points[i]["coor"][0][1], 'bo', color=colors[i])
#    plt.plot(matched_points[i]["coor"][1][0],matched_points[i]["coor"][1][1], 'bo', color=colors[i])
#plt.xlim([0,1080])
#plt.ylim([0,1080])
#plt.show()
# would be better to display them in a plot where matched points have the same color really