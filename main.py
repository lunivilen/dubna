from post_processing.cleaning.graph_cleaning import graph_merging, graph_cleaning
from post_processing.cleaning.direct_cleaning import direct_cleaning
from post_processing.merging.direct_merging import direct_merging
from analyse.validation import calc_characteristics
from analyse.visualizing import MainWindow
from data_processing.parse_data import *
from PyQt6.QtWidgets import QApplication
from copy import deepcopy
import sys

result = {
    "raw": get_tracks_data("data/tracks_data/event_0_prototracks.txt", "data/tracks_data/event_0_space_points.txt")}

hit_list = get_hits_data_for_validation("data/tracks_data/event_0_space_points.txt")
track_id_dict = get_track_id("data/tracks_data/event_0_trackIds.txt")
track_dict = get_hits_data("data/tracks_data/event_0_space_points.txt", track_id_dict)

result["PWS"] = direct_cleaning(deepcopy(result.get("raw")))
result["PWM"] = direct_merging(deepcopy(result.get("raw")))
result["PGS"] = graph_merging(deepcopy(result.get("raw")))
result["PGM"] = graph_cleaning(deepcopy(result.get("raw")))

# Computation efficiency
for i in range(len(result)):
    characteristic_dict = calc_characteristics(result[i], hit_list, track_dict, track_id_dict)

    for characteristic, value in characteristic_dict.items():
        print(f"{characteristic}: {value}\n")

    # Remove hit indexes for visualizing
    if len(result[i][0][0]) > 3:
        for track_id in range(len(result[i])):
            for hit_id in range(len(result[i][track_id])):
                result[i][track_id][hit_id] = result[i][track_id][hit_id][1:]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plot = MainWindow(result, track_dict)
    plot.show()
    sys.exit(app.exec())
