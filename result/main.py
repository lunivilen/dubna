from result.remove_outliers import remove_outliers
from PyQt6.QtWidgets import QApplication
from visualizing import MainWindow
from smoothing import smoothing
from save_data import save_data
from get_data import get_data
from cleaning import cleaning
from merging import merging
import sys

result = []
result.append(get_data("data/event0.txt"))
result.append(cleaning(list(map(lambda x: x.copy(), result[0]))))
result.append(merging(list(map(lambda x: x.copy(), result[1])),
                      allowable_angle=160,
                      allowable_length=700,
                      allowable_distance=35))
result.append(remove_outliers(list(map(lambda x: x.copy(), result[2]))))
result.append(smoothing(list(map(lambda x: x.copy(), result[3])), smooth_scale=200))
# save_data(tracks)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plot = MainWindow(result, False)
    plot.show()
    sys.exit(app.exec())
