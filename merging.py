from cleaning_old import sort_hits_old
from time import time
import numpy as np
import math
from copy import deepcopy


def get_vector(hit_1, hit_2):
    return np.array([hit_2[0] - hit_1[0], hit_2[1] - hit_1[1], hit_2[2] - hit_1[2]])

def get_track_angle(v):
    return np.abs(np.rad2deg(np.arctan(v[1]/v[0])))

def get_distance(track, circle = [0, 0, 3]): #returns the distance between a track and a circle
    #circle = [x1, y1, r]
    #might be used to eliminate tracks that do not start from the starting cylinder
    return np.abs(np.sqrt((track[0]-circle[0])**2+(track[1]-circle[1])**2)-circle[2])

def angle_between_vec(v1, v2):
    dot_pr = v1.dot(v2)
    norms = np.linalg.norm(v1) * np.linalg.norm(v2)
    return np.rad2deg(np.arccos(dot_pr / norms))

def get_vector_length(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)

def co_directed(track_one, track_two):
    normal = get_vector(track_one[0], track_two[-1])
    reverse = get_vector(track_one[0], track_two[0])
    return get_vector_length(reverse) > get_vector_length(normal)

def average_vec(hits):
    vec = np.array([hits[2][0] - hits[0][0], hits[2][1] - hits[0][1], hits[2][2] - hits[0][2]])
    return vec * 2 / 3

def distance_to_line(m0, m1, m_check):
    ab = m0 - m1
    ac = m_check - m1
    d = np.linalg.norm(np.cross(ab, ac)) / np.linalg.norm(ab)
    return d

def angle_sorting(tracks:list):
    start = time()
    print("Sorting start")
    tracks_start = {}
    tracks_end = {}
    for i in range(len(tracks)):
        if len(tracks[i]) > 1:
            vec_start = get_vector(tracks[i][0][1:4], tracks[i][1][1:4])
            vec_end = get_vector(tracks[i][len(tracks[i])-2][1:4], tracks[i][len(tracks[i])-1][1:4])

            tracks_start[i] = [tracks[i], get_track_angle(vec_start)]
            tracks_end[i] = [tracks[i], get_track_angle(vec_end)]
        else: 
            tracks_start[i] = [tracks[i], 1]
            tracks_end[i] = [tracks[i], 1]
    tracks_start = dict(sorted(tracks_start.items(), key=lambda x: x[1][1], reverse=False))
    tracks_end = dict(sorted(tracks_end.items(), key=lambda x: x[1][1], reverse=False))
    for i in range(len(tracks_start)): 
        tracks_start[i].pop(1)
        tracks_end[i].pop(1)
    print(f"Sorting completed in {time() - start} seconds")
    return tracks_start, tracks_end

def merge(tracks: list, allowable_angle=160, allowable_length=700, allowable_distance=35):
    count = 0
    start = time()
    print("Starting real merging")
    i = 0
    while i < len(tracks):
        if len(tracks[i]) < 2:
            i += 1
            continue
        j = 0
        # Get vector of the first track
        if len(tracks[i]) == 2:
            vec_1 = get_vector(tracks[i][0], tracks[i][1])
        else:
            vec_1 = average_vec([tracks[i][k] for k in range(3)])

        while j < len(tracks) and i < len(tracks):
            # Check length of tracks
            if len(tracks[j]) < 2 or len(tracks[i]) < 2 or i == j:
                j += 1
                continue

            # Check distance between tracks
            vec_a = get_vector(tracks[i][0], tracks[j][-1])
            if get_vector_length(vec_a) > allowable_length:
                j += 1
                continue

            # Discarding not co-directed tracks
            if not co_directed(tracks[i], tracks[j]):
                j += 1
                continue

            # Get vector of the second track
            if len(tracks[j]) == 2:
                vec_2 = get_vector(tracks[j][-1], tracks[j][-2])
            else:
                vec_2 = average_vec([tracks[j][-k] for k in range(1, 4)])

            # Check angele between tracks
            if angle_between_vec(vec_1, vec_2) < allowable_angle:
                j += 1
                continue

            # Check distance between straight lines formed by tracks
            distance = distance_to_line(np.array(tracks[i][0][0:3]),
                                        np.array(tracks[i][1][0:3]),
                                        np.array(tracks[j][-1][0:3]))
            if distance < allowable_distance:
                tracks[i].extend(tracks[j])
                tracks[i] = sort_hits_old(tracks[i])
                tracks.pop(j)
                i -= 1
                break
            else:
                j += 1
        i += 1
    print(f"Real merging completed in {time() - start} seconds")
    print(f"After merging there are {len(tracks)} tracks")
    return tracks

def find_key(dict, track_dict):
    for key, track in dict.iteritems():
        if track == track_dict:
            return key

def fast_merging(tracks: list, allowable_angle=160, allowable_length=700, allowable_distance=35):
    count = 0
    start = time()
    print("Starting real merging")
    tracks_start, tracks_end = angle_sorting(tracks)
    list_start = list(tracks_start.values())
    list_end = list(tracks_end.values()) #list(tracks_end.items())[1][1][0]
    i = 0
    while i < len(list_end):
        if len(list_end[i][0]) < 2:
            i += 1
            continue
        j = 0
        # Get vector of the first track
        if len(list_end[i][0]) == 2:
            vec_1 = get_vector(list_end[i][0][0], list_end[i][0][1])
        else:
            vec_1 = average_vec([list_end[i][0][k] for k in range(3)])

        while j < len(list_start) and i < len(list_end):
            # Check length of tracks
            if len(list_start[j][0]) < 2 or len(list_end[i][0]) < 2 or i == j:
                j += 1
                continue

            # Check distance between tracks
            vec_a = get_vector(list_end[i][0][0], list_start[j][0][-1])
            if get_vector_length(vec_a) > allowable_length:
                j += 1
                continue

            # Discarding not co-directed tracks
            if not co_directed(list_end[i][0], list_start[j][0]):
                j += 1
                continue

            # Get vector of the second track
            if len(list_start[j][0]) == 2:
                vec_2 = get_vector(list_start[j][0][-1], list_start[j][0][-2])
            else:
                vec_2 = average_vec([list_start[j][0][-k] for k in range(1, 4)])

            # Check angele between tracks
            if angle_between_vec(vec_1, vec_2) < allowable_angle:
                j += 1
                continue

            if get_track_angle(vec_1)-get_track_angle(vec_2) > 15:
                j += 1
                continue

            # Check distance between straight lines formed by tracks
            distance = distance_to_line(np.array(list_end[i][0][0][0:3]),
                                        np.array(list_end[i][0][1][0:3]),
                                        np.array(list_start[j][0][-1][0:3]))
            if distance < allowable_distance:
                list_end[i].extend(list_start[j])
                # list_end[i] = sort_hits_old(list_end[i])
                list_start.pop(j)
                if list_start[j] in list_end:
                    list_end.remove(list_start[j])

                i -= 1
                break
            else:
                j += 1
        i += 1
    tracks = list_start
    print(f"Real merging completed in {time() - start} seconds")
    print(f"After merging there are {len(tracks)} tracks")
    return tracks


