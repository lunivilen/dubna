from data_processing.parse_data import *
from copy import deepcopy
import time

# Функция для нахождения общих хитов между двумя треками
def common_hits(track1, track2):
    hits1 = set(hit[0] for hit in track1)
    hits2 = set(hit[0] for hit in track2)
    return len(hits1.intersection(hits2))


def count_shared(tracks):
    used_hits = set()
    shared_num = {}
    for i, track in tracks.items():
        shared_num[i]=0
        for hit in track:
            if str(hit) in used_hits:
                shared_num[i]+=1
            else: 
                used_hits.add(str(hit))
    return shared_num


def cluster_tracks(tracks, n):
    # Собираем словарь с инфой, в каких треках встречается каждый хит
    hit_to_tracks = {}
    for track_index, track in enumerate(tracks):
        for hit in track:
            hit_index = hit[0]
            if hit_index not in hit_to_tracks:
                hit_to_tracks[hit_index] = set()
            hit_to_tracks[hit_index].add(track_index)

    # Кластеризация треков
    clusters = []
    used_tracks = set()
    for i, track1 in enumerate(tracks):
        if i in used_tracks:
            continue

        cluster = [i]
        used_tracks.add(i)

        for j, track2 in enumerate(tracks):
            if j not in used_tracks and common_hits(track1, track2) >= n:
                cluster.append(j)
                used_tracks.add(j)

        clusters.append(cluster)

    return clusters


def greedy_solver(tracks, clusters, n=2):
    tracks = deepcopy(tracks)
    # clusters = cluster_tracks(tracks, n)
    filtered_tracks = {i: track for i, track in enumerate((filter(lambda track: len(track) > n, tracks)))}
    filtered_tracks = dict(sorted(filtered_tracks.items(), key = lambda x: len(x[1])))
    shared_num = count_shared(filtered_tracks)
    while len(filtered_tracks) > 0:
        max_idx = max(shared_num, key = shared_num.get)
        if shared_num[max_idx] > n:
            for i, cluster in enumerate(clusters):
                if max_idx in cluster:
                    # print('1')
                    tracks_list = clusters[i]
            for track_id in tracks_list:
                # print('2')
                if track_id in filtered_tracks:
                    shared_num[track_id] = shared_num[track_id] - common_hits(filtered_tracks[max_idx], filtered_tracks[track_id])
            # print('3')
            
            shared_num.pop(max_idx)
            # print('4')
            tracks.remove(filtered_tracks[max_idx])
            filtered_tracks.pop(max_idx)
        else: 
            break
    return tracks


def clone_and_fake_remove(tracks, clusters, ratio=0.3):
    sorted_tracks = {i: track for i, track in enumerate(tracks)}
    sorted_tracks = dict(sorted(sorted_tracks.items(), key = lambda x: len(x[1])))
    shared_num = count_shared(sorted_tracks)
    for track_id, track in sorted_tracks.items():
        if shared_num[track_id]/len(track)>=ratio:
            for i, cluster in enumerate(clusters):
                if track_id in cluster:
                    # print('1')
                    tracks_list = clusters[i]
            for id in tracks_list:
                
                if id in shared_num:
                    # print('2')
                    # print(id)
                    # print(track_id)
                    shared_num[id] = shared_num[id] - common_hits(sorted_tracks[track_id], sorted_tracks[id])
            # print('3')
            tracks.remove(sorted_tracks[track_id])
            shared_num.pop(track_id)
    return tracks

# tracks = get_tracks_data("data/event_1_prototracks.txt", "data/event_1_space_points.txt")
# clusters = cluster_tracks(tracks, 1)
# start = time.time()
# greedy_tracks = greedy_solver(tracks, clusters, n=2)
# yuri_tracks = clone_and_fake_remove(tracks, clusters, ratio=0.3)
# print(time.time() - start)
