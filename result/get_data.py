def get_data(path):
    track_id = 0
    tracks = []
    with open(path, "r") as f:
        for i in f:
            temp = []
            tracks.append([])
            mas = i.split(", ")
            amount_characteristics = 0
            j = 0
            while j < len(mas):
                if amount_characteristics != 10:
                    if amount_characteristics != 0:
                        temp.append(float(mas[j]))
                    amount_characteristics += 1
                    j += 1
                else:
                    tracks[track_id].append(temp)
                    temp = []
                    amount_characteristics = 0
            if j == amount_characteristics:
                tracks[track_id].append(temp)
            track_id += 1
    return tracks
