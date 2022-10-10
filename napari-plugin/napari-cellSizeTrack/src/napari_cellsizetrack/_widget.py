"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
#from curses import window
import datetime
from enum import Enum
from pathlib import Path
from magicgui import magicgui
import math
from typing import TYPE_CHECKING

from napari.types import ImageData

from magicgui import magic_factory
import numpy as np
from psygnal import EventedModel
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget, QToolTip

from napari.settings import get_settings

if TYPE_CHECKING:
    import napari

import napari
viewer = napari.Viewer()
layer = viewer.add_image(np.random.random((512, 512)))

class ExampleQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, viewer: 'napari.viewer.Viewer'):
        super().__init__()
        self.viewer = viewer

        viewer.bind_key("f", self._func)


        #QToolTip.setFont(QFont('SansSerif', 10))
        #self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton("Click me!")
        #btn.setToolTip('This is a <b>QPushButton</b> widget')
        #btn.clicked.connect(self._on_click)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(btn)

        

        #w1 = ComboBox(choices=choices, value='two', label='ComboBox:')

    def _on_click(self):
        print("napari has", len(self.viewer.layers), "layers")
        print("layers:",self.viewer.layers)

    def _func(self, viewer):
        print("ffffffffffffffffffff")

    @layer.mouse_move_callbacks.append
    def update_layer(layer, event):
        #layer.data = np.random.random((512, 512))
        #print(event.pos)
        print(layer.world_to_data(viewer.cursor.position))
        print(round(layer.world_to_data(viewer.cursor.position)[0]))
        print(round(layer.world_to_data(viewer.cursor.position)[1]))
        #print(layer.coordinates)
        

@magic_factory
def example_magic_widget(img_layer: "napari.layers.Labels"):

    print(f"you have selected {img_layer}")
    print("type",type(img_layer))
    print("data",img_layer.data)
    print("data type",type(img_layer.data))
    print("max num/number of segmented cells:",img_layer.data.max())

    
    unique, size_of_cells_in_pixels = np.unique(img_layer.data, return_counts=True)

    #Printing the number of labelled pixels
    size_of_mask_in_pixels = np.count_nonzero(img_layer.data) #count of every pixel that does not have a value of 0 as 0 is background
    print("Total labelled area of mask:",size_of_mask_in_pixels,"pixels")

    #Printing biggest and smallest cell sizes and their corresponding indexes
    smallest_cell_num_pixels = np.amin(size_of_cells_in_pixels)
    smallest_cell_index = np.where(size_of_cells_in_pixels == smallest_cell_num_pixels)[0][0]
    print("Smallest cell's index:",smallest_cell_index)
    print("Smallest cell size in pixels:",smallest_cell_num_pixels)
    biggest_cell_num_pixels = np.amax(size_of_cells_in_pixels[1:]) #starting from 1 since the pixel intensity 0 is the most common one so it would say the background (of pixel intensity 0) as the background
    biggest_cell_index = np.where(size_of_cells_in_pixels == biggest_cell_num_pixels)[0][0]
    print("Biggest cell's index:",biggest_cell_index)
    print("Biggest cell size in pixels:",biggest_cell_num_pixels)

    #Print average size of cells
    average_cell_size_in_pixels = np.average(size_of_cells_in_pixels[1:])
    print("Average cell size in pixels",average_cell_size_in_pixels)
    
    @viewer.bind_key('i')
    def add_layer(viewer):
        viewer.add_image(np.random.random((512, 512)))
    


    #create a mask with only cell 1 (or cell selected from dropdown)
        #this will be useful to work on the "hover to higlight cell"



# Uses the `autogenerate: true` flag in the plugin manifest
# to indicate it should be wrapped as a magicgui to autogenerate
# a widget.
#def example_function_widget(img_layer: "napari.layers.Image"):
#    print(f"you have selected {img_layer}")
