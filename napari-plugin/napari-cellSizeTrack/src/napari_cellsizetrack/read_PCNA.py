## PART 1 - extracting the cells

# Read the TIF image and the mask and separate the four channels
from calendar import c
import os
from symbol import single_input
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
images = []
for i in range(3):
    if i % 50 == 0: print(str(i+1)+"/180")
    path_to_img = os.getcwd() + '\Example_imgs\data\images\\' + str(i) + '.tif'
    images.append(np.squeeze(imread(path_to_img)))
print(len(images))

#IMPORT MASKS
masks = []
for i in range(len(images)):
    path_to_mask = os.getcwd() + '\Example_imgs\data\masks\\' + str(i) + '.tif'
    masks.append(np.squeeze(imread(path_to_mask)))
print('masks:',len(masks))
print('shape of masks',masks[0].shape)

#CREATE AND SAVE MASKS
#model = models.Cellpose(gpu=True, model_type='nuclei')
#channels = [0,0]
#masks, flows, styles, diams = model.eval(images, diameter=None, flow_threshold=None, channels=channels)
#print(len(masks))
#for i in range(len(masks)):
#    result = Image.fromarray(masks[i].astype(np.uint8))
#    path_to_save = os.getcwd() + '\Example_imgs\data\masks\\' + str(i) + '.tif'
#    result.save(path_to_save)



#create a mask with cellpose of all of the images
print('images shape',images[0].shape)

singled_out_cells_per_mask = []
for i in range(len(images)):
    singled_out_cells = []
    for num in np.unique(masks[i].data)[1:]:
        single_mask = np.where(masks[i] == num, images[i][...,0], 0)
        singled_out_cells.append(single_mask)
    singled_out_cells_per_mask.append(singled_out_cells)
print(len(singled_out_cells_per_mask))
print(len(singled_out_cells_per_mask[0]))
print(len(singled_out_cells_per_mask[1]))
#print(len(singled_out_cells_per_mask[2]))

#Now need to read the all of the images and get all of their singled_out_cells data

## PART 2 - centroids
# This will work on matching the cells on a sequence of images

def centeroidnp(arr):
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return np.array([sum_x/length, sum_y/length])

#Next need to compute centeroids between cells and compare them
centeroids_per_mask = []
for i in range(len(images)):
    centeroids = []
    for singled_out_cell in singled_out_cells_per_mask[i]:
        coordinates_of_val = np.argwhere(singled_out_cell != 0)
        centeroids.append(centeroidnp(coordinates_of_val))
    centeroids = np.array(centeroids)
    centeroids_per_mask.append(centeroids)
centeroids_per_mask = np.array(centeroids_per_mask)
print(len(centeroids_per_mask))
print(len(centeroids_per_mask[0]))
print(len(centeroids_per_mask[1]))
print(len(centeroids_per_mask[2]))

#for i in range(len(centeroids_per_mask[0])):
    

#ids = centeroids_per_mask[1][np.argmin(distance.cdist(centeroids_per_mask[2], centeroids_per_mask[1][:,:-1]),axis=1)][:,-1]
#new_arr = np.hstack([centeroids_per_mask[2],ids.reshape(-1,1)])

#print(centeroids_per_mask[1])
#print(centeroids_per_mask[2])
#print(new_arr)

def match_points(points1, points2):
    matched_points = []
    for i in range(len(points1)):
        all_distances_from_point = []
        for j in range(len(points2)):
            dist = np.linalg.norm(points1[i] - points2[j])
            all_distances_from_point.append(dist)
        index_of_matched_point_from_points_2 = np.argmin(all_distances_from_point)
        matched_points.append({"index":(1,index_of_matched_point_from_points_2) , "coor":(points1[i],points2[index_of_matched_point_from_points_2])})    
    return matched_points

pts = np.concatenate((centeroids_per_mask[0],centeroids_per_mask[1]),axis=0)
spts = pts[pts[:,1].argsort(),]
counts = np.sum(np.diff(np.all(np.diff(spts,axis=0)==0,1)+0)==1)
#print('SPTS',spts)
matched_points = match_points(centeroids_per_mask[0],centeroids_per_mask[1])

for i in range(5):
    print(matched_points[i])
#print(matched_points)

print('XXX',matched_points[i]["coor"][0][0])
print('XXX',matched_points[i]["coor"][0][1])
print('XXX',matched_points[i]["coor"][1][0])
print('XXX',matched_points[i]["coor"][1][1])


colors = ['b','g','r','c','m','y','k','w']

plt.plot(100,100,color='green')
for i in range(5):
    print(colors[i])
    plt.plot(matched_points[i]["coor"][0][0],matched_points[i]["coor"][0][1])
    plt.plot(matched_points[i]["coor"][1][0],matched_points[i]["coor"][1][1])
plt.show()
# would be better to display them in a plot where matched points have the same color really