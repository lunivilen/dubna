import pandas as pd


def replace_hits_to_track_id(tracks, hits):
    tracks_hits = {}
    for i in range(len(tracks)):
        tracks_hits[i] = []
        for hit in tracks[i]:
            hit_id = hit[0]
            truth_track_id = int(hits[hit_id][3])
            tracks_hits[i].append(truth_track_id)
    return tracks_hits


def get_real_tracks(track_dict, n):
    real_track_list = []
    for tack_id, hit_list in track_dict.items():
        if len(hit_list) >= n:
            real_track_list.append(tack_id)
    return real_track_list


def get_characteristics(tracks, hits, n, ratio):
    reco_tracks = set()
    fake_tracks = set()
    duplicate_tracks = []

    # Replace hits in track with id of their real track
    tracks_hits = replace_hits_to_track_id(tracks, hits)
    for i in range(len(tracks)):
        if len(tracks[i]) < n:
            continue

        # Find the most common real track id in reco track
        reco_track_id = max(tracks_hits[i], key=tracks_hits[i].count)

        # Check duplicates
        if reco_track_id in reco_tracks:
            duplicate_tracks.append(reco_track_id)
            continue

        # Check ration and mark track as reco or fake
        if tracks_hits[i].count(reco_track_id) / len(tracks_hits[i]) >= ratio:
            reco_tracks.add(reco_track_id)
        else:
            fake_tracks.add(i)
    return reco_tracks, fake_tracks, duplicate_tracks


def calc_characteristics(tracks, hit_list, track_dict, secondary_track_list=None, min_length=9, ratio=0.5):
    # Get all lists of necessary data
    reco_track_list, fake_track_list, duplicate_track_list = get_characteristics(tracks, hit_list, min_length, ratio)
    real_track_list = get_real_tracks(track_dict, min_length)

    # Remove secondary track id from data if in necessary
    if secondary_track_list:
        for info_list in [reco_track_list, duplicate_track_list, real_track_list]:
            for track_id in secondary_track_list:
                if track_id in info_list:
                    info_list.remove(track_id)

    # Save table of reco and not reco tracks
    # save_recognised_logo(reco_track_list, real_track_list)

    # Calc characteristics
    num_real_track = len(real_track_list)
    num_proto_track = len(tracks)

    characteristic_dict = {
        "efficiency": len(reco_track_list) / num_real_track if num_real_track else 0,
        "fake_rate": len(fake_track_list) / num_real_track if num_real_track else 0,
        "duplication_rate": len(duplicate_track_list) / num_proto_track if num_real_track else 0,
        "purity": num_real_track / num_proto_track if num_proto_track else 0
    }
    return characteristic_dict


def save_recognised_logo(reco_track_list, real_track_list):
    result_df = pd.DataFrame(columns=["track_id", "is_reco"])
    for i, track_id in enumerate(real_track_list):
        result_df.at[i, "track_id"] = track_id
        result_df.at[i, "is_reco"] = track_id in reco_track_list
    result_df = result_df.sort_values(by=["is_reco"])
    result_df.to_csv("logo.csv", index=False)
