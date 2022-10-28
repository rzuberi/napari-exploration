## PART 1 - extracting the cells

# Read the TIF image and the mask and separate the four channels
from calendar import c
import os
from xml.etree import cElementTree
import numpy as np
import tifffile
from tifffile import imread
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
import cellpose
from cellpose import models, core
import PIL
from PIL import Image
from scipy.spatial import distance
import time

print('GPU activated',core.use_gpu())

## PART 0: Reading the images

#IMPORT IMAGES
def import_cell_images(path,num_images):
    images = []
    for i in range(num_images):
        if i % 50 == 0: print(str(i+1)+"/180")
        path_to_img = path + str(i) + '.tiff'
        images.append(np.squeeze(imread(path_to_img)))
    return np.array(images)

images = import_cell_images(os.getcwd() + '\Example_imgs\data_to_upload2\serie0\\', 5)
print('SSSSS',images.shape)

def display_with_slider(images):
    fig, ax = plt.subplots()
    axcolor = 'yellow'
    ax_slider = plt.axes([0.20, 0.01, 0.65, 0.03], facecolor=axcolor)
    slider = Slider(ax_slider, 'Slide->', 0, len(images)-1, valinit=0)
    def update(val):
        val = int(np.round(val))
        ax.imshow(images[val])
        fig.canvas.draw_idle()
    slider.on_changed(update)
    plt.show()

#display_with_slider(images)

#CREATE AND SAVE MASKS
def create_masks_and_save(path, images):
    model = models.Cellpose(gpu=True, model_type='nuclei')
    channels = [0,0]
    for i in range(len(images)):
        mask, flows, styles, diams = model.eval(images[i], diameter=None, flow_threshold=None, channels=channels)
        result = Image.fromarray(mask.astype(np.uint8))
        path_to_save = path + str(i) + '.tif'
        result.save(path_to_save)

#create_masks_and_save(os.getcwd() + '\Example_imgs\data_to_upload2\serie0_masks\\', images)

#IMPORT MASKS
def import_masks(path,num_masks):
    masks = []
    for i in range(num_masks):
        path_to_mask = path + str(i) + '.tif'
        masks.append(np.squeeze(imread(path_to_mask)))
    return np.array(masks)

start_time = time.time()
masks = import_masks(os.getcwd() + '\Example_imgs\data_to_upload2\serie0_masks\\', len(images))
print("--- %s seconds ---" % (time.time() - start_time))


# GET AN ARRAY OF ARRAYS THAT CONTAINS (IN EACH ARRAY) A SINGLED OUT CELL FROM EACH IMAGE
# EX: singled_out_cells_per_image[0][0]: in the first cell image, get the first image of the cell and just that
def single_out_cells_from_images(images,masks):
    #data_arr = [np.array([image]) for image in images]
    #data_arr = np.concatenate((data_arr, masks.T), axis=1)
    #print(data_arr)
    #print(data_arr.shape)

    #for i in range(len(data_arr)):
    #    data_arr[i].append(masks[i])
    #    data_arr[i] = np.array(data_arr)
    #data_arr = np.array(data

    singled_out_cells_per_mask = []
    for i in range(len(images)):
        singled_out_cells = []
        for num in np.unique(masks[i].data)[1:]:
            single_mask = np.where(masks[i] == num, images[i][...,3], 0)
            singled_out_cells.append(single_mask)
        #data_arr[i].
        singled_out_cells_per_mask.append(singled_out_cells)
    return np.array(singled_out_cells_per_mask)

singled_out_cells_per_image = single_out_cells_from_images(images, masks)

# Array of images
# Array of masks
# Array of singled out cells per image
# If I want to find what image a singled out cell is from, I juse need to look at the index of the array it is currently in
# singled_out_cells_per_image = [index of image/mask][cells]
            
#print (len(singled_out_cells_per_image[0]))

## PART 2 - centroids
# This will work on matching the cells on a sequence of images

# FROM A SET OF COORDINATES DETERMINE THE CENTER COORDINATE
def centeroidnp(arr):
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return np.array([sum_x/length, sum_y/length])

# CALCULATE ALL THE CENTEROIDS OF EVERY CELL IN EVERY IMAGE
# I want to change this function to deliver the centeroids_per mask with the mask and the cell number

def get_all_centeroids_per_mask(singled_out_cells_per_image):
    centeroids_per_mask = []
    for i in range(singled_out_cells_per_image.shape[0]):
        centeroids = []
        for singled_out_cell in singled_out_cells_per_image[i]:
            coordinates_of_val = np.argwhere(singled_out_cell != 0)
            centeroids.append([singled_out_cell,centeroidnp(coordinates_of_val)])
        centeroids = np.array(centeroids)
        centeroids_per_mask.append(centeroids)
    centeroids_per_mask = np.array(centeroids_per_mask)
    return centeroids_per_mask

