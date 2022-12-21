import numpy as np

# get the region of interest
def roi(data: np.ndarray, ROI_IMAGE_HEIGHT, ROI_IMAGE_WIDTH, ROI_IMAGE_OFFSET_X, ROI_IMAGE_OFFSET_Y):
    shape = data.shape
    resize_shap = (ROI_IMAGE_HEIGHT, ROI_IMAGE_WIDTH, shape[2])
    dtype = data.dtype
    res = np.ndarray(resize_shap, dtype)
    for h in range(ROI_IMAGE_OFFSET_Y, ROI_IMAGE_HEIGHT + ROI_IMAGE_OFFSET_Y):
        for w in range(ROI_IMAGE_OFFSET_X, ROI_IMAGE_WIDTH + ROI_IMAGE_OFFSET_X):
            res[h - ROI_IMAGE_OFFSET_Y][w - ROI_IMAGE_OFFSET_X] = data[h][w]
    return res
