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
from PyQt5.QtCore import QPoint
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget, QToolTip

from napari.settings import get_settings

import pyautogui

from napari.utils.events import Event

if TYPE_CHECKING:
    import napari

import napari
viewer = napari.current_viewer()
#layer = viewer.add_image(np.random.random((512, 512)))
#layer = viewer.layers.selection
layer = viewer.layers.selection.active

#def _on_change(event):
#    layer = viewer.layers.selection
#    print('layer changed')

#viewer.layers.selection.events.changed(_on_change)

#@viewer.layers.selection.events.changed.connect
#def change_layer():
#    layer = viewer.layers.selection.active

#def change_layer_selection(event):
        #layer = viewer.layers.selection.active
#        change_layer()
#        print("layer changed")
    
    #viewer.layers.selection.events.changed.connect(change_layer_selection)


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

        layer = viewer.layers.selection.active
        
        self.setMouseTracking(True)
        

        #w1 = ComboBox(choices=choices, value='two', label='ComboBox:')

    def _on_click(self):
        print("napari has", len(self.viewer.layers), "layers")
        print("layers:",self.viewer.layers)

    def _func(self, viewer):
        print("ffffffffffffffffffff")

    @viewer.mouse_move_callbacks.append
    def update_layer(self, event):
        print('eventxxx',event)
        #layer.data = np.random.random((512, 512))
        #print(event.pos)
        #layer = viewer.layers.selection.active
        x_coor = round(viewer.cursor.position[0])
        y_coor = round(viewer.cursor.position[1])

        #We first need to find the layer so we loop through all the layers in the viewer
        for lay_it in viewer.layers:
            #We only want the layers that are label layers since that's what we want to display
            if str(type(lay_it)) == "<class 'napari.layers.labels.labels.Labels'>":
                #If the layer is of type label AND that it is the one currently selected
                if lay_it in viewer.layers.selection:
                    print(x_coor,y_coor) #print the coordinates of the mouse
                    #print('mouse track', event.x(), event.y())
                    print(viewer.layers.selection) #print the name of the currently selected layer
                    current_layer = lay_it
                    current_layer_data = current_layer.data #get the data of
                    if x_coor < 1080 and x_coor > -1 and y_coor < 1080 and y_coor > -1:
                        cell_mask_number = current_layer.data[x_coor][y_coor]  
                        if cell_mask_number != 0:
                            print('data at coordinates (cell mask number)',cell_mask_number)
                        
                            #self.x = event.pos().x()
                            #self.y = event.pos().y()
                            #p = mapToGlobal(event.pos())
                            p = QPoint()
                            #p.setX(x_coor)
                            #p.setY(y_coor)
                            p.setX(pyautogui.position()[0])
                            p.setY(pyautogui.position()[1])

                            #self.x = event.pos().x()
                            #self.y = event.pos().y()

                            #p = self.mapToGlobal(event.pos())

                            QToolTip.showText(p,str(cell_mask_number))


                            #QToolTip.showText(p, x_coor)
                            #event.setToolTip('sfdfdfds')
        #make it print at the coordinates


            #print('11',lay)
            #print(type(lay))
            #print(lay.data)

        #get the labels
        #print(viewer.layers.selection.data)
        #print(napari.layers.Labels.name)
        #print(viewer.layers.selection[0])

        #print(napari.layers.Labels[viewer.layers.selection])

        #print at those coordinates the current label

    
        

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
