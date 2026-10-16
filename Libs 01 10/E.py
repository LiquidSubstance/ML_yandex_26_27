import numpy as np

def count_unique_colors(image):
    image = np.reshape(image, (-1, 3))
    return len(np.unique(image, axis=0))

