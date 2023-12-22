import cv2
import numpy as np
import os

from PCT import PCT, SPCT
from display import display


def createMask2(path1, path2, isOneVideo=False):
    if not isOneVideo:
        vid1, vid2 = cv2.VideoCapture(path1), cv2.VideoCapture(path2)
        cold, hot = [], []

        # Create window to display frame and select RoI
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

        # Get RoI coordinates
        x, y, w, h = cv2.selectROI("Select RoI", frame1)

        # Mask each frame for both videos
        while True:
            ret, frame = vid1.read()
            if not ret:
                break

            cold.append(cv2.cvtColor(frame[y : y + h, x : x + w], cv2.COLOR_BGR2GRAY))

        while True:
            ret, frame = vid2.read()
            if not ret:
                break

            hot.append(cv2.cvtColor(frame[y : y + h, x : x + w], cv2.COLOR_BGR2GRAY))

        vid1.release()
        vid2.release()

        return np.stack(cold, axis=0), np.stack(hot, axis=0)
    else:
        vid = cv2.VideoCapture(path1)
        cold, hot = [], []
        fps = vid.get(cv2.CAP_PROP_FPS)

        # Create window to display frame and select RoI
        ret, frame = vid.read()
        while True:
            cv2.imshow("Press 's' to skip frame, 'c' to choose RoI", frame)
            key = cv2.waitKey(0) & 0xFF
            if key == ord("s"):
                cv2.destroyAllWindows()
                ret, frame = vid.read()

                if not ret:
                    raise Exception("Video 1 ended before selecting RoI")

                continue
            elif key == ord("c"):
                cv2.destroyAllWindows()
                break

        # Get RoI coordinates
        x, y, w, h = cv2.selectROI("Select RoI", frame)

        # Mask each frame for both videos. Assumes that the first ten seconds
        # is the cold video and the rest is hot
        while True:
            ret, frame = vid.read()
            if not ret:
                break

            if len(cold) < 10 * fps:
                cold.append(cv2.cvtColor(frame[y : y + h, x : x + w], cv2.COLOR_BGR2GRAY))
            else:
                hot.append(cv2.cvtColor(frame[y : y + h, x : x + w], cv2.COLOR_BGR2GRAY))

        vid.release()

        return np.stack(cold, axis=0), np.stack(hot, axis=0)


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
    print("Reading videos...")
    cold, hot = createMask2(coldPath, hotPath, coldPath is None)

    print("Creating folder...")
    try:
        os.mkdir(savePath)
    except FileExistsError:
        pass

    if method == "PCT":
        print("Performing PCT...")
        numEOFs = int(options.get("numEOFs", 6))
        normMethod = options.get("normMethod", "col-wise standardize")

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
