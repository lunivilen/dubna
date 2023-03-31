def save_data(tracks):
    # Saving new tracks
    with open("new_event.txt", "w") as f:
        for track in tracks:
            for hit in track:
                for characteristic in hit:
                    f.write(str(characteristic) + ", ")
            f.write("\n")