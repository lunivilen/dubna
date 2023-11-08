from copy import deepcopy

from PyQt6.QtWidgets import QApplication
from analyse.validation import calc_characteristics
from post_processing.cleaning.graph_cleaning import graph_merging, graph_cleaning
from data_processing.parse_data import *
from post_processing.cleaning.direct_cleaning import direct_cleaning, sort_hits_old
from post_processing.merging.direct_merging import direct_merging
from post_processing.merging.merging import merge_og

import sys

from visualizing import MainWindow

result = [get_tracks_data("data/event_672_prototracks.txt", "data/event_672_points.txt")]
track_dict = get_hits_data("data/event_672_points.txt")
hit_list = get_hits_data_for_validation("data/event_672_points.txt")
track_id_dict = get_track_id("data/event_0_trackIds.txt")

# result.append(direct_cleaning(deepcopy(result[0])))
# result.append(direct_merging(deepcopy(result[0])))
result.append(graph_merging(deepcopy(result[0])))
# result.append(graph_cleaning(deepcopy(result[0])))
result.append(merge_og(deepcopy(result[1]),
                       allowable_angle=160,
                       allowable_length=700,
                       allowable_distance=35))
# result.append(remove_outliers(deepcopy(result[2])))
# result.append(smoothing(deepcopy(result[3]), smooth_scale=150))
# save_data(tracks)

# result.append(get_tracks_data("data/event672_mpdroot.txt"))

# Computation efficiency
for i in range(len(result)):
    characteristic_dict = calc_characteristics(result[i], hit_list, track_dict, track_id_dict)

    for characteristic, value in characteristic_dict.items():
        print(f"{characteristic}: {value}\n")

    if len(result[i][0][0]) > 3:
        for track_id in range(len(result[i])):
            for hit_id in range(len(result[i][track_id])):
                result[i][track_id][hit_id] = result[i][track_id][hit_id][1:]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plot = MainWindow(result, track_dict)
    plot.show()
    sys.exit(app.exec())
