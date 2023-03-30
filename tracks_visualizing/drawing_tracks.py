import pyqtgraph.opengl as gl
import PyQt6.QtWidgets as pqg
from PyQt6 import QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
import numpy as np
import pandas as pd


def merge_tracks(track_one, track_two):
    for point in track_two:
        if point not in track_one:
            track_one.append(point)
    return track_one


def separate_tracks(track_one, track_two):
    for point in track_two:
        if point in track_one:
            track_two.remove(point)
    return track_one


# Breaking tracks from a file into separate hits
tracks = []
track_id = 0
with open("event0.txt", "r") as f:
    for i in f:
        temp = []
        tracks.append([])
        mas = i.split(", ")
        amount_characteristics = 0
        j = 0
        while j < len(mas):
            if amount_characteristics != 10:
                if amount_characteristics != 0 and amount_characteristics != 1 and len(temp) < 3:
                    temp.append(float(mas[j]))
                amount_characteristics += 1
                j += 1
            else:
                tracks[track_id].append(temp)
                temp = []
                amount_characteristics = 0
        if j == amount_characteristics:
            tracks[track_id].append(temp)
            temp = []
            amount_characteristics = 0
        track_id += 1

# Merge same tracks
similarity_factor = 0.4
i = 0
while i < len(tracks):
    j = 0
    while j < len(tracks):
        if tracks[j][0] in tracks[i] and i != j:
            temp_mas = tracks[i] + tracks[j]
            if len(temp_mas) / len(np.unique(temp_mas)) > similarity_factor:
                tracks[i] = merge_tracks(tracks[i], tracks[j])
                tracks.pop(j)
                j -= 1
        j += 1
    i += 1

# Separate tracks
i = 0
while i < len(tracks):
    for j in range(i + 1, len(tracks)):
        tracks[i] = separate_tracks(tracks[i], tracks[j])
    if not tracks[i] or len(tracks[i]) < 5:
        tracks.pop(i)
    else:
        i += 1

# Sort the hits in the correct order after merge
for i in range(len(tracks)):
    df = pd.DataFrame(tracks[i], columns=[0, 1, 2])
    scatter_x = df[0].max() - df[0].min()
    scatter_y = df[1].max() - df[1].min()
    scatter_z = df[2].max() - df[2].min()
    if max(scatter_x, scatter_y, scatter_z) == scatter_x:
        tracks[i] = list(df.sort_values(0, ascending=True).values)
    elif max(scatter_x, scatter_y, scatter_z) == scatter_y:
        tracks[i] = list(df.sort_values(1, ascending=True).values)
    else:
        tracks[i] = list(df.sort_values(2, ascending=True).values)
    tracks[i] = list(map(list, tracks[i]))

# Discard all characteristics of hits, except for coordinates
tracks_new = []
indexes = []
i = 0
j = 0
for track_num in range(len(tracks)):
    indexes.append([])
    for hit in range(len(tracks[track_num])):
        x = tracks[track_num][hit][0]
        y = tracks[track_num][hit][1]
        z = tracks[track_num][hit][2]
        tracks_new.append([x, y, z])
        if hit != 0 and hit != len(tracks[track_num]) - 1:
            indexes[i].extend([j, j])
        else:
            indexes[i].extend([j])
        j += 1
    i += 1

# Looking for the maximum track length
max_len = -1
for i in range(len(indexes)):
    if len(indexes[i]) > max_len:
        max_len = len(indexes[i])

# Reducing all tracks to the largest size by creating loops
# It is necessary, because to build a single large graph, all subgraphs must form a matrix,
# which means that the length of all subgraphs must be the same
for i in range(len(indexes)):
    if len(indexes[i]) < max_len:
        indexes[i].extend([indexes[i][-1]] * (max_len - len(indexes[i])))

# Draw a graph
app = pqg.QApplication([])
plot = gl.GLViewWidget()
graphs = gl.GLGraphItem()
graphs.setData(nodePositions=np.array(tracks_new),
               edges=np.array(indexes),
               edgeColor=QColor(Qt.GlobalColor.green),
               nodeColor=QColor(Qt.GlobalColor.gray),
               edgeWidth=2)
plot.addItem(graphs)

# for i in range(len(tracks)):
#     if len(tracks[i]) < 3:
#         text = gl.GLTextItem(text=str(i), parentItem=graphs, pos=tracks[i][-1], font=QtGui.QFont('Helvetica', 8),
#                              color=QColor(Qt.GlobalColor.red))
#         plot.addItem(text)
plot.show()

if __name__ == '__main__':
    app.exec()
