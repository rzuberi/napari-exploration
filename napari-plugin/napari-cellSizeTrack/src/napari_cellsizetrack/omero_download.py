# File to download images from Omero locally

# Connect to Omero

import ezomero
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import PIL
from PIL import Image
import os
import tifffile
from tifffile import imread

HOST = 'ome2.hpc.sussex.ac.uk' #change if different
port=4064
conn = ezomero.connect(user='rz200',password='omeroreset',group='',host=HOST,port=4064,secure=True)
if conn: print('Connection successful')
else: print('Unsuccessful')

print(os.getcwd())
#os.makedirs(str(os.getcwd() + '\Example_imgs\data_to_upload\\serie' + str(2) + '\\'))

def save_plate_locally(plate_id):
    image_ids = ezomero.get_image_ids(conn,plate=plate_id)
    print('In plate',plate_id,'we have',len(image_ids),'images')
    #image_from_omero = ezomero.get_image(conn,image_id=image_ids[0])

    #print(image_from_omero[1][0][0].shape)

    for i in range(len(image_ids)):
        print(str(i) + '/' + str(len(image_ids)))
        os.makedirs(os.getcwd() + '\Example_imgs\data_to_upload\\serie' + str(i) + '\\')
        image_from_omero = ezomero.get_image(conn,image_id=image_ids[i])
        for j in range(image_from_omero[1].shape[0]):
            result = Image.fromarray(image_from_omero[1][i][0].reshape(1080,1080).astype(np.uint16))
            path_to_save = os.getcwd() + '\Example_imgs\data_to_upload\\serie' + str(i) + '\\' + str(j) + '.tiff'
            result.save(path_to_save)
        #if i == 3: break

#save_plate_locally(449)

def import_cell_images(path,num_images):
    images = []
    for i in range(num_images):
        if i % 50 == 0: print(str(i+1)+"/180")
        path_to_img = path + str(i) + '.tiff'
        images.append(np.squeeze(imread(path_to_img)))
    return np.array(images)

def display_with_slider(plate_id,serie):
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()
    img = ax.imshow(np.random.rand(3, 3))
    image_ids = ezomero.get_image_ids(conn,plate=449)
    image = ezomero.get_image(conn,image_id=image_ids[1])
    axcolor = 'yellow'
    ax_slider = plt.axes([0.20, 0.01, 0.65, 0.03], facecolor=axcolor)
    slider = Slider(ax_slider, 'Slide->', 0, 60, valinit=0)
    def update(val):
        #ax.imshow(np.random.rand(3, 3))
        print(val)
        val = int(np.round(val))
        print(val)
        ax.imshow(image[1][val][0])
        fig.canvas.draw_idle()
    slider.on_changed(update)
    plt.show()

#display_with_slider(449,1)