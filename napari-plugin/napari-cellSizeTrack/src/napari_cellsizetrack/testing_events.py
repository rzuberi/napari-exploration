import numpy as np
import napari

viewer = napari.Viewer()

@viewer.bind_key('i')
def add_layer(viewer):
    viewer.add_image(np.random.random((512, 512)))

@viewer.bind_key('k')
def delete_layer(viewer):
    try:
        viewer.layers.pop(0)
    except IndexError:
        pass

napari.run()