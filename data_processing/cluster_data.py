def create_clusters(track_list, n_hits):
    # Сортируем треки по длине в убывающем порядке
    track_dict = {index: value for index, value in enumerate(track_list)}
    # Переводим треки в представление вида {track_id: hit_id_list}
    sorted_tracks = dict(sorted(track_dict.items(), key=lambda item: len(item[1]), reverse=True))
    clusters = []
    used_track_id = set()

    for track in sorted_tracks.items():
        if track[0] in used_track_id:
            # Если трек уже принадлежит кластеру, пропускаем его
            continue

        # Создаем новый кластер с текущим треком
        current_cluster = [{track[0]: track[1]}]
        used_track_id.add(track[0])

        # Проверяем все остальные треки
        for other_track in sorted_tracks.items():
            if other_track[0] in used_track_id:
                continue
            # Проверяем количество общих хитов
            if len(set(track[1]) & set(other_track[1])) >= n_hits:
                current_cluster.append({other_track[0]: other_track[1]})
                used_track_id.add(other_track[0])

        # Добавляем кластер в итоговый список
        clusters.append(current_cluster)

    return clusters
