from time import time
from collections import defaultdict

def count_tracks_intersections(all_tracks: dict):                                 
    intersections = defaultdict(list)
    intersections_count = defaultdict(int)
    tracks_graph = defaultdict(list)
    for new_track_id, track in all_tracks.items():
        for point in track: 
            point_id = point[0]
            for track_id in intersections.get(point_id, []):
                track_pair = (track_id, new_track_id) if track_id < new_track_id else (new_track_id, track_id)
                tracks_graph[track_pair[0]].append(track_pair[1])
                tracks_graph[track_pair[1]].append(track_pair[0])
                intersections_count[track_pair] += 1
            intersections[point_id].append(new_track_id)
    return intersections_count, tracks_graph            
    

def divide_tracks_graph(
        intersections_count: dict,
        tracks_graph: dict,
        all_tracks: dict):
    graph_to_separate = {}
    graph_to_unite = {}
    for vertex, edges in tracks_graph.items():
        unite_edges = list()
        separate_edges = list()
        for edge in set(edges):
            track_pair = (edge, vertex) if edge < vertex else (vertex, edge)
            num_shared_points = intersections_count[track_pair]
            min_len = min(len(all_tracks[track_pair[0]]), len(all_tracks[track_pair[1]]))
            unite_edges.append(edge) if num_shared_points / min_len > 0.5 else separate_edges.append(edge)
        if len(unite_edges) != 0: graph_to_unite[vertex] = set(unite_edges)
        if len(separate_edges) != 0: graph_to_separate[vertex] = set(separate_edges)
    return graph_to_unite, graph_to_separate


def dfs(graph: dict, start: int, all_visited: set, visited):
    if visited is None: visited = set()
    visited.add(start)
    all_visited.add(start)
    for next_vertex in graph[start]:
        if next_vertex not in all_visited:
            dfs(graph, next_vertex, all_visited, visited)


def get_connected_components(graph: dict):
    all_visited = set() 
    connected_components = []
    for vertex in graph.keys():
        if vertex not in all_visited:
            visited = set()
            dfs(graph, vertex, all_visited, visited)
            connected_components.append(visited)
    return connected_components


def process_tracks(tracks: list):
    first_start = time()
    tracks_dict = {i : tracks[i] for i in range(len(tracks))}
    intersections_count, tracks_graph = count_tracks_intersections(
            tracks_dict)

    #print("Graph:")
    #print(len(tracks_graph))
    graph_to_unite, graph_to_separate = divide_tracks_graph(
            intersections_count,
            tracks_graph,
            tracks_dict)

    #print("Graph to unite:")
    #print(len(graph_to_unite))
    #print(list(graph_to_unite.items())[0])
    #print(list(graph_to_unite.items())[1])
    #print(list(graph_to_unite.items())[2])

    tracks_to_unite = get_connected_components(graph_to_unite)
    #print("Tracks to unite:")
    #print(len(tracks_to_unite))
    #print(tracks_to_unite[0])
    #print(tracks_to_unite[1])
    #print(tracks_to_unite[2])
    #print(tracks_to_unite[3])

    end = time()
    print("All process_tracks time:")
    print(end - first_start)
    return tracks_dict, tracks_to_unite, graph_to_separate



def flatten(l):
    return [item for sublist in l for item in sublist]

def unite_tracks(tracks_dict, tracks_to_unite, graph_to_separate):
    tracks = []
    for i in range(len(tracks_to_unite)):
        track = []
        for j in list(tracks_to_unite[i]):
            track.append((tracks_dict[j]))
        tracks.append(flatten(track))
    tracks
    return tracks

