import pyqtgraph.opengl as gl
import PyQt6.QtWidgets as pqg
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
import numpy as np

# Breaking data from a file into separate hits
hits = []
with open("../data/event2_original.txt", "r") as f:
    for i in f:
        mas = i.split(", ")
        hits.append([mas[0], mas[1], mas[2]])

# Draw the hits
app = pqg.QApplication([])
plot = gl.GLViewWidget()
graphs = gl.GLGraphItem()
graphs.setData(nodePositions=np.array(hits),
               edgeColor=QColor(Qt.GlobalColor.green),
               edgeWidth=2)
plot.addItem(graphs)

plot.show()

if __name__ == '__main__':
    app.exec()
