# napari-exploration

What I think this project will be (these are my unfinished quickly written ideas for the pre-interim report for my supervisors)
- A Napari plugin that can segment out cells, using the ones found by CellPose2.
- A Napari plugin that has a trainable model to classify cells by their cell cycle phase from only one (or a selection) of channels. It first asks the use to label some cells manually and then trains the model which can then be applied on many cell micrographs. Could make it a human-in-the-loop model like CellPose2.
- A Naparai plugin that perfoms some tracking on cells such as size, shape, and cell cycle phase. It could give some interesting data on sequential micrographs about how long cells stay in phases and take to go through the entire cycle.

For this, I would also need to write the purpose and need for these plugins and review other Napari plugins that might already be doing this (and why making them generalisable to every marker is important).

And why Napari? Because its a popular, open-source, emerging and popular python image viewer where every developer can easily contribute and improve through plugins which makes it accessible to less computer sciency cell biologists.
