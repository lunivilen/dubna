from merging import get_distance
from itertools import chain
from copy import deepcopy

def add_track_number(tracks):
    tracks_numbd = deepcopy(tracks)
    for i in range(len(tracks_numbd)):
        for track in tracks_numbd[i]:
            track.insert(0, i)
    return tracks_numbd


def get_unique_tracks_and_coords(tracks,
                                 track_id_loc: int,
                                 cut_start: int,
                                 cut_end: int):       # track_id_loc - location of a track_id in a list,track_id_loc= 0 for tracks,track_id_loc= 3 for hits
    tracks_numbd = add_track_number(tracks)
    tracks_rec = []                                   # cut_start:cut_end - cut of y and z coords; for tracks cut_start=2, cut_end=4; for hits cut_start=1, cut_end=3
    tracks_y_z = []
    for i in range(len(tracks_numbd)):
        for j in range(len(tracks_numbd[i])):
            tracks_rec.append(tracks_numbd[i][j][track_id_loc])
            tracks_y_z.append(tracks_numbd[i][j][cut_start:cut_end])
    return list(set(tracks_rec)), tracks_y_z                         # [0] - unique tracks, [1] - y, z coords of all tracks

def get_selected_tracks(tracks):
    selected_tracks = []
    for i in range(len(tracks)):
        selected_tracks.append([])
        for track in tracks[i]:
            if len(track) > 5: #and get_distance(track, [0,0,200]) < 1000:
                selected_tracks[i].append(track)
    return selected_tracks

def crop_list(listA):
    new_list = deepcopy(listA)
    for i in range(len(new_list)):
        new_list[i] = new_list[i][0]
    return new_list

def get_tracks_from_hits(hits):
    trimmed_hits = crop_list(hits)
    trimmed_hits = sorted(trimmed_hits, key=lambda x: x[2], reverse=False)
    tracks_from_hits = [[]]
    # for i in range(len(trimmed_hits)):
    #     tracks_from_hits.append([])
    for i in range(1, len(trimmed_hits)):
        if trimmed_hits[i-1][2] == trimmed_hits[i][2]:
            tracks_from_hits[i-1].append(trimmed_hits[i-1])
        else: tracks_from_hits.append([])
    return 

def get_simple_efficiency(tracks, hits):
    n_reco = len(get_unique_tracks_and_coords(tracks, 0, 1, 3)[0])
    n_real = len(get_unique_tracks_and_coords(hits, 4, 1, 3)[0])
    efficiency = n_reco / n_real
    print('Number of reco tracks:', n_reco)
    print('Number of real tracks:', n_real)
    print('Efficiency value is:', efficiency)
    return efficiency

def get_matched_tracks(tracks, hits):
    tracks_hits = {}
    tracks_matched = []
    # tracks = get_selected_tracks(tracks)
    #
    for i in range(len(tracks)):
        tracks_hits[i] = []
        for hit in tracks[i]:
            tracks_hits[i].append(hits[int(hit[3])][0])
        flat=list(chain.from_iterable(tracks_hits[i]))
        if flat.count(max(set(flat), key = flat.count)) / len(tracks_hits[i]) > 0.5:
            tracks_matched.append(tracks[i])
    return tracks_matched

def get_efficiency(tracks, hits):
    # n_selected_reco = len(get_unique_tracks_and_coords(get_selected_tracks(tracks), 3, 0, 2)[0])
    # print(len(tracks))
    n_matched = len(get_matched_tracks(tracks, hits))
    # n_matched = len(get_unique_tracks_and_coords(get_matched_tracks(tracks, hits), 0, 1, 3)[0])
    n_real = len(get_unique_tracks_and_coords(hits, 4, 1, 3)[0])
    n_selected_real = len(get_unique_tracks_and_coords(hits, 4, 1, 3)[0])
    # n_selected_real = len(get_unique_tracks_and_coords(get_tracks_from_hits(hits), 3, 1, 3)[0])
    # n_matched = len(get_unique_tracks_and_coords(get_matched_tracks(tracks), 0, 2, 4)[0])
    print('Number of reco tracks:', n_matched)
    print('Number of real selected tracks:', n_real)
    efficiency = n_matched / n_real
    return efficiency

def get_real_tracks(tracks, hits): 
    real_tracks = []
    for i in range(len(get_unique_tracks_and_coords(hits, 2, 0, 2)[1])):
        if get_unique_tracks_and_coords(hits, 2, 0, 2)[1][i] in get_unique_tracks_and_coords(tracks, 0, 2, 4)[1]:
            print(i)
            real_tracks.append(get_unique_tracks_and_coords(hits, 2, 0, 2)[1][i])
    return real_tracks


def get_purity(tracks, hits):
    purity = len(get_real_tracks(tracks, hits)) / len(get_unique_tracks_and_coords(tracks, 0, 2, 4)[1])
    print('Purity value is:', purity)
    return purity