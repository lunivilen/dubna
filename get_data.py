from collections import defaultdict
from cleaning import sort_hits


def get_tracks_data(path, amount_parameters_in_hit) -> list:
    track_id = 0
    tracks = []
    with open(path) as f:
        for i in f:
            temp = []
            tracks.append([])
            mas = i.split(", ")
            amount_characteristics = 0
            j = 0
            while j < len(mas):
                if amount_characteristics != amount_parameters_in_hit:
                    if amount_characteristics != 0:
                        temp.append(float(mas[j]))
                    amount_characteristics += 1
                    j += 1
                else:
                    tracks[track_id].append(temp[:4])
                    temp = []
                    amount_characteristics = 0
            if j == len(mas):
                tracks[track_id].append(temp[:4])
            track_id += 1
    return tracks


def get_hits_data(path) -> dict:
    hits = defaultdict(list)
    with open(path) as f:
        for i in f:
            hit = list(map(float, i.split(", ")))
            hits[str(hit[3])].append(hit[:3])

    for id_track in hits.keys():
        hits[id_track] = sort_hits(hits[id_track])
    return hits
