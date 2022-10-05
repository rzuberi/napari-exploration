This is where I am leaving the meeting notes that I took for my 3rd year project, for now.

Wednesday 21/09/2022 16h30-17h30:

Attendees: Dr Ivor Simpson, Dr Helfrid Hochegger, Rehan Zuberi

Location: Zoom meeting

- Mostly used TrackMate which is written in Java
	- You can look at theri algos
	- WE could combine our classification with TrackMate or make our own tracker
- Napari is what's being used with plugins
	- As good as TrackMate
	- https://napari.org/stable/tutorials/tracking/cell_tracking.html
- Keep things in Python
	- A cell cycle tracker would be very good
	- The "going foward" in the cell cycel, unlikely to go backwards in the phases
-  Let's dig into Napari
- In the next few months
	- We will do some cell cycle classification with different colors of trackers (green in G1, yellow is S etc.) https://www.tandfonline.com/doi/full/10.1080/15384101.2018.1547001
	- A lot of people are liking the PCNA because it is a single probe
- Helfrid says they should provide me with better data
- Differentiate between G1 and S, still not quite sure it can be done this year, it's a hard task 
- Anything I do in Napari is useful for the community
	- Can make me popular
	- Integrate something that exists in another program but in Napari
	- It's for the cell microscopists that use Python
- Low hanging fruits in Machine Learning with Biology
	- Very good field to go into
- First few weeks: familiarise myself with Napari
	- Build some tracks of the cells
	- Check out the plugins and tracking algorithms
	- Check where they might go wrong, try tracking a cell and classifying and see if it gives you consistent classification. If you spot a cell and it's rapidly changing between cell states, you shoud incorporate some more info into the algo. So check what the existing approaches seem to do.
- Should have the meeting combined with Ryan.
	- Give a presentation about what I've done during the project
	- Ryan is trying to see with markers if we can predict which phase the cell is in
- There is a cell line that has a  more pronounced PCNA stain that can be used for tracking and labelling.
	- The problem when we look at live is that we don't have additonal data to generate the labels automatically
- It would be good next wednesday to prepare a presenation on summarsing the JRA project for everyone in a more formal way
	- If I get some new data next week that would be great and show how the project will evolve
	- Will get higher quality pictures of cells from Helfrid
- Post-doc Rob of Helfrid wrote a script for labelling the EdU and Dapi stain to build the classifier that sets the thresholds automatically based on the peaks. It formalises the procedure which is good
	- Rob will send me the code
	- Around the thresholds line a gradient can be done to give the confidence of the phases, it will be a very powerful addition to the model
	- I can make a clean version of it when Rob sends it to improve it
	- //Build a soft threshold as Ivor suggested

Wednesday 28/09/2022 16h00-17h00:

Attendees: Dr Ivor Simpson, Dr Helfrid Hochegger, Ryan, Rehan Zuberi

Location: Zoom meeting

- Ryan talked about his project, the augmentation of the data and the features he was collecting off the cells right now
- Ivor explained to him, with a diagram, an encoder and decoder model (VAE) to extract more data from the image of marked cells
- Helfrid showed some the best way to flatten out a micrograph to get the brightness constant on the entire image. It is especially important for Tubulin.
- Ivor said that you should first test to see if your model can overfit to check if everything works
- I talked about how I've been playing around to discover Napari and its plugins. I talked about the 2009 intensity and surface curvature histogram feature cell classifying paper and Ivor and Helfrid had some things to say about it: Helfrid said that the paper did not get cited much, probably because it is too "complex" (means too computer sciency) for biologists. Ivor explained their method: It's a 2x2 matrix of the change of shape intensity in x, equation 7 in the paper, standard for describing how informative a region is, it's curvature in some sense but can be used to describe interesting blobs, it uses the ration between two eigen values that gives hwo elliptical it is or how spherical it is. CNNs should be able to already learn these patterns by itself right? Actually, you need the good quality and representative data that would permit to learn that, enough data to learn the right features, which is why CNNs were invented in the 80s but only properly used in 2013.
- I offered to present Napari and do a demonstration to Helfrid's lab and he strongly agreed
- Ivor asked me to start sketching a plan for what my dissertation will look like. I need to write that, I'll probably make a document with images and a straightforward Gant plan. I said I imagined my dissertation to offer the classification and tracking trainable models from only one cell marker as Napari plugins.
- Helfrid is confident about the project and having me until May to complete a lot of this.


Wednesday 05/10/2022 16h00-16h50:

Attendees: Dr Ivor Simpson, Ryan, Rehan Zuberi

Location: Zoom meeting

- Ryan talked about his project. He is introducing soft labels and talked about where to cut from the DNA content to separate cells in classes. He showed his code for his Variational Auto Encoder just to explain his layers. He showed for the M-phase DAPI the predicted results. He talked about the BCE loss (which is a loss for a binary classifier) and Ivor explained that for a multi class problem it does not work here, he is better off using the softmax function. For regression roblems (since here Ryan is trying to rebuild the data) he can't use a binary function, Ivor explains. Ivor proposed the multiclass [cross entropy loss](https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html) and the [MSE loss](https://pytorch.org/docs/stable/generated/torch.nn.MSELoss.html#torch.nn.MSELoss). Maybe PyTorch is doing something smart under the hood with the binary classifier and turning it into a multi class, but still it is better to change to a categorical one.
- I briefly talked about my project and how I have been discovering Napari (how it works under the hood, how to integrate plugins)
- Helfrid said the following (basically that if Napari can use video then we can use gained information from sequential frames to improve the information tracked on other frames):
    - Use tracking to improve the segmentation and classification because we can aggregate information across frames. Having multiple frames, we can segment them on the two different frames to get less noise. Pixel wise tracking or deform the frame before and the frame after so we can look and draw on the extra frames to assist the tracking of one. We could also have three output tracking inforation and we just pass the information, it should be able to draw on the segmentation performance. Same as for classification, we can think about the cycle. We can then feedback information about the classifier. Thinking about how we can track and also improve the tasks we want to do, we want to track the size of cells oer time but if we can improve the other tracking features with that.
- Ryan asked a question again which was on the DAPI labelling and then the meeting ended.
