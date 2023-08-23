from collections import defaultdict
from cleaning_old_longer import sort_hits
import re


# Берёт из всех параметров хита, только нужные
def clear_temp(temp, x_index, y_index, z_index, hit_index):
    x = temp[x_index]
    y = temp[y_index]
    z = temp[z_index]
    hit_id = temp[hit_index]
    return [hit_id, x, y, z]


def get_tracks_data(path) -> list:
    track_id = 0
    tracks = []
    x_index = 1
    y_index = 2
    z_index = 3
    hit_index = 0
    amount_parameters_in_hit = 0

    with open(path) as f:
        for i in f:
            if 'format' in i:
                data_format = re.findall(r'\((.*)\)', i)[0].split(', ')
                amount_parameters_in_hit = len(data_format)
                x_index = data_format.index('x')
                y_index = data_format.index('y')
                z_index = data_format.index('z')
                hit_index = data_format.index('hit-index')
                continue

            if not amount_parameters_in_hit:
                print("The first line in the data file must be of the format: x, y, z, etc.")
                exit()

            temp = []
            tracks.append([])
            mas = i.split(", ")
            amount_characteristics = 0
            j = 0
            while j < len(mas):
                if amount_characteristics != amount_parameters_in_hit:
                    temp.append(float(mas[j]))
                    amount_characteristics += 1
                    j += 1
                else:
                    tracks[track_id].append(clear_temp(temp, x_index, y_index, z_index, hit_index))
                    temp = []
                    amount_characteristics = 0
            if j == len(mas):
                tracks[track_id].append(clear_temp(temp, x_index, y_index, z_index, hit_index))
            track_id += 1
    return tracks


def get_hits_data(path) -> dict:
    hits = defaultdict(list)
    with open(path) as f:
        for i in f:
            if 'format' in i:
                continue

            hit = list(map(float, i.split(", ")))
            hits[str(hit[3])].append(hit[:3])

    for id_track in hits.keys():
        hits[id_track] = sort_hits(hits[id_track])
    return hits


def get_hits_data_for_validation(path) -> list:
    hits = []
    with open(path) as f:
        for i in f:
            if 'format' in i:
                continue

            hit = list(map(float, i.split(", ")))
            hits.append(hit)
    return hits
