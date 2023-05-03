import pyqtgraph.opengl as gl
import PyQt6.QtWidgets as pqg
from PyQt6 import QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
import numpy as np


def visualizing(tracks: list, show_tracks_indexes=False):
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

    if show_tracks_indexes:
        for i in range(len(tracks)):
            text = gl.GLTextItem(text=str(i), parentItem=graphs, pos=tracks[i][0][1:4],
                                 font=QtGui.QFont('Helvetica', 14), color=QColor(Qt.GlobalColor.red))
            plot.addItem(text)
    plot.show()

    return app
