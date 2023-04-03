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


def sort_hits(track):
    df = pd.DataFrame(track, columns=[0, 1, 2, 3, 4, 5, 6, 7, 8])
    scatter_x = df[1].max() - df[1].min()
    scatter_y = df[2].max() - df[2].min()
    scatter_z = df[3].max() - df[3].min()
    if max(scatter_x, scatter_y, scatter_z) == scatter_x:
        track = list(df.sort_values(1, ascending=True).values)
    elif max(scatter_x, scatter_y, scatter_z) == scatter_y:
        track = list(df.sort_values(2, ascending=True).values)
    else:
        track = list(df.sort_values(3, ascending=True).values)
    return list(map(list, track))


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
        if not tracks[i]:
            tracks.pop(i)
        else:
            i += 1
    print(f"Track separating completed in {time() - start} seconds")

    # Return to x,y,z and etc.
    for i in range(len(tracks)):
        for j in range(len(tracks[i])):
            tracks[i][j] = hits[tracks[i][j]]

    print("Staring sorting the points in the track")
    start = time()

    # Sort the hits in the correct order after merge
    for i in range(len(tracks)):
        tracks[i] = sort_hits(tracks[i])

    print(f"Sorting completed in {time() - start} seconds")
    print(f"After cleaning there are {len(tracks)} tracks")
    return sorted(tracks, key=len)
