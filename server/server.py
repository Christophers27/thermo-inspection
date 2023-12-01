from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from process import process

# Create Flask app
app = Flask(__name__)
CORS(app)

# Global variables
coldPath, hotPath = None, None


@app.route("/upload", methods=["POST", "GET"])
def upload():
    """Receives video file from client and saves it to the server

    Returns:
        msg: Message to client as JSON
    """
    # Check if files are uploaded
    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"})

    # Get file and details
    file = request.files["file"]
    fileName = file.filename
    fileType = request.form["type"]

    # Check if file is empty
    if fileName == "":
        return jsonify({"message": "No file selected"})

    # Check if file is video
    if file.filename.split(".")[-1] not in ["mp4", "avi", "mov"]:
        return jsonify({"message": "File is not a video"})

    # Save file
    file.save("temp/" + fileName)

    if fileType == "cold":
        global coldPath
        coldPath = "temp/" + fileName
    elif fileType == "hot":
        global hotPath
        hotPath = "temp/" + fileName

    return jsonify({"message": "File uploaded successfully"})


@app.route("/process", methods=["POST", "GET"])
def processVideo():
    global coldPath, hotPath

    # Check if both videos are uploaded
    if coldPath is None:
        return jsonify({"message": "Cold video not uploaded"})
    elif hotPath is None:
        return jsonify({"message": "Hot video not uploaded"})

    # Get processing method
    method = request.form["method"]
    options = request.form["options"]
    options = json.loads(options)

    print(method, options)

    # Process video
    resPath = process(coldPath, hotPath, "client/public/", method, options)
    resPath = resPath.removeprefix("client/public/")

    return jsonify({"message": "Video processed successfully", "path": resPath})


if __name__ == "__main__":
    app.run(debug=True, port=8080)  # The default port 5000 doesn't work with CORS
