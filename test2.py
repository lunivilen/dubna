import sys

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QWidget
import pyqtgraph.opengl as gl
import numpy as np

graphs_1 = gl.GLGraphItem()
graphs_1.setData(nodePositions=np.array([[1, 2, 3], [6, 5, 4]]))

graphs_2 = gl.GLGraphItem()
graphs_2.setData(nodePositions=np.array([[-1, 2, -3], [6, -5, 4]]),
                 nodeColor=QColor(Qt.GlobalColor.green))


class MainWindow(gl.GLViewWidget):
    def __init__(self, axes):
        self.ax = axes
        super().__init__()

    def keyPressEvent(self, key: QtGui.QKeyEvent) -> None:
        try:
            match key.text():
                case '1':
                    self.addItem(self.ax)
                    self.removeItem(graphs_2)
                case '2':
                    self.addItem(graphs_2)
                    self.removeItem(graphs_1)
                case '3':
                    self.clear()
        except ValueError:
            print(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = gl.GLViewWidget()
    demo.show()
    sys.exit(app.exec())
