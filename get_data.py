from collections import defaultdict
from cleaning_longer import sort_hits
import re


def get_tracks_data(track_path, hit_path) -> list:
    hit_list = get_hits_data_for_validation(hit_path)
    tracks = []
    track_id = 0
    amount_parameters_in_hit = 0

    with open(track_path) as f:
        for i in f:
            if 'format' in i:
                data_format = re.findall(r'\((.*)\)', i)[0].split(', ')
                amount_parameters_in_hit = len(data_format)
                continue

            if not amount_parameters_in_hit:
                print("Wrong format")
                exit()

            temp = []
            tracks.append([])
            mas = i.split(", ")
            amount_characteristics = 0
            j = 0
            while j < len(mas) or temp:
                if amount_characteristics != amount_parameters_in_hit:
                    temp.append(float(mas[j]))
                    amount_characteristics += 1
                    j += 1
                else:
                    hit_index = int(temp[0])
                    hit_params = hit_list[hit_index][:-1]
                    hit_params.insert(0, hit_index)
                    tracks[track_id].append(hit_params)
                    temp = []
                    amount_characteristics = 0
            track_id += 1
    return tracks


def get_hits_data(path_hits) -> dict:
    hits = defaultdict(list)
    with open(path_hits) as f:
        for i in f:
            if 'format' in i:
                continue

            hit = list(map(float, i.split(", ")))
            hits[int(hit[3])].append(hit[:3])

    for id_track in hits.keys():
        hits[id_track] = sort_hits(hits[id_track])
    return hits


def get_hits_data_for_validation(path_hits) -> list:
    hits = []
    with open(path_hits) as f:
        for i in f:
            if 'format' in i:
                continue

            hit = list(map(float, i.split(", ")))
            hits.append(hit)
    return hits


def get_secondary_track(path) -> list:
    secondary_track_list = []
    with open(path) as f:
        for i in f:
            if 'format' in i:
                continue

            info = list(map(int, i.split(", ")))
            if not info[1]:
                secondary_track_list.append(info[0])
    return secondary_track_list
