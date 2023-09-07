from copy import deepcopy
from itertools import chain


def crop_list(listA):
    new_list = deepcopy(listA)
    for i in range(len(new_list)):
        new_list[i] = new_list[i][0]
    return new_list


def get_tracks_from_hits(hits):
    trimmed_hits = sorted(hits, key=lambda x: x[3], reverse=False)
    tracks_from_hits = {}
    track = []
    for i in range(1, len(trimmed_hits)):
        if trimmed_hits[i - 1][3] == trimmed_hits[i][3] and trimmed_hits[i - 1][3] != trimmed_hits[-1][3]:
            track.append(trimmed_hits[i - 1])
        elif trimmed_hits[i - 1][3] != trimmed_hits[-1][3]:
            tracks_from_hits[int(trimmed_hits[i - 1][3])] = track
            track = []
        elif trimmed_hits[i - 1][3] == trimmed_hits[i][3] and trimmed_hits[i - 1][3] == trimmed_hits[-1][3]:
            tracks_from_hits[int(trimmed_hits[i][3])] = track
            tracks_from_hits[int(trimmed_hits[i][3])].append(trimmed_hits[i - 1])
    return tracks_from_hits


def get_hit_chars(tracks, hits):
    tracks_hits = {}
    track_ids = []
    for i in range(len(tracks)):
        tracks_hits[i] = []
        track_id = []
        for hit in tracks[i]:
            original_hit = hits[int(hit[0])]
            tracks_hits[i].append(original_hit)  # gets track's hits characteristics from hits list
            track_id.append(int(original_hit[3]))
        track_ids.append(max(track_id, key=track_id.count))
    return tracks_hits, track_ids


def get_real_matched_tracks(hits, n):
    real_tracks = get_tracks_from_hits(hits)
    real_matched = []
    for i in range(len(list(real_tracks.values()))):
        if len(list(real_tracks.values())[i]) >= n:
            real_matched.append(list(real_tracks.values())[i])
    return real_matched


def get_matched_tracks(tracks, hits, n, ratio=0.5):
    tracks_matched = []
    used_ids = []
    tracks_hits, track_ids = get_hit_chars(tracks, hits)
    for i in range(len(tracks)):
        flat = list(chain.from_iterable(tracks_hits[i]))
        if len(tracks[i]) >= n and (track_ids[i] not in used_ids) and flat.count(max(flat, key=flat.count)) / len(
                tracks_hits[i]) > ratio:
            tracks_matched.append(tracks[i])
            used_ids.append(track_ids[i])
    return tracks_matched


def get_fake_tracks(tracks, hits, n=9, ratio=0.5):
    fake_tracks = []
    tracks_hits = get_hit_chars(tracks, hits)[0]
    for i in range(len(tracks)):
        flat = list(chain.from_iterable(tracks_hits[i]))
        if len(tracks[i]) >= n and flat.count(max(set(flat), key=flat.count)) / len(tracks_hits[i]) < ratio:
            fake_tracks.append(tracks[i])
    return fake_tracks


def get_efficiency(tracks, hits, min_length, ratio=0.5):  # min_length - minimal length of a track
    # hits should have 4 characterisrics, fourth being track_id
    tracks_matched = get_matched_tracks(tracks, hits, min_length, ratio)
    real_matched = get_real_matched_tracks(hits, min_length)
    n_matched = len(tracks_matched)
    n_real = len(real_matched)
    print('Number of reco tracks:', n_matched)
    print('Number of real selected tracks:', n_real)
    if not n_real:
        return 0
    efficiency = n_matched / n_real
    return efficiency


def get_selected_real(tracks, min_length):
    selected_tracks = []
    for track in tracks:
        if len(track) >= min_length:
            selected_tracks.append(track)
    return selected_tracks


def get_fake_rate(tracks, hits, min_length=20, ratio=0.5):
    fake_tracks = get_fake_tracks(tracks, hits, min_length, ratio)
    n_fake = len(fake_tracks)
    n_real = len(get_selected_real(tracks, min_length))
    print('Number of fake tracks:', n_fake)
    print('Number of real selected tracks:', n_real)
    if not n_real:
        return 0
    fake_rate = n_fake / n_real
    return fake_rate


def get_purity(tracks, hits, min_length=20, ratio=0.5):
    tracks_matched = get_matched_tracks(tracks, hits, min_length, ratio)
    n_matched = len(tracks_matched)
    n_reco = len(tracks)
    if not n_reco:
        return 0
    purity = n_matched / n_reco
    print('Number of real reco tracks:', n_matched)
    print('Number of reco tracks:', n_reco)
    return purity


def get_duplicated_tracks(tracks, hits, n=20, ratio=0.5):
    tracks_duplicated = []
    used_ids = []
    tracks_hits, track_ids = get_hit_chars(tracks, hits)
    for i in range(len(tracks)):
        flat = list(chain.from_iterable(tracks_hits[i]))
        if len(tracks[i]) >= n and (track_ids[i] not in used_ids) and flat.count(max(set(flat), key=flat.count)) / len(
                tracks_hits[i]) >= ratio:
            used_ids.append(track_ids[i])
        elif len(tracks[i]) >= n and (track_ids[i] in used_ids) and flat.count(max(set(flat), key=flat.count)) / len(
                tracks_hits[i]) >= ratio:
            tracks_duplicated.append(tracks[i])
    return tracks_duplicated


def get_duplication_rate(tracks, hits, min_length=9, ratio=0.5):
    tracks_duplicated = get_duplicated_tracks(tracks, hits, min_length, ratio)
    n_duplicated = len(tracks_duplicated)
    n_reco = len(tracks)
    if not n_reco:
        return 0
    duplication_rate = n_duplicated / n_reco
    print('Number of real reco tracks:', n_duplicated)
    print('Number of reco tracks:', n_reco)
    return duplication_rate

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
