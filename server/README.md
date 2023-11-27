# Backend Files

This folder contains the Python files to perform the back-end processes for the GUI.

## Files

### display.py

This file contains the functions to display the results of the post-processing methods as a matplotlib figure. The functions are called by the 'process.py' file.

- normalize: Normalizes a 2D numpy array to a range between 0 and 255.
- display: Displays multiple 2D numpy arrays in a single matplotlib figure, using 'normalize' to make them all have the same scale. Has a colorbar for reference. Saves the figure as a .png file and returns the path to the file.

### PCT.py

This file contains the functions to perform the Principal Component Thermography (PCT) method. The functions are called by the 'process.py' file. Other methods based off of PCT may be added to this file.

- PCT: Performs the PCT method on a 3D numpy array. Returns a 2D numpy array of the same size as the a single frame of the input array. Extra parameters can change the number of principal components extracted, or the normalization method which can vary the results.
- SPCT: Similar to PCT, but uses Sparce Principal Component Thermography (SPCT) instead. More computationally expensive.

### process.py

This file contains the functions to perform the post-processing methods. The functions are called by the 'server.py' file.

- readVideo: Reads a video file and returns it as a 3D numpy array
- createMask: Creates a mask for two videos in the same position. Results are two masked videos.
- process: Performs post-processing methods on a cold or hot video. The videos are first masked in the same position, then are processed. The results are displayed and saved as .png files. The paths to the results are returned. Do note that this assumes that the RoI in the cold and hot videos are in the same position. If they are not, results may be inaccurate.
