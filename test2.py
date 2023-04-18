from multiprocessing import Process
import keyboard
from time import sleep
import pyqtgraph.opengl as gl
import PyQt6.QtWidgets as pqg
from PyQt6 import QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QMetaObject
import numpy as np


class App(pqg.QApplication):
    def __init__(self):
        pass


app = App()
plot = gl.GLViewWidget()
graphs = gl.GLAxisItem()
plot.addItem(graphs)
plot.show()


def test():
    while True:
        if keyboard.is_pressed('q'):
            # QMetaObject.invokeMethod(app, )
            pass


if __name__ == '__main__':
    t = Process(target=test)
    t.start()
    app.exec()
