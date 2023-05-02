def to_dict(tracks: list):
    tracks_dict = {}
    for i in range(len(tracks)):
        tracks_dict[i] = tracks[i]
    return tracks_dict


def get_correct_order(track1_id: int, track2_id: int):
    if track1_id < track2_id:                                     
        track1_id, track2_id = track2_id, track1_id 
    return track1_id, track2_id

def update_tracks_graph(
        track_id: int,
        intersected_track_id: int, 
        tracks_graph: dict):

    if track_id in tracks_graph:
        tracks_graph[track_id].add(intersected_track_id)         
    else:
        tracks_graph[track_id] = set([intersected_track_id])


def update_tracks_intersections(
        intersections_count: dict,
        tracks_graph: dict,
        tracks_with_point: set,
        new_track_id: int):

    for track_id in tracks_with_point:
        track1_id, track2_id = get_correct_order(track_id, new_track_id)

        update_tracks_graph(track1_id, track2_id, tracks_graph)
        update_tracks_graph(track2_id, track1_id, tracks_graph)

        track_pair = (track1_id, track2_id)
        
        if track_pair in intersections_count:
            intersections_count[track_pair] += 1
        else:                                   
            intersections_count[track_pair] = 1
            

def count_tracks_intersections(all_tracks: dict):                                 
    intersections = {}
    intersections_count = {}
    tracks_graph = {}

    for track_id, track in all_tracks.items():
        for point in track: 
            point_id = point[0]
            if point_id in intersections:
                update_tracks_intersections(
                    intersections_count,
                    tracks_graph,
                    intersections[point_id],
                    track_id)
                intersections[point_id].add(track_id)
            else:
                intersections[point_id] = set([track_id])
                                                                
    return intersections_count, tracks_graph            
    

def divide_tracks_graph(
        intersections_count: dict,
        tracks_graph: dict,
        all_tracks: dict):

    graph_to_separate = {}
    graph_to_unite = {}

    for vertex, edges in tracks_graph.items():
        unite_edges = set()
        separate_edges = set()
        for edge in edges:
            track1_id, track2_id = get_correct_order(edge, vertex)

            track_pair = (track1_id, track2_id)

            num_shared_points = intersections_count[track_pair]
            len_track1 = len(all_tracks[track1_id])
            len_track2 = len(all_tracks[track2_id])
            min_len = min(len_track1, len_track2)

            if num_shared_points / min_len > 0.5:
                unite_edges.add(edge)
            else:
                separate_edges.add(edge)

        if len(unite_edges):
            graph_to_unite[vertex] = unite_edges

        if len(separate_edges):
            graph_to_separate[vertex] = separate_edges

    return graph_to_unite, graph_to_separate


def dfs(graph: dict, start: int, visited = None):
    if visited is None:
        visited = set()
    visited.add(start)

    for next_vertex in graph[start].difference(visited):
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
    #print("Track presentation:")
    #print(tracks[0])

    tracks_dict = to_dict(tracks)
    #print("Track dict:")
    #print(next(iter(tracks_dict.items())))

    intersections_count, tracks_graph = count_tracks_intersections(
            tracks_dict)

    #print("Intersections count:")
    #print(next(iter(intersections_count.items())))

    #print("Tracks graph:")
    #print(next(iter(tracks_graph.items())))

    graph_to_unite, graph_to_separate = divide_tracks_graph(
            intersections_count,
            tracks_graph,
            tracks_dict)

    #print("Graph to unite:")
    #print(next(iter(graph_to_unite.items())))

    #print("Graph to separate:")
    #print(next(iter(graph_to_separate.items())))
    
    tracks_to_unite = get_connected_components(graph_to_unite)

    #print("Tracks to unite:")
    #print(tracks_to_unite[0])

    return tracks_dict, tracks_to_unite, graph_to_separate

