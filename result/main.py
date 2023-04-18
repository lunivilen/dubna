import sys

from PyQt6.QtWidgets import QApplication
import pyqtgraph.opengl as gl
from remove_outliers import remove_outliers
from visualizing import visualizing, MainWindow
from save_data import save_data
from get_data import get_data
from cleaning import cleaning
from merging import merging

result = [get_data("data/event0.txt")]
tracks = cleaning(result[0].copy())
result.append(tracks)
# result.append(merging(result[1],
#                       allowable_angle=160,
#                       allowable_length=700,
#                       allowable_distance=35))
# result.append(remove_outliers(result[2]))
# save_data(tracks)
data = visualizing(result, show_tracks_indexes=False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plot = MainWindow(data)
    plot.show()
    sys.exit(app.exec())
