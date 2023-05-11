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
        for track_id in range(len(tracks)):
            indexes.append([])
            for hit_id in range(len(tracks[track_id])):
                tracks_new.append(tracks[track_id][hit_id])
                if hit_id == 0:
                    head_indexes.append(tracks[track_id][hit_id])

                if hit_id != 0 and hit_id != len(tracks[track_id]) - 1:
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
    def __init__(self, tracks_data: list, hits_data: dict):
        super().__init__()
        self.stage = -1
        self.tracks_data = data_preparation_for_visualizing(tracks_data)
        self.simulation_data = data_preparation_for_visualizing([list(hits_data.values())])[0]
        self.is_indexes_showed = False
        self.is_simulation_data_showed = False
        self.graph = gl.GLGraphItem()
        self.show_tracks()

    def keyPressEvent(self, key: QtGui.QKeyEvent) -> None:
        try:
            pressed_key = key.text()
            if self.is_simulation_data_showed:
                match pressed_key:
                    case "-":
                        self.is_simulation_data_showed = False
                        self.show_tracks()
            else:
                match pressed_key:
                    case "-":
                        self.is_simulation_data_showed = True
                        self.is_indexes_showed = False
                        self.show_tracks(is_simulations_data=True)
                    case "0":
                        self.is_indexes_showed = not self.is_indexes_showed
                        self.show_tracks()
                    case _:
                        self.stage = int(key.text()) - 1
                        self.show_tracks()
        except ValueError:
            pass

    def show_tracks(self, is_simulations_data=False):
        try:
            # Get node positions and edges for tracks
            if is_simulations_data:
                node_positions = np.array(self.simulation_data[0])
                edges_index = np.array(self.simulation_data[1])
                colour = QColor(Qt.GlobalColor.cyan)
                self.clear()
            else:
                node_positions = np.array(self.tracks_data[self.stage][0])
                edges_index = np.array(self.tracks_data[self.stage][1])
                colour = QColor(Qt.GlobalColor.green)
                self.clear()
                if self.is_simulation_data_showed:
                    self.show_tracks(is_simulations_data=True)

            # Create graph object
            self.graph.setData(nodePositions=node_positions,
                               edges=edges_index,
                               edgeColor=colour,
                               nodeColor=QColor(Qt.GlobalColor.gray),
                               edgeWidth=2)
            self.addItem(self.graph)

            if self.is_indexes_showed:
                self.show_indexes()

        except IndexError:
            pass

    def show_indexes(self):
        for i in range(len(self.tracks_data[self.stage][2])):
            text = gl.GLTextItem(text=str(i),
                                 pos=self.tracks_data[self.stage][2][i],
                                 font=QtGui.QFont('Helvetica', 14),
                                 color=QColor(Qt.GlobalColor.red))
            self.addItem(text)
