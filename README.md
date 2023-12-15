# Thermographic Inspection GUI

A web app GUI to perform thermographic inspection post-processing methods on thermal videos.

## Dependencies

### Python

- Python (v3.11.5)
- opencv-python
- numpy
- scikit-learn
- matplotlib
- Flask
- Flask-Cors

### Node

- Node.js (v21.2.0)

## Installation

You can install Python from [here](https://www.python.org/downloads/), or use a package manager such as [Anaconda](https://www.anaconda.com/products/individual). \
The Python libraries can be installed using pip. You can run 'pip install dependency_name' in the terminal to install the libraries, or run ```pip install -r requirements.txt``` to install all the libraries at once.

You can install Node.js from [here](https://nodejs.org/en/download/), or use a node version manager with this [guide](https://www.freecodecamp.org/news/node-version-manager-nvm-install-guide/). \
The Node.js libraries are all included in the package.json file, and can be automatically installed by running 'npm install' in the terminal in the client directory.

## Usage

First, run 'server/server.py' to start the back-end server. Then, go to the client directory, and start the web app with the command ```npm run dev```
