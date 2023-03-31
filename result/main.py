from get_data import get_data
from cleaning import cleaning
from visualizing import visualizing
from save_data import save_data

tracks = get_data("event.txt")
tracks = cleaning(tracks)
save_data(tracks)
app = visualizing(tracks)

if __name__ == '__main__':
    app.exec()
