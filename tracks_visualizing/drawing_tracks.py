import pyqtgraph.opengl as gl
import PyQt6.QtWidgets as pqg
from PyQt6 import QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
import numpy as np
import pandas as pd
from time import time
import math


def merge_tracks(track_one, track_two):
    similarity_factor = 0.5
    temp_mas = track_one + track_two
    unique = list(np.unique(temp_mas))
    difference = len(temp_mas) - len(unique)
    if difference / len(track_two) > similarity_factor:
        return unique, 1
    elif difference / len(track_one) > similarity_factor:
        return unique, 2
    else:
        return [], 0


def separate_tracks(track_one, track_two):
    for point in track_two:
        if point in track_one:
            track_two.remove(point)
    return track_one


start = time()
# Breaking tracks from a file into separate hits
tracks = []
track_id = 0
# ================= Get data from file =================
with open("event0.txt", "r") as f:
    for i in f:
        temp = []
        tracks.append([])
        mas = i.split(", ")
        amount_characteristics = 0
        j = 0
        while j < len(mas):
            if amount_characteristics != 10:
                if amount_characteristics != 0:
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

# ================= Cleaning =================
print(f"Before merging there are {len(tracks)} tracks")

# Speed up
hits = {}
for i in range(len(tracks)):
    for j in range(len(tracks[i])):
        s = tracks[i][j][0]
        hits[s] = tracks[i][j]
        tracks[i][j] = s

print("Starting the first stage of merging")
start = time()
# The first merging stage
i = 0
while i < len(tracks):
    j = i + 1
    while j < len(tracks) and i < len(tracks):
        if tracks[j][0] in tracks[i] and i != j:
            merged_track, number = merge_tracks(tracks[i], tracks[j])
            if number == 1:
                tracks[i] = merged_track
                tracks.pop(j)
                j -= 1
            elif number == 2:
                tracks[j] = merged_track
                tracks.pop(i)
                i -= 1
                break
        j += 1
    i += 1

print(f"The first stage of merging completed in {time() - start} seconds")
print("Starting the second stage of merging")
start = time()
i = 0
# The second merging stage
while i < len(tracks):
    j = i + 1
    while j < len(tracks) and i < len(tracks):
        if i != j:
            merged_track, number = merge_tracks(tracks[i], tracks[j])
            if number == 1:
                tracks[i] = merged_track
                tracks.pop(j)
                j -= 1
            elif number == 2:
                tracks[j] = merged_track
                tracks.pop(i)
                i -= 1
                break
        j += 1
    i += 1

print(f"The second stage of merging completed in {time() - start} seconds")
print("Starting split tracks")
start = time()

# Separate tracks
i = 0
while i < len(tracks):
    for j in range(i + 1, len(tracks)):
        tracks[i] = separate_tracks(tracks[i], tracks[j])
    if not tracks[i]:
        tracks.pop(i)
    else:
        i += 1
print(f"Track splitting completed in {time() - start} seconds")

# Return to x,y,z and etc.
for i in range(len(tracks)):
    for j in range(len(tracks[i])):
        tracks[i][j] = hits[tracks[i][j]]

print("Staring sorting the points in the track")
start = time()

# Sort the hits in the correct order after merge
for i in range(len(tracks)):
    df = pd.DataFrame(tracks[i], columns=[0, 1, 2, 3, 4, 5, 6, 7, 8])
    scatter_x = df[1].max() - df[1].min()
    scatter_y = df[2].max() - df[2].min()
    scatter_z = df[3].max() - df[3].min()
    if max(scatter_x, scatter_y, scatter_z) == scatter_x:
        tracks[i] = list(df.sort_values(1, ascending=True).values)
    elif max(scatter_x, scatter_y, scatter_z) == scatter_y:
        tracks[i] = list(df.sort_values(2, ascending=True).values)
    else:
        tracks[i] = list(df.sort_values(3, ascending=True).values)
    tracks[i] = list(map(list, tracks[i]))

print(f"Sorting completed in {time() - start} seconds")
print(f"After merging there are {len(tracks)} tracks")

# Saving new tracks
with open("new_event.txt", "w") as f:
    for track in tracks:
        for hit in track:
            for characteristic in hit:
                f.write(str(characteristic) + ", ")
        f.write("\n")
# ================= Visualizing =================
# Discard all characteristics of hits, except for coordinates
tracks_new = []
indexes = []
i = 0
j = 0
for track_num in range(len(tracks)):
    indexes.append([])
    for hit in range(len(tracks[track_num])):
        x = tracks[track_num][hit][1]
        y = tracks[track_num][hit][2]
        z = tracks[track_num][hit][3]
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
plot.show()

if __name__ == '__main__':
    app.exec()
