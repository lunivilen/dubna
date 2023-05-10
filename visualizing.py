from PyQt6.QtGui import QColor
import pyqtgraph.opengl as gl
from PyQt6.QtCore import Qt
from PyQt6 import QtGui
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
    def __init__(self, tracks_data):
        super().__init__()
        self.stage = -1
        self.data = data_preparation_for_visualizing(tracks_data)
        self.is_indexes_showed = False
        self.graph = gl.GLGraphItem()
        self.show_tracks()

    def keyPressEvent(self, key: QtGui.QKeyEvent) -> None:
        try:
            if key.text() == '0' and self.is_indexes_showed:
                self.is_indexes_showed = False
                self.show_tracks()
            elif key.text() == '0':
                self.is_indexes_showed = True
                self.show_indexes()
            else:
                self.stage = int(key.text()) - 1
                self.show_tracks()
        except ValueError:
            pass

    def show_tracks(self):
        try:
            node_positions = np.array(self.data[self.stage][0])
            edges_index = np.array(self.data[self.stage][1])
            self.clear()
            self.graph.setData(nodePositions=node_positions,
                               edges=edges_index,
                               edgeColor=QColor(Qt.GlobalColor.green),
                               nodeColor=QColor(Qt.GlobalColor.gray),
                               edgeWidth=2)
            self.addItem(self.graph)

            if self.is_indexes_showed:
                self.show_indexes()
        except IndexError:
            pass

    def show_indexes(self):
        for i in range(len(self.data[self.stage][2])):
            text = gl.GLTextItem(text=str(i), pos=self.data[self.stage][2][i],
                                 font=QtGui.QFont('Helvetica', 14), color=QColor(Qt.GlobalColor.red))
            self.addItem(text)