centeroids_per_mask = get_all_centeroids_per_mask(singled_out_cells_per_image)

print(centeroids_per_mask)
#Now data is
    # For each mask
        # The singled out cell image and the centroid

#centeroids_per_mask = [image/mask index][index of cell in the masks]

#print(centeroids_per_mask)

#Function to get for each cell in each mask the index of the point that they match with from after
# This would be in a new list
def get_matches(centeroids_per_mask):
    #So we have a list of masks
        #that each have a list of cell images and their centroids

    #array that will hold, per mask, the list of matches
    matches = []
    #We need for each masks, except the last one
    for i in range(len(centeroids_per_mask)-1):
        #mask (list of cells)
        mask_1 = centeroids_per_mask[i]
        #mask that comes after (list of cells)
        mask_2 = centeroids_per_mask[i+1]
        #empty array that will hold the indexes of cells that match from the first to the second array (so the length is the number of cells in the first array)
        matches_for_mask_1 = [] #the index of the element represents the index of the cell in mask_1, and the element is the index of the matched cell in mask_2
        #for each cells in the first list
        for cell in mask_1:
            #find the one that matches with the cell from the second list
            #first lets get a list of the coordinates of the cells in mask_2
            all_distances_from_cell = []
            for j in range(len(mask_2)):
                dist = np.linalg.norm(cell[1] - mask_2[j][1])
                all_distances_from_cell.append(dist)
            index_of_matched_point_from_points_2 = np.argmin(all_distances_from_cell)

            #append that index to the empty array defined above
            matches_for_mask_1.append(index_of_matched_point_from_points_2)
        matches.append(matches_for_mask_1)
    #later one we may want to concatenate both of these lists as they will hold for each element per mask
        #[singled out image, centroid coordinates, index of cell it maches with in the next mask]
    return matches

matches = get_matches(centeroids_per_mask)
print(matches)

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

def get_all_matched_points(singled_out_cells_per_image, centeroids_per_mask):
    all_matched_points = []
    for i in range(len(centeroids_per_mask)-1):
        matched_points = match_points(centeroids_per_mask[i],centeroids_per_mask[i+1])
        all_matched_points.append(matched_points)
    return all_matched_points

#all_matched_points = get_all_matched_points(singled_out_cells_per_image, centeroids_per_mask)
#for point in all_matched_points:
#    print('\n')
#    print(point)


# FOR EACH CELL IMAGE MATCH EVERY CELL TOGETHER
def match_images(centeroids_per_mask):
    all_matched_points = []
    for i in range(len(centeroids_per_mask)-1):
        matched_points = match_points(centeroids_per_mask[i],centeroids_per_mask[i+1])
        all_matched_points.append(matched_points)
    #Right now it is of size 2, so we really only have to do 1 comparison
    #For each points in the second part of the first array, check if there is an equal one in the first part of the second array
    all_pairs = []
    for i in range(len(all_matched_points[0])):
        first_array_second_coor = all_matched_points[0][i]['coor'][1]
        #loop through second array's first coor until you find a match
        all_points_in_second_arr_first_coor = []
        for j in range(len(all_matched_points[1])):
            if all_matched_points[1][j]['coor'][0][0] == first_array_second_coor[0] and all_matched_points[1][j]['coor'][0][1] == first_array_second_coor[1]:
                pair = (all_matched_points[0][i]['coor'],all_matched_points[1][j]['coor'])
                all_pairs.append(pair)

    #singled_out_cells_pairs = []
    #for pair in all_pairs:
        #take the first pair and need to m
    
    return all_pairs

#all_pairs = match_images(centeroids_per_mask)
#print('XXXX',centeroids_per_mask.shape)
#for i in range(len(all_pairs)):
#    print(all_pairs[i])

#matched_points = match_points(centeroids_per_mask[0],centeroids_per_mask[1])

##TODO: a function that would display only the centroids of the cells per image with a slider to get to the next image but each centroid (which is just the point) has the color of the other centroids it was matched with

#print(matched_points)

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
#print('leeeennn',len(matched_points))
#for i in range(8):
    #print(colors[i % len(matched_points)])
#    plt.plot(matched_points[i]["coor"][0][0],matched_points[i]["coor"][0][1], 'bo', color=colors[i])
#    plt.plot(matched_points[i]["coor"][1][0],matched_points[i]["coor"][1][1], 'bo', color=colors[i])
#plt.xlim([0,1080])
#plt.ylim([0,1080])
#plt.show()
# would be better to display them in a plot where matched points have the same color really