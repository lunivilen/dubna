import os
from get_data import get_tracks_data
import matplotlib.pyplot as plt


path = r"data\selecting_pri_and_sec"
file_list = os.listdir(path)

chi2 = []

for file_name in file_list:
    if 'prototracks' in file_name:
        tracks = get_tracks_data(rf"{path}\{file_name}", 10)
        chi2.extend([track[0][-2] for track in tracks])
        break

plt.hist(chi2, bins=20)
plt.xlabel('ch2')
plt.ylabel('Частота')
plt.title(path)
plt.show()
