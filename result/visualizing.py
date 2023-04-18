import sys

import pyqtgraph.opengl as gl
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
import numpy as np


def data_preparation(data):
    new_data = []
    for tracks in data:
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
        new_data.append([tracks_new, indexes])
    return new_data


def visualizing(tracks_data: list, show_tracks_indexes=False):
    # Preparing the data
    data = data_preparation(tracks_data)

    # Draw a graph
    # if show_tracks_indexes:
    #     for i in range(len(tracks)):
    #         text = gl.GLTextItem(text=str(i), parentItem=graphs, pos=tracks[i][0][1:4],
    #                              font=QtGui.QFont('Helvetica', 14), color=QColor(Qt.GlobalColor.red))
    #         plot.addItem(text)
    return data


class MainWindow(gl.GLViewWidget):
    def __init__(self, tracks_data):
        super().__init__()
        self.data = tracks_data
        self.graph = gl.GLGraphItem(nodePositions=np.array(self.data[-1][0]),
                                    edges=np.array(self.data[-1][1]),
                                    edgeColor=QColor(Qt.GlobalColor.green),
                                    nodeColor=QColor(Qt.GlobalColor.gray),
                                    edgeWidth=2)
        self.addItem(self.graph)

    def keyPressEvent(self, key: QtGui.QKeyEvent) -> None:
        key = key.text()
        try:
            node_positions = np.array(self.data[int(key) - 1][0])
            edges_index = np.array(self.data[int(key) - 1][1])
            self.clear()
            self.graph.setData(nodePositions=node_positions, edges=edges_index)
            self.addItem(self.graph)
        except (IndexError, ValueError):
            pass
