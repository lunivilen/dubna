from copy import deepcopy
from itertools import chain

def crop_list(listA):
    new_list = deepcopy(listA)
    for i in range(len(new_list)):
        new_list[i] = new_list[i][0]
    return new_list

def get_tracks_from_hits(hits):
    # trimmed_hits = crop_list(hits)
    trimmed_hits = sorted(hits, key=lambda x: x[3], reverse=False)
    tracks_from_hits = {}
    track = []
    for i in range(1, len(trimmed_hits)):
        if trimmed_hits[i-1][3] == trimmed_hits[i][3] and trimmed_hits[i-1][3] != trimmed_hits[-1][3]:
            track.append(trimmed_hits[i-1])
        elif trimmed_hits[i-1][3] != trimmed_hits[-1][3]: 
            tracks_from_hits[int(trimmed_hits[i-1][3])] = track
            track = []
        elif trimmed_hits[i-1][3] == trimmed_hits[i][3] and trimmed_hits[i-1][3] == trimmed_hits[-1][3]:
            tracks_from_hits[int(trimmed_hits[i][3])] = track
            tracks_from_hits[int(trimmed_hits[i][3])].append(trimmed_hits[i-1])
    return tracks_from_hits

def get_hit_chars(tracks, hits):
    tracks_hits = {}
    track_ids = []
    for i in range(len(tracks)): 
        tracks_hits[i] = []
        track_ids.append([])
        track_id = []
        for hit in tracks[i]:
            tracks_hits[i].append(hits[int(hit[3])]) #gets track's hits characteristics from hits list 
            track_id.append(int(hits[int(hit[3])][3]))
        track_ids[i] = max(set(track_id), key = track_id.count) 
    return tracks_hits, track_ids

def get_real_matched_tracks(matched_ids, hits, n):
    matched_id = deepcopy(matched_ids)
    real_tracks = get_tracks_from_hits(hits)
    real_matched = []
    for i in range(1, len(matched_ids)-1):
        if matched_ids[i-1][1] == matched_ids[i][1] and matched_ids[i-1][0]=='False' and matched_ids[i][0]=='True': 
            matched_id.remove(matched_ids[i-1])
    for i in range(len(list(real_tracks.values()))):
        if len(list(real_tracks.values())[i])+1 >= n: 
            real_matched.append(list(real_tracks.values())[i])
    return real_matched

def get_matched_tracks(tracks, hits, n, ratio=0.5):
    matched_ids = []
    tracks_matched = []
    used_ids = []
    tracks_hits, track_ids = get_hit_chars(tracks, hits)
    for i in range(len(tracks)):
        flat=list(chain.from_iterable(tracks_hits[i]))
        if len(tracks[i]) > n and (track_ids[i] not in used_ids) and flat.count(max(set(flat), key = flat.count)) / len(tracks_hits[i]) > ratio:
            tracks_matched.append(tracks[i])
            used_ids.append(track_ids[i])
            matched_ids.append(['True', track_ids[i]]) #int(max(set(flat), key = flat.count))
        elif (['False', track_ids[i]] not in matched_ids) and (['True', track_ids[i]] not in matched_ids): matched_ids.append(['False', track_ids[i]])
    real_matched = get_real_matched_tracks(matched_ids, hits, n)
    return tracks_matched, real_matched

def get_efficiency(tracks, hits, min_length, ratio=0.5): #min_length - minimal length of a track 
    #hits should have 4 characterisrics, fourth being track_id
    tracks_matched, real_matched = get_matched_tracks(tracks, hits, min_length, ratio)
    n_matched = len(tracks_matched)
    n_real = len(real_matched)
    print('Number of reco tracks:', n_matched)
    print('Number of real selected tracks:', n_real)
    efficiency = n_matched / n_real
    return efficiency


# def add_track_number(tracks):
#     tracks_numbd = deepcopy(tracks)
#     for i in range(len(tracks_numbd)):
#         for track in tracks_numbd[i]:
#             track.insert(0, i)
#     return tracks_numbd

# def get_unique_tracks_and_coords(tracks,
#                                  track_id_loc: int,
#                                  cut_start: int,
#                                  cut_end: int):       # track_id_loc - location of a track_id in a list,track_id_loc= 0 for tracks,track_id_loc= 3 for hits
#     tracks_numbd = add_track_number(tracks)
#     tracks_rec = []                                   # cut_start:cut_end - cut of y and z coords; for tracks cut_start=2, cut_end=4; for hits cut_start=1, cut_end=3
#     tracks_y_z = []
#     for i in range(len(tracks_numbd)):
#         for j in range(len(tracks_numbd[i])):
#             tracks_rec.append(tracks_numbd[i][j][track_id_loc])
#             tracks_y_z.append(tracks_numbd[i][j][cut_start:cut_end])
#     return list(set(tracks_rec)), tracks_y_z                         # [0] - unique tracks, [1] - y, z coords of all tracks


