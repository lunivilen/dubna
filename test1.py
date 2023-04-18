import keyboard
from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QThread, QMetaObject, QRunnable, QThreadPool
import pyqtgraph.opengl as gl
from time import sleep
from multiprocessing import Process

from PyQt6.QtWidgets import QProgressBar, QVBoxLayout, QWidget, QPushButton, QApplication


class ProcessRunnable(QRunnable):
    def __init__(self, target, args):
        QRunnable.__init__(self)
        self.t = target
        self.a = args

    def run(self):
        self.t(*self.a)

    def start(self):
        QThreadPool.globalInstance().start(self)


def test(key):
    print(1)


class MyWidget(QWidget):
    keyPressed = QtCore.pyqtSignal(int)

    def keyPressEvent(self, event):
        super(MyWidget, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())
        self.keyPressed.connect(self.press)

    def press(self, key):
        self.p = ProcessRunnable(target=test, args=[key])
        self.p.start()


class App(gl.GLViewWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        # vbox = QVBoxLayout()
        # self.pBar = QProgressBar()
        # self.pBar.setMaximum(10)
        # vbox.addWidget(self.pBar)
        # self.button = QPushButton("Start")
        # vbox.addWidget(self.button)

    def init_ui(self):
        self.ax = gl.GLAxisItem()
        self.addItem(self.ax)
        # self.thread = ProcessRunnable(target=test)
        # self.thread.start()


if __name__ == '__main__':
    app = QApplication([])
    win = App()
    win.show()
    app.exec()
