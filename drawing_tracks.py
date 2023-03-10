import pyqtgraph.opengl as gl
import PyQt6.QtWidgets as pqg
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
import numpy as np

# Breaking tracks from a file into separate hits
tracks = []
track_id = 0
with open("event.txt", "r") as f:
    for i in f:
        temp = []
        tracks.append([])
        mas = i.split(", ")
        t = 0
        j = 0
        while j < len(mas):
            if t != 9:
                temp.append(float(mas[j]))
                t += 1
                j += 1
            else:
                tracks[track_id].append(temp)
                temp = []
                t = 0
        if j == t:
            tracks[track_id].append(temp)
            temp = []
            t = 0
        track_id += 1

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
        indexes[i].append(j)
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
               edgeWidth=2)
plot.addItem(graphs)

plot.show()

if __name__ == '__main__':
    app.exec()
