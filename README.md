# napari-exploration

What I think this project will be (these are my unfinished quickly written ideas for the pre-interim report for my supervisors)
- A Napari plugin that can segment out cells, using the ones found by CellPose2.
- A Napari plugin that has a trainable model to classify cells by their cell cycle phase from only one (or a selection) of channels. It first asks the use to label some cells manually and then trains the model which can then be applied on many cell micrographs. Could make it a human-in-the-loop model like CellPose2.
- A Naparai plugin that perfoms some tracking on cells such as size, shape, and cell cycle phase. It could give some interesting data on sequential micrographs about how long cells stay in phases and take to go through the entire cycle.

For this, I would also need to write the purpose and need for these plugins and review other Napari plugins that might already be doing this (and why making them generalisable to every marker is important).

And why Napari? Because its a popular, open-source, emerging and popular python image viewer where every developer can easily contribute and improve through plugins which makes it accessible to less computer sciency cell biologists.

I think I can discard the "segmenting out" napari plugin development because CellPose2 already creates the segementation mask quite well. I could provide further features for a segmentation plugin such as:
- "only look at this cell" which takes the CellPose2 segmentation of a cell and discards everything in the micrograph apart from what the mask found
- "label this cell" where you can hover over a cell and select it to manually label it (such as cell class, even if it would not be very useful to label it this way since more data needs to be known then just looking at it). It could also just give some numbers about that mask (such as intensity of the different masks)

# When setting up Omero
- The portal address is the following: bond.sussex.ac.uk
- The Omero database address if the following: ome2.hpc.sussex.ac.uk
