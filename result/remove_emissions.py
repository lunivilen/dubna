from merging import get_vector, get_vector_length
from time import time


def remove_emissions(tracks: list):
    print("Start removing emissions")
    start = time()
    for track in tracks:
        i = 0
        while i < len(track) - 2:
            vec_1 = get_vector(track[i], track[i + 1])
            vec_2 = get_vector(track[i], track[i + 2])
            if get_vector_length(vec_1) > get_vector_length(vec_2):
                track.remove(track[i + 1])
            else:
                i += 1
    print(f"Removing emissions completed in {time() - start} seconds")
    return tracks
