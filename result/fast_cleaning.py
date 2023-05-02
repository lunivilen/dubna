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
        if len(unite_edges): graph_to_unite[vertex] = set(unite_edges)
        if len(separate_edges): graph_to_separate[vertex] = set(separate_edges)
    return graph_to_unite, graph_to_separate


def dfs(graph: dict, start: int, visited = None):
    if visited is None: visited = set() 
    visited.add(start)
    for next_vertex in graph[start]:
        if next_vertex not in visited:
            dfs(graph, next_vertex, visited)
    return visited


def get_connected_components(graph: dict):
    all_visited = set() 
    connected_components = []
    for vertex in graph.keys():
        if vertex not in all_visited:
            visited = dfs(graph, vertex)
            connected_components.append(visited)
            all_visited.union(visited)
    return connected_components


def process_tracks(tracks: list):
    first_start = time()
    tracks_dict = {i : tracks[i] for i in range(len(tracks))}
    intersections_count, tracks_graph = count_tracks_intersections(
            tracks_dict)
    graph_to_unite, graph_to_separate = divide_tracks_graph(
            intersections_count,
            tracks_graph,
            tracks_dict)
    tracks_to_unite = get_connected_components(graph_to_unite)
    end = time()
    print("All process_tracks time:")
    print(end - first_start)
    return tracks_dict, tracks_to_unite, graph_to_separate

