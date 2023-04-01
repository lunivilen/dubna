from cleaning import sort_hits
from time import time
import numpy as np
import math


def get_vector(hit_1, hit_2):
    return np.array([hit_1[0] - hit_2[0], hit_1[1] - hit_2[1], hit_1[2] - hit_2[2]])


def angle_between_vec(v1, v2):
    dot_pr = v1.dot(v2)
    norms = np.linalg.norm(v1) * np.linalg.norm(v2)
    return np.rad2deg(np.arccos(dot_pr / norms))


def area_of_triangle(v1, v2):
    c = [v1[1] * v2[2] - v1[2] * v2[1], v1[0] * v2[2] - v1[2] * v2[0], v1[0] * v2[1] - v1[1] * v2[0]]
    return get_vector_length(c) / 2


def get_vector_length(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)


def check_direction(track_one, track_two):
    normal = get_vector(track_one[0], track_two[-1])
    reverse = get_vector(track_one[0], track_two[0])
    return get_vector_length(reverse) > get_vector_length(normal)


def average_vec(hits):
    vec_1 = get_vector(hits[0], hits[1])
    vec_2 = get_vector(hits[0], hits[2])
    vec_3 = get_vector(hits[1], hits[2])
    vec = np.array([])
    for i in range(3):
        vec = np.append(vec, (vec_1[i] + vec_2[i] + vec_3[i]) / 3)
    return vec


def merging(tracks: list):
    start = time()
    print("Staring real merging")
    allowable_angle = 160
    allowable_error = 200
    allowable_length = 160
    i = 0
    while i < len(tracks):
        if len(tracks[i]) < 2:
            i += 1
            continue
        j = 0
        vec_1 = get_vector(tracks[i][0][1:4], tracks[i][1][1:4])
        while j < len(tracks) and i < len(tracks):
            if len(tracks[j]) < 2 or len(tracks[i]) < 2 or i == j:
                j += 1
                continue

            end = -1 if check_direction(tracks[i], tracks[j]) else 0
            vec_2 = get_vector(tracks[j][end][1:4], tracks[j][end - 1][1:4])
            angel = angle_between_vec(vec_1, vec_2)
            if angle_between_vec(vec_1, vec_2) < allowable_angle:
                j += 1
                continue
            vec_a = get_vector(tracks[i][0][1:4], tracks[j][end][1:4])
            vec_b = get_vector(tracks[i][1][1:4], tracks[j][end][1:4])
            s = area_of_triangle(vec_a, vec_b)
            length = get_vector_length(vec_a)
            if s < allowable_error and length < allowable_length:
                tracks[i].extend(tracks[j])
                tracks[i] = sort_hits(tracks[i])
                tracks.pop(j)
                i -= 1
                break
            else:
                j += 1
        i += 1
    print(f"Real merging completed in {time() - start} seconds")
    print(f"After merging there are {len(tracks)} tracks")
    return tracks
