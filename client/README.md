# Front-End Web App

## Relevant Files

### `pages` folder

- `index.tsx` - The main page of the web app. Contains all the components for the web app. When the web app is started, this is the page that is loaded. 

### `components` folder

- `ProcessBoard.tsx` - The process board takes in a setter function for the path to the result image. It contains a dropdown menu for the different methods, a column of text inputs for the parameters, and a button to run the method. The button will send a request to the back-end to run the method, and the back-end will return the path to the result image. The setter function will then be called to update the path to the result image.
- `TextCard.tsx` - A card that takes in text as input, and displays it in a card.
- `UploadButton.tsx` - A component that takes in the type of file to upload (cold or hot), and creates a set of buttons to choose the file, and upload it to the back-end. Also displays the status of the upload.

### `styles` folder

Contains the CSS files for the components, which match the names of the components. Also contains the global CSS file for all common CSS styles.

### `public` folder

Results of the processed images are stored here.
