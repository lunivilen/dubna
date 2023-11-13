def create_clusters(track_list, min_n_shared_hits):
    # Sort tracks by length in descending order
    track_dict = {index: value for index, value in enumerate(track_list)}
    # Converting tracks to format as {track_id: hit_id_list}
    sorted_tracks = dict(sorted(track_dict.items(), key=lambda item: len(item[1]), reverse=True))
    clusters = []
    used_track_id = set()

    for track in sorted_tracks.items():
        if track[0] in used_track_id:
            # If the track already belongs to the cluster, skip it
            continue

        # Create a new cluster with the current track
        current_cluster = [{track[0]: track[1]}]
        used_track_id.add(track[0])

        # Checking all other tracks
        for other_track in sorted_tracks.items():
            if other_track[0] in used_track_id:
                continue
            # Check the number of shared hits
            if len(set(track[1]) & set(other_track[1])) >= min_n_shared_hits:
                current_cluster.append({other_track[0]: other_track[1]})
                used_track_id.add(other_track[0])

        # Add a cluster to the final list
        clusters.append(current_cluster)

    return clusters
