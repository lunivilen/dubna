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
    trimmed_hits = sorted(trimmed_hits, key=lambda x: x[3], reverse=False)
    tracks_from_hits = {}
    track = []
    # for i in range(len(trimmed_hits)):
    #     tracks_from_hits.append([])

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

def get_simple_efficiency(tracks, hits):
    n_reco = len(get_unique_tracks_and_coords(tracks, 0, 1, 3)[0])
    n_real = len(get_unique_tracks_and_coords(hits, 4, 1, 3)[0])
    efficiency = n_reco / n_real
    print('Number of reco tracks:', n_reco)
    print('Number of real tracks:', n_real)
    print('Efficiency value is:', efficiency)
    return efficiency

def get_matched_ids(tracks, hits, n, ratio=0.5):  #n - minimal length of a track
    tracks_hits = {}
    tracks_matched = []
    tracks_from_hits = {}
    tracks_from_hits = get_tracks_from_hits(hits)
    # tracks = get_selected_tracks(tracks)
    track_ids = []
    for i in range(len(tracks)): 
        tracks_hits[i] = []
        track_ids.append([])
        track_id = []
        for hit in tracks[i]:
            tracks_hits[i].append(hits[int(hit[3])][0]) #gets track's hits characteristics from hits list 
            track_id.append(int(hits[int(hit[3])][0][3]))
        track_ids[i] = max(set(track_id), key = track_id.count)  
        flat = list(chain.from_iterable(tracks_hits[i]))   
        # flat = [val for val in flat if val.is_integer() and val >= 0]
        flat.count(max(set(flat), key = flat.count)) #checks how many hits are a part of the same original track len(tracks_hits[i])
    used_ids = []
    matched_ids = []
    for i in range(len(tracks)):
        if len(tracks[i]) > n and (track_ids[i] not in used_ids) and flat.count(max(set(flat), key = flat.count)) / len(tracks[i]) > ratio:
            tracks_matched.append(tracks[i])
            used_ids.append(track_ids[i])
            matched_ids.append(['True', i])
        else: matched_ids.append(['False', i])
    return matched_ids

def get_matched_tracks(tracks, hits, n, ratio=0.5):
    tracks_hits = {}
    tracks_matched = []
    used_ids = []
    track_ids = []
    matched_ids = []
    # tracks = get_selected_tracks(tracks)
    #
    for i in range(len(tracks)): 
        tracks_hits[i] = []
        track_ids.append([])
        track_id = []
        for hit in tracks[i]:
            tracks_hits[i].append(hits[int(hit[3])][0]) #gets track's hits characteristics from hits list 
            track_id.append(int(hits[int(hit[3])][0][3]))
        track_ids[i] = max(set(track_id), key = track_id.count) 

    for i in range(len(tracks)):
        tracks_hits[i] = []
        for hit in tracks[i]:
            tracks_hits[i].append(hits[int(hit[3])][0])
            track_id.append(int(hits[int(hit[3])][0][3]))
        
        flat=list(chain.from_iterable(tracks_hits[i]))
        if len(tracks[i]) >= n and (track_ids[i] not in used_ids) and flat.count(max(set(flat), key = flat.count)) / len(tracks_hits[i]) >= ratio:
            tracks_matched.append(tracks[i])
            used_ids.append(track_ids[i])
            matched_ids.append(['True', track_ids[i]]) #int(max(set(flat), key = flat.count))
        elif (['False', track_ids[i]] not in matched_ids) and (['True', track_ids[i]] not in matched_ids): matched_ids.append(['False', track_ids[i]])
    
    matched_id = deepcopy(matched_ids)
    for i in range(1, len(matched_ids)-1):
        if matched_ids[i-1][1] == matched_ids[i][1] and matched_ids[i-1][0]=='False' and matched_ids[i][0]=='True': 
            matched_id.remove(matched_ids[i-1])

    real_tracks = get_tracks_from_hits(hits)
    real_matched = []

    for i in range(len(list(real_tracks.values()))):
        if len(list(real_tracks.values())[i])+1 >= n: 
            real_matched.append(list(real_tracks.values())[i])
    
    real_length = []
    for i in range(len(list(real_tracks.items()))):
        real_length.append([list(real_tracks.items())[i][0], len(list(real_tracks.items())[i][1])])

    return tracks_matched, real_matched

with open(r'matched_ids.txt', 'w') as fp:
    for item in matched_id:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')

with open(r'real_lengths.txt', 'w') as fp:
    for item in real_length:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')

def get_efficiency(tracks, hits, min_length, ratio=0.5): #min_length - minimal length of a track 
    # n_selected_reco = len(get_unique_tracks_and_coords(get_selected_tracks(tracks), 3, 0, 2)[0])
    # print(len(tracks))
    tracks_matched, real_matched = get_matched_tracks(tracks, hits, min_length, ratio)
    n_matched = len(tracks_matched)
    # n_matched = len(get_unique_tracks_and_coords(get_matched_tracks(tracks, hits), 0, 1, 3)[0])
    n_real = len(real_matched)
    # n_selected_real = len(get_unique_tracks_and_coords(hits, 4, 1, 3)[0])
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