tracks = []
track_id = 0
with open("event.txt", "r") as f:
    for i in f:
        temp = []
        tracks.append([])
        mas = i.split(", ")
        amount_characteristics = 0
        j = 0
        while j < len(mas):
            if amount_characteristics != 9:
                temp.append(float(mas[j]))
                amount_characteristics += 1
                j += 1
            else:
                tracks[track_id].append(temp)
                temp = []
                amount_characteristics = 0
        if j == amount_characteristics:
            tracks[track_id].append(temp)
            temp = []
            amount_characteristics = 0
        track_id += 1
print(tracks)