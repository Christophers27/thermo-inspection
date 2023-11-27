import numpy as np
import cv2
import matplotlib.pyplot as plt


def normalize(x):
    """Normalizes a numpy array to the range [0, 255]

    Args:
        x (np.ndarray): Numpy array

    Returns:
        res: Normalized numpy array
    """
    res = np.zeros(x.shape)
    cv2.normalize(x, res, 0, 255, cv2.NORM_MINMAX)
    return res.astype(np.uint8)


def display(arrays, names, title):
    """Displays a list of numpy arrays as images in a grid

    Args:
        arrays (np.ndarray list): List of numpy arrays
        names (str list): List of names for the arrays
        title (str): Title of the plot and folder to save the plot in

    Returns:
        path: Path to the plot
    """
    n = len(arrays)

    if n > 2:
        rows = n // 2
        cols = 2
        fig, axes = plt.subplots(rows, cols)
        fig.suptitle(title)  # No this is not a typo

        images = []
        for i, arr in enumerate(arrays):
            row = i // cols
            col = i % cols

            images.append(axes[row, col].imshow(normalize(arr), cmap="jet"))
            axes[row, col].label_outer()
            axes[row, col].set_title(names[i])

        fig.colorbar(images[0], ax=axes, orientation="horizontal", fraction=0.1)
        plt.savefig(title + "plot.png")
        return title + "plot.png"
    elif n == 2:
        fig, axes = plt.subplots(1, 2)
        fig.suptitle(title)

        images = []
        for i, arr in enumerate(arrays):
            images.append(axes[i].imshow(normalize(arr), cmap="jet"))
            axes[i].label_outer()
            axes[i].set_title(names[i])

        fig.colorbar(images[0], ax=axes, orientation="horizontal", fraction=0.1)
        plt.savefig(title + "plot.png")
        return title + "plot.png"
    else:
        plt.imshow(arrays[0], cmap="jet")
        plt.title(title)
        plt.colorbar()

        plt.savefig(title + "plot.png")
        return title + "plot.png"
