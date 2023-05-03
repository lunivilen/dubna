from merging import get_vector, get_vector_length
from scipy.interpolate import RBFInterpolator, BSpline
from time import time
import pandas as pd
import numpy as np


def remove_emissions(tracks: list):
    print("Start removing emissions")
    start = time()
    allowable_height = 2
    for track in tracks:
        i = 0
        while i < len(track) - 2:
            vec_1 = get_vector(track[i], track[i + 1])
            vec_2 = get_vector(track[i], track[i + 2])
            vec_3 = get_vector(track[i + 1], track[i + 2])
            # s = area_of_triangle(vec_1, vec_3)
            s = 0
            bottom = get_vector_length(vec_2)
            if s / bottom > allowable_height:
                track.remove(track[i + 2])
            else:
                i += 1
    print(f"Removing emissions completed in {time() - start} seconds")
    return tracks
