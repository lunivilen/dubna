import time

from remove_outliers import remove_outliers
from PyQt6.QtWidgets import QApplication
from fast_cleaning import process_tracks
from visualizing import MainWindow
from smoothing import smoothing
from save_data import save_data
from get_data import get_tracks_data, get_hits_data
from cleaning import cleaning
from merging import merging

import sys

result = []
result.append(get_tracks_data("data/event672_1.txt", 11))
hits = get_hits_data("data/event672_1_hits.txt")

# tracks_dict, tracks_to_unite, graph_to_separate = process_tracks(result[0])
result.append(cleaning(list(map(lambda x: x.copy(), result[0]))))
result.append(merging(list(map(lambda x: x.copy(), result[1])),
                      allowable_angle=160,
                      allowable_length=700,
                      allowable_distance=35))
result.append(remove_outliers(list(map(lambda x: x.copy(), result[2]))))
result.append(smoothing(list(map(lambda x: x.copy(), result[3])), smooth_scale=150))
# save_data(tracks)


# Remove hit_index from raw data
for track_id in range(len(result[0])):
    for hit_id in range(len(result[0][track_id])):
        result[0][track_id][hit_id] = result[0][track_id][hit_id][1:]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plot = MainWindow(result, hits)
    plot.show()
    sys.exit(app.exec())
