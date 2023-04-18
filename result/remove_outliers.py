from merging import get_vector, get_vector_length
from scipy.interpolate import RBFInterpolator, BSpline
from time import time
import pandas as pd
import numpy as np
from scipy import interpolate


def remove_outliers(tracks: list):
    print("Start removing emissions")
    start = time()
    for track in tracks:
        df = pd.DataFrame(track, columns=[0, 1, 2, 3, 4, 5, 6, 7, 8])
        tck, u = interpolate.splprep(np.array([df[1], df[2], df[3]]), s=3)
    print(f"Removing emissions completed in {time() - start} seconds")
    return tracks
