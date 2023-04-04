from remove_emissions import remove_emissions
from visualizing import visualizing
from save_data import save_data
from get_data import get_data
from cleaning import cleaning
from merging import merging

tracks = get_data("data/new_event.txt")
# tracks = cleaning(tracks)
# tracks = merging(tracks, allowable_angle=160, allowable_error=700, allowable_length=700, allowable_distance=35)
tracks = remove_emissions(tracks)
# save_data(tracks)
app = visualizing(tracks, show_tracks_indexes=True)

if __name__ == '__main__':
    app.exec()
