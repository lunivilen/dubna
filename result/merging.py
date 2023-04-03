from cleaning import sort_hits
from time import time
import numpy as np
import math


def get_vector(hit_1, hit_2):
    return np.array([hit_2[0] - hit_1[0], hit_2[1] - hit_1[1], hit_2[2] - hit_1[2]])


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
    vec = np.array([hits[2][0] - hits[0][0], hits[2][1] - hits[0][1], hits[2][2] - hits[0][2]])
    return vec * 2 / 3


def distance_to_line(m0, m1, m_check):
    ab = m0 - m1
    ac = m_check - m1
    d = np.linalg.norm(np.cross(ab, ac)) / np.linalg.norm(ab)
    return d


def merging(tracks: list, allowable_angle=160, allowable_error=700, allowable_length=700, allowable_distance=35):
    start = time()
    print("Staring real merging")
    i = 0
    while i < len(tracks):
        if len(tracks[i]) < 2:
            i += 1
            continue
        j = 0
        # Get vector of the first track
        if len(tracks[i]) == 2:
            vec_1 = get_vector(tracks[i][0][1:4], tracks[i][1][1:4])
        else:
            vec_1 = average_vec([tracks[i][k][1:4] for k in range(3)])

        while j < len(tracks) and i < len(tracks):
            if len(tracks[j]) < 2 or len(tracks[i]) < 2 or i == j:
                j += 1
                continue

            # Correcting the direction of the track
            end = -1 if check_direction(tracks[i], tracks[j]) else 0

            # Get vector of the second track
            if len(tracks[j]) == 2:
                vec_2 = get_vector(tracks[j][end][1:4], tracks[j][end - 1 if end < 0 else end + 1][1:4])
            else:
                vec_2 = average_vec([tracks[j][end][1:4],
                                     tracks[j][end - 1 if end < 0 else end + 1][1:4],
                                     tracks[j][end - 2 if end < 0 else end + 2][1:4]])
            if angle_between_vec(vec_1, vec_2) < allowable_angle:
                j += 1
                continue

            # We build a triangle from the last point of the second vector
            # and the last two points of the first vector
            vec_a = get_vector(tracks[i][0][1:4], tracks[j][end][1:4])
            vec_b = get_vector(tracks[i][1][1:4], tracks[j][end][1:4])
            s = area_of_triangle(vec_a, vec_b)
            length = get_vector_length(vec_a)
            if s < allowable_error and length < allowable_length:
                distance = distance_to_line(np.array(tracks[i][0][1:4]),
                                            np.array(tracks[i][1][1:4]),
                                            np.array(tracks[j][end][1:4]))
                if distance < allowable_distance:
                    tracks[i].extend(tracks[j])
                    tracks[i] = sort_hits(tracks[i])
                    tracks.pop(j)
                    i -= 1
                    break
                else:
                    j += 1
            else:
                j += 1
        i += 1
    print(f"Real merging completed in {time() - start} seconds")
    print(f"After merging there are {len(tracks)} tracks")
    return tracks
