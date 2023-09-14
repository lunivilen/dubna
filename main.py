from copy import deepcopy

from PyQt6.QtWidgets import QApplication
from validation import calc_characteristics
from fast_cleaning import fast_merging_logical, fast_cleaning_longer
from get_data import *
from cleaning_longer import cleaning_longer, sort_hits_old
from merging_logical import merging_logical

import sys

from visualizing import MainWindow

result = [get_tracks_data("data/event_0_prototracks.txt", "data/event_0_space_points.txt")]
track_dict = get_hits_data("data/event_0_space_points.txt")
hit_list = get_hits_data_for_validation("data/event_0_space_points.txt")
secondary_track_list = get_secondary_track("data/event_0_trackIds.txt")

# result.append(cleaning_longer(deepcopy(result[0])))
# result.append(merging_logical(deepcopy(result[0])))
# result.append(fast_merging_logical(deepcopy(result[0])))
# result.append(fast_cleaning_longer(deepcopy(result[0])))
# result.append(merging(deepcopy(result[1]),
#                       allowable_angle=160,
#                       allowable_length=700,
#                       allowable_distance=35))
# result.append(remove_outliers(deepcopy(result[2])))
# result.append(smoothing(deepcopy(result[3]), smooth_scale=150))
# save_data(tracks)

# result.append(get_tracks_data("data/event672_mpdroot.txt"))

# Computation efficiency
for i in range(len(result)):
    characteristic_dict = calc_characteristics(result[i], hit_list, track_dict, secondary_track_list)

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
