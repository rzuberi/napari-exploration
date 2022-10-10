Quick tutorial on how to setup Napari on Windows and documentation of problems that I encountered

## Setup Napari

Following this tutorial: https://napari.org/stable/tutorials/fundamentals/installation.html#installation
1. Install Anaconda terminal if that is not already on your computer
2. Inside the terminal, create a virtual environment with the following commands:

```conda create -y -n napari-env -c conda-forge python=3.9```

```conda activate napari-env```

3. Install the napari package with the following commands:

```python -m pip install "napari[all]"```
```python -m pip install "napari[all]" --upgrade```

4. Launch Napari by typing the name in the console:

 ```napari```


## Troubleshooting on Windows

1. If you received the following error: ```ImportError: DLL load failed while importing QtGui: The specified procedure could not be found.```

- Please make sure you used the same command to create the virtual environment as above in the 2nd step of the "Setup Napari" tutorial. While creating an environment with the ```conda create --name napari-env python=3.9" command I got the same error.


2. If you receive the following error:  ```ModuleNotFoundError: No module named 'imageio_ffmpeg'```

- The quick fix is typing in the following command: ```pip install imageio_ffmpeg```.

## Troubleshooting on Mac
(I haven't yet tried installing it on my Mac, but I will and get back to this document)

## Quickstart on Windows

```
conda create -y -n napari-env -c conda-forge python=3.9
conda activate napari-env
python -m pip install "napari[all]"
python -m pip install "napari[all]" --upgrade
pip install imageio_ffmpeg
conda install git
napari

```
