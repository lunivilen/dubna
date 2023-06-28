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
from validation import get_simple_efficiency
from validation import get_efficiency
from fast_cleaning import tracks_separation
from fast_cleaning import unite_tracks
from fast_cleaning import fast_cleaning

import sys

result = []
result.append(get_tracks_data("data/event_672_prototracks_acts.txt", 10))
hits = get_hits_data("data/event_672_hits_acts.txt")

result[0][1]
hits[0]

tracks_mpd = get_tracks_data("data/event_672_tracks_mpd.txt", 10)
hits_mpd = get_hits_data("data/event_672_hits_mpd.txt")

# tracks_dict, tracks_to_unite, graph_to_separate = process_tracks(result[0])

# result.append(fast_cleaning(list(map(lambda x: x.copy(), result[0]))))
result.append(cleaning(list(map(lambda x: x.copy(), result[0]))))
# result.append(unite_tracks(list(map(lambda x: x.copy(), result[0]))))
# len(result[1][1])

# for i in range(len(result[1])):
#     for j in range(len(result[1][i])):
#         if len(result[1][i][j]) > 4: print(i, j)

result.append(merging(list(map(lambda x: x.copy(), result[1])),
                      allowable_angle=160,
                      allowable_length=700,
                      allowable_distance=35))
# result[1][1][1][3]
# len(result[1])
# result.append(remove_outliers(list(map(lambda x: x.copy(), result[2]))))
# result.append(smoothing(list(map(lambda x: x.copy(), result[3])), smooth_scale=150))
# # save_data(tracks)
# hits[0][0]
# 933/971

tracks_mpd[1]
result[1][1]
len(result[2])
hits[1:5]
result[2][1:5]

hits_test = [[[56, 68, 87, 0]], [[45, 78, 87, 0]], [[24, 67, 85, 1]], [[76, 23, 53, 2]], [[86, 54, 34, 3]]]
tracks_test = [[[67, 45, 87, 0], [0, 75, 78, 1]], [[98, 54, 87, 2]], [[56,87,45,3]], [[76,98,76,4]]]

# print(get_simple_efficiency(result[1], hits))

print(get_efficiency(tracks_test, hits_test))
print(get_efficiency(result[2], hits))
print(get_efficiency(tracks_mpd, hits_mpd))

# print(get_purity(tracks, hits))
# tracks = remove_outliers(tracks)
# save_data(tracks)
# app = visualizing(tracks, show_tracks_indexes=False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plot = MainWindow(result, hits)
    plot.show()
    sys.exit(app.exec())