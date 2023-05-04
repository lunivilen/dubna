from remove_emissions import remove_emissions
from visualizing import visualizing
from save_data import save_data
from get_data import get_data
from cleaning import cleaning
from merging import merging
from fast_cleaning import process_tracks

tracks = get_data("data/event0.txt")
tracks_dict, tracks_to_unite, graph_to_separate = process_tracks(tracks)
tracks = cleaning(tracks)
tracks = merging(tracks,
                 allowable_angle=160,
                 allowable_length=700,
                 allowable_distance=35)
#tracks = remove_outliers(tracks)
save_data(tracks)
app = visualizing(tracks, show_tracks_indexes=False)

if __name__ == '__main__':
    app.exec()
