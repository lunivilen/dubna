from time import time
import pandas as pd
import numpy as np


def merge_tracks(track_one: list, track_two: list):
    similarity_factor = 0.5
    temp_mas = np.concatenate((track_one, track_two))
    unique = np.unique(temp_mas)
    difference = temp_mas.shape[0] - unique.shape[0]
    if difference / len(track_two) > similarity_factor:
        return unique.tolist(), 1
    elif difference / len(track_one) > similarity_factor:
        return unique.tolist(), 2
    else:
        return [], 0


def separate_tracks(track_one: list, track_two: list):
    for point in track_two:
        if point in track_one:
            track_two.remove(point)
    return track_one


def sort_hits(points):
    points = list(map(lambda x: np.array(x), points))

    # Нахождение расстояния каждой точки до центра координат
    distances_to_center = np.linalg.norm(points, axis=1)

    # Нахождение индекса ближайшей точки
    nearest_point_index = np.argmin(distances_to_center)

    # Формирование линии из точек
    line = [points[nearest_point_index]]
    remaining_points = np.delete(points, np.where(points == points[nearest_point_index])[0], axis=0)
    while len(remaining_points) > 0:
        last_point = line[-1]
        distances = np.linalg.norm(remaining_points - last_point, axis=1)
        closest_point_index = np.argmin(distances)
        closest_point = remaining_points[closest_point_index]
        line.append(closest_point)
        remaining_points = np.delete(remaining_points, closest_point_index, axis=0)

    line = list(map(lambda x: list(x), line))
    return line


def cleaning(tracks: list):
    print(f"Before cleaning there are {len(tracks)} tracks")

    # Speed up
    hits = {}
    for i in range(len(tracks)):
        for j in range(len(tracks[i])):
            s = tracks[i][j][0]
            hits[s] = tracks[i][j]
            tracks[i][j] = s

    print("Starting the first stage of merging duplicates")
    start = time()
    # The first merging stage
    i = 0
    while i < len(tracks):
        j = i + 1
        while j < len(tracks) and i < len(tracks):
            if tracks[j][0] in tracks[i] and i != j:
                merged_track, number = merge_tracks(tracks[i], tracks[j])
                if number == 1:
                    tracks[i] = merged_track
                    tracks.pop(j)
                    j -= 1
                elif number == 2:
                    tracks[j] = merged_track
                    tracks.pop(i)
                    i -= 1
                    break
            j += 1
        i += 1

    print(f"The first stage of merging completed in {time() - start} seconds")
    print("Starting the second stage of merging duplicates")
    start = time()
    i = 0
    # The second merging stage
    while i < len(tracks):
        j = i + 1
        while j < len(tracks) and i < len(tracks):
            if i != j:
                merged_track, number = merge_tracks(tracks[i], tracks[j])
                if number == 1:
                    tracks[i] = merged_track
                    tracks.pop(j)
                    j -= 1
                elif number == 2:
                    tracks[j] = merged_track
                    tracks.pop(i)
                    i -= 1
                    break
            j += 1
        i += 1

    print(f"The second stage of merging completed in {time() - start} seconds")
    print("Starting separate tracks")
    start = time()

    # Separate tracks
    i = 0
    while i < len(tracks):
        for j in range(len(tracks)):
            if i != j:
                tracks[i] = separate_tracks(tracks[i], tracks[j])
        if len(tracks[i]) < 2:
            tracks.pop(i)
        else:
            i += 1
    print(f"Track separating completed in {time() - start} seconds")

    # Return to x,y,z
    for i in range(len(tracks)):
        for j in range(len(tracks[i])):
            tracks[i][j] = hits[tracks[i][j]][1:]

    print("Staring sorting the points in the track")
    start = time()

    # Sort the hits in the correct order after merge
    for i in range(len(tracks)):
        tracks[i] = sort_hits(tracks[i])

    print(f"Sorting completed in {time() - start} seconds")
    print(f"After cleaning there are {len(tracks)} tracks")
    return sorted(tracks, key=len)
