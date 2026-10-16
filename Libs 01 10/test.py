import numpy as np

def clip_features(features, lower, upper):
    return np.clip(features, lower, upper)