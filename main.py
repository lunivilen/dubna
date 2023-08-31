from copy import deepcopy

from PyQt6.QtWidgets import QApplication

from fast_cleaning import fast_cleaning_merge, fast_cleaning_longer
from get_data import *
from cleaning_old_longer import cleaning_old_longer, sort_hits_old
from cleaning_old_merge import cleaning_old_merge
from merging import merging

from validation import get_efficiency, get_fake_rate

import sys

from visualizing import MainWindow

result = [get_tracks_data("data/event_0_prototracks.txt", "data/event_0_space_points.txt")]
hits = get_hits_data("data/event_0_space_points.txt")
hits_for_validation = get_hits_data_for_validation("data/event_0_space_points.txt")
track_id_list = get_track_id("data/event_0_trackIds.txt")

# result.append(cleaning_old_longer(deepcopy(result[0])))
# result.append(cleaning_old_merge(deepcopy(result[0])))
# result.append(fast_cleaning_merge(deepcopy(result[0])))
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
    # print(f"Эффективность {i}: {get_efficiency(result[i], hits_for_validation, track_id_list)}")
    print(f"Рассчёт фейков {i}: {get_fake_rate(result[i], hits_for_validation, track_id_list)}\n\n")

    if len(result[i][0][0]) > 3:
        for track_id in range(len(result[i])):
            for hit_id in range(len(result[i][track_id])):
                result[i][track_id][hit_id] = result[i][track_id][hit_id][1:]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plot = MainWindow(result, hits)
    plot.show()
    sys.exit(app.exec())
