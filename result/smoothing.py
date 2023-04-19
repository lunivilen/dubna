from scipy import interpolate
from time import time
import pandas as pd
import numpy as np


def smoothing(tracks: list, smooth_scale):
    print("Start smoothing")
    start = time()
    for track_id in range(len(tracks)):
        if len(tracks[track_id]) < 6:
            continue
        df = pd.DataFrame(tracks[track_id], columns=[0, 1, 2, 3, 4, 5, 6, 7, 8])
        x = np.array(df[1])
        y = np.array(df[2])
        z = np.array(df[3])
        tck = interpolate.splprep([x, y, z], k=1, s=smooth_scale)[0]
        u_fine = np.linspace(0, 1, len(tracks[track_id]))
        new_x, new_y, new_z = interpolate.splev(u_fine, tck)
        df[1], df[2], df[3] = new_x, new_y, new_z
        tracks[track_id] = df.values.tolist()
    print(f"Smoothing completed in {time() - start} seconds")
    return tracks
