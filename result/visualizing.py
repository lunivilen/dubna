import pyqtgraph.opengl as gl
from PyQt6 import QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
import numpy as np


def data_preparation_for_visualizing(data):
    new_data = []
    for tracks in data:
        # Discard all characteristics of hits, except for coordinates
        tracks_new = []
        indexes = []
        head_indexes = []
        i = 0
        j = 0
        for track_num in range(len(tracks)):
            indexes.append([])
            for hit in range(len(tracks[track_num])):
                x = tracks[track_num][hit][1]
                y = tracks[track_num][hit][2]
                z = tracks[track_num][hit][3]
                tracks_new.append([x, y, z])
                if hit == 0:
                    head_indexes.append([x, y, z])

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
        new_data.append([tracks_new, indexes, head_indexes])
    return new_data


class MainWindow(gl.GLViewWidget):
    def __init__(self, tracks_data, show_tracks_indexes=False):
        super().__init__()
        self.data = data_preparation_for_visualizing(tracks_data)
        self.show_tracks_indexes = show_tracks_indexes
        self.graph = gl.GLGraphItem()
        self.show_tracks(-1)

    def keyPressEvent(self, key: QtGui.QKeyEvent) -> None:
        try:
            self.show_tracks(int(key.text()) - 1)
        except ValueError:
            pass

    def show_tracks(self, stage: int):
        try:
            node_positions = np.array(self.data[stage][0])
            edges_index = np.array(self.data[stage][1])
            self.clear()
            self.graph.setData(nodePositions=node_positions,
                               edges=edges_index,
                               edgeColor=QColor(Qt.GlobalColor.green),
                               nodeColor=QColor(Qt.GlobalColor.gray),
                               edgeWidth=2)
            self.addItem(self.graph)

            # Indexes
            if self.show_tracks_indexes:
                for i in range(len(self.data[stage][2])):
                    text = gl.GLTextItem(text=str(i), pos=self.data[stage][2][i],
                                         font=QtGui.QFont('Helvetica', 14), color=QColor(Qt.GlobalColor.red))
                    self.addItem(text)
        except IndexError:
            pass
