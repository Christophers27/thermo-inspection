import cv2
import numpy as np
import os

from PCT import PCT, SPCT
from display import display


def readVideo(path):
    """Reads a video and returns a numpy array of the frames in grayscale

    Args:
        path (str): Path to the video

    Returns:
        np.ndarray: Numpy array of the frames in grayscale. Shape: (n_frames, height, width)
    """
    vid = cv2.VideoCapture(path)
    res, ret = [], True

    while ret:
        ret, frame = vid.read()
        if ret:
            res.append(
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            )  # We convert the frame to grayscale to make it one channel

    vid.release()
    return np.stack(res, axis=0)


def createMask(path1, path2):
    """Creates a mask for two videos. The mask is created by selecting a region of interest (RoI) in a frame from the first video (note that this requires the two videos to be aligned). The RoI is then used to mask the frames of both videos.

    Args:
        path1 (str): Path to the first video
        path2 (str): Path to the second video

    Raises:
        Exception: If the first video ends before selecting the RoI

    Returns:
        newPath1, newPath2: Tuple of the paths to the masked videos
    """
    vid1, vid2 = cv2.VideoCapture(path1), cv2.VideoCapture(path2)
    newPath1 = path1.replace(".mp4", "_mask.mp4")
    newPath2 = path2.replace(".mp4", "_mask.mp4")
    fps = vid1.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    # Create window to display frame and select RoI.
    ret, frame1 = vid1.read()
    while True:
        cv2.imshow("Press 's' to skip frame, 'c' to choose RoI", frame1)
        key = cv2.waitKey(0) & 0xFF
        if key == ord("s"):
            cv2.destroyAllWindows()
            ret, frame1 = vid1.read()

            if not ret:
                raise Exception("Video 1 ended before selecting RoI")

            continue
        elif key == ord("c"):
            cv2.destroyAllWindows()
            break

    # Select RoI
    x, y, w, h = cv2.selectROI("Select RoI", frame1)

    # Create masked videos
    writer1 = cv2.VideoWriter(newPath1, fourcc, fps, (w, h))
    writer2 = cv2.VideoWriter(newPath2, fourcc, fps, (w, h))

    # Mask each frame for both videos
    print("Masking videos...")

    while True:
        ret, frame = vid1.read()
        if not ret:
            break

        roiFrame = frame[y : y + h, x : x + w]
        writer1.write(roiFrame)

    while True:
        ret, frame = vid2.read()
        if not ret:
            break

        roiFrame = frame[y : y + h, x : x + w]
        writer2.write(roiFrame)

    # Release resources
    vid1.release()
    vid2.release()
    writer1.release()
    writer2.release()
    cv2.destroyAllWindows()

    return newPath1, newPath2


def process(coldPath, hotPath, savePath="temp/", method="PCT", options={}):
    """Processes two videos and returns the path to the plot of the results

    Args:
        coldPath (str): Path to the cold video
        hotPath (str): Path to the hot video
        savePath (str, optional): Folder path to put results in. Defaults to "temp/".
        method (str, optional): The processing method to use. Defaults to "PCT". Can be ["PCT", "SPCT"]
        options (dict, optional): Optional arguments for processing. Defaults to {}.

    Returns:
        plotPath: Path to the plot of the results
    """
    print("Creating mask...")
    coldMask, hotMask = createMask(coldPath, hotPath)

    print("Reading videos...")
    cold, hot = readVideo(coldMask), readVideo(hotMask)

    print("Creating folder...")
    try:
        os.mkdir(savePath)
    except FileExistsError:
        pass

    if method == "PCT":
        print("Performing PCT...")
        numEOFs = int(options.get("numEOFs", 6))
        normMethod = options.get("normMethod", "col-wise standardize")

        print(normMethod)

        EOFs = PCT(hot, normMethod, numEOFs)

        print("Displaying results...")
        plotPath = display(EOFs, [f"EOF{i}" for i in range(numEOFs)], savePath)

        print("Saving EOFs...")
        for i, EOF in enumerate(EOFs):
            np.save(savePath + f"EOF{i}.npy", EOF)

        return plotPath
    elif method == "SPCT":
        print("Performing SPCT...")
        numEOFs = int(options.get("numEOFs", 6))
        normMethod = options.get("normMethod", "col-wise mean reduction")
        EOFs = SPCT(hot, normMethod, numEOFs)

        print("Displaying results...")
        plotPath = display(EOFs, [f"EOF{i}" for i in range(numEOFs)], savePath)

        print("Saving EOFs...")
        for i, EOF in enumerate(EOFs):
            np.save(savePath + f"EOF{i}.npy", EOF)

        return plotPath
