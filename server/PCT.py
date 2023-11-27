import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import SparsePCA


def PCT(video, normMethod="col-wise standardize", EOFs=2):
    """Performs Principal Component Thermography (PCT) on a video. The video is first normalized, then the EOFs are computed using Singular Value Decomposition (SVD).

    Args:
        video (np.ndarray): Numpy array of the frames in grayscale. Shape: (n_frames, height, width)
        normMethod (str, optional): The normalization method. Defaults to "col-wise standardize". Can be ["col-wise standardize", "row-wise standardize", "mean reduction"]
        EOFs (int, optional): Number of EOFs to return. Defaults to 2.

    Returns:
        [EOF_i]: List of EOFs. Each EOF is a numpy array of shape (height, width)
    """
    # Reshape video to (height*width, n_frames)
    n, h, w = video.shape[:3]
    A = video.reshape(n, -1).T

    # Normalize
    if normMethod == "col-wise standardize":
        mean = np.mean(A, axis=0)
        std = np.std(A, axis=0)
        epsilon = 1e-5
        A = (A - mean) / (std + epsilon)
    elif normMethod == "row-wise standardize":
        for i, row in enumerate(A):
            A[i] = (row - np.mean(row)) / np.std(row)
    elif normMethod == "mean reduction":
        A = A - np.mean(A)

    # Perform Singular Value Decomposition (SVD)
    U, _, _ = np.linalg.svd(A, full_matrices=False)

    # Return EOFs
    return [U[:, i].reshape(h, w) for i in range(EOFs)]


def SPCT(video, normMethod="col-wise mean reduction", EOFs=2):
    """Performs Sparse Principal Component Thermography (SPCT) on a video. The video is first normalized, then the EOFs are computed using Sparse PCA.

    Args:
        video (np.ndarray): Numpy array of the frames in grayscale. Shape: (n_frames, height, width)
        normMethod (str, optional): The normalization method. Defaults to "col-wise mean reduction". Can be ["col-wise mean reduction", "col-wise standardize", "row-wise standardize", "mean reduction"]
        EOFs (int, optional): Number of EOFs to return. Defaults to 2.

    Returns:
        [EOF_i]: List of EOFs. Each EOF is a numpy array of shape (height, width)
    """
    # Reshape video to (height*width, n_frames)
    n, h, w = video.shape[:3]
    A = video.reshape(n, -1).T

    # Normalize
    if normMethod == "col-wise mean reduction":
        A = A - np.mean(A, axis=0)
    elif normMethod == "col-wise standardize":
        mean = np.mean(A, axis=0)
        std = np.std(A, axis=0)
        epsilon = 1e-5
        A = (A - mean) / (std + epsilon)
    elif normMethod == "row-wise standardize":
        for i, row in enumerate(A):
            A[i] = (row - np.mean(row)) / np.std(row)
    elif normMethod == "mean reduction":
        A = A - np.mean(A)

    # Perform Sparse PCA
    spca = SparsePCA(n_components=EOFs, alpha=0.5)
    res = spca.fit_transform(A)

    return [res[:, i].reshape(h, w) for i in range(EOFs)]
