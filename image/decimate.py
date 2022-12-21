import numpy as np

# get the upper left corner pixel every 2X2 array
def decimate(data:np.ndarray):
    shape = data.shape
    resize_shap = (int(shape[0] / 2), int(shape[1] / 2), shape[2])
    dtype = data.dtype
    res = np.ndarray(resize_shap, dtype)
    for h in range(0, shape[0], 2):
        for w in range(0, shape[1], 2):
            res[int(h / 2)][int(w / 2)] = data[h][w]
    return res