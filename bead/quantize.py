import numpy as np
import os
from skimage import io
from sklearn.cluster import KMeans


def quantize_image(project):
    num_colors = project.properties.quantize_colors
    print(f'Quantizing image -- Name:{project.name}; Colors:{num_colors}')

    if not os.path.exists(project.orig_path):
        raise ValueError(f'File missing -- Path:{project.orig_path}')

    original = io.imread(project.orig_path)
    width = original.shape[0]
    height = original.shape[1]
    pixels = width * height
    channels = original.shape[2]

    # Make sure this is <= the number of pixels
    num_colors = min(pixels, num_colors)

    arr = original.reshape((-1, channels))
    kmeans = KMeans(n_clusters=num_colors, random_state=42).fit(arr)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_
    less_colors = centers[labels].reshape(original.shape).astype('uint8')

    print(f'Writing -- Path:{project.quantized_path}')
    io.imsave(project.quantized_path, less_colors)
