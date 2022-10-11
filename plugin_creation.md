Here are some notes on creating a plugin with Napari
You could follow the tutorial like I did on [this link on the official Napari website](https://napari.org/stable/plugins/first_plugin.html) 

1. Amazingly I hadn't installed GitHub and got an error for it when running the CookieCutter to create a napari plugin with a template. "git" has to be installed before "cookiecutter" can be installed. Here's the command to install git in Conda:

```conda install git``` 


2. If you're trying to develop a Napari plugin without creating a new one (i.e. basing yourself on one that you've already started making) then just go into the folder of that plugin and type the following command. This will pip install your plugin and make sure that everytime you close and re-open Napari, it reads the new code you wrote for it.

```pip install -e .```


3. Having problems with SSL connection when trying the command  ```conda install git``` in the Anaconda terminal. Therefore I had to downgrade conda with the follwing command:

```conda install conda==4.14.0```
