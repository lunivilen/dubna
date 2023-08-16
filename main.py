from PyQt6.QtWidgets import QApplication

from fast_cleaning import fast_cleaning
from get_data import *
from cleaning_new import cleaning_new, sort_hits_old
from cleaning_old import cleaning_old
from merging import merging

from validation import get_efficiency, get_fake_rate

import sys

from visualizing import MainWindow

result = []
result.append(get_tracks_data("data/selecting_pri_and_sec/event_0_prototracks.txt"))
hits = get_hits_data("data/selecting_pri_and_sec/event_0_hits.txt")

hits_for_validation = get_hits_data_for_validation("data/selecting_pri_and_sec/event_0_hits.txt")

result.append(cleaning_old(list(map(lambda x: x.copy(), result[0]))))
result.append(cleaning_new(list(map(lambda x: x.copy(), result[0]))))
merged_tracks, longer_tracks = fast_cleaning(list(map(lambda x: x.copy(), result[0])))
result.append(merged_tracks)
result.append(longer_tracks)
# result.append(merging(list(map(lambda x: x.copy(), result[1])),
#                       allowable_angle=160,
#                       allowable_length=700,
#                       allowable_distance=35))
# result.append(remove_outliers(list(map(lambda x: x.copy(), result[2]))))
# result.append(smoothing(list(map(lambda x: x.copy(), result[3])), smooth_scale=150))
# save_data(tracks)

result.append(get_tracks_data("data/event672_mpdroot.txt", 10))

# Computation efficiency
for i in range(len(result)):
    print(f"Эффективность {i}: {get_efficiency(result[i], hits_for_validation, min_length=4)}")
    print(f"Рассчёт фейков {i}: {get_fake_rate(result[i], hits_for_validation)}\n\n")

    if len(result[i][0][0]) > 3:
        for track_id in range(len(result[i])):
            for hit_id in range(len(result[i][track_id])):
                result[i][track_id][hit_id] = result[i][track_id][hit_id][1:]

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     plot = MainWindow(result, hits)
#     plot.show()
#     sys.exit(app.exec())
