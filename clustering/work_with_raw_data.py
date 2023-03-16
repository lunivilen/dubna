import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

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

tracks[1]

for i in range(len(tracks)):
    for track in tracks[i]:
        track.insert(0, i)

def flatten(l):
    return [item for sublist in l for item in sublist]

tracks_numd = flatten(tracks)

tracks_df = pd.DataFrame(data = tracks_numd, columns = ('track_number', 'hit-index', 'x', 'y', 'z', 'phi', 'theta', 'q/p', 't', 'chi2'))

tracks_df.head(5)


#------------------------------------------------bugging
tracks_df.groupby('track_number')['phi'].mean()
tracks_df[tracks_df['track_number'] == 2]['phi']- tracks_df[tracks_df['track_number'] == 2]['phi'].shift(1)
(tracks_df.groupby('track_number')['phi'].mean()- tracks_df.groupby('track_number')['phi'].mean().shift(1)).mean()
tracks_df = tracks_df[tracks_df[['hit-index', 'x', 'y', 'z', 'phi', 'theta', 'q/p', 't', 'chi2']].duplicated()==False]

print(len(tracks_df['theta'].unique()))
#print(tracks_df['track_number'].max())
#print(tracks_df[[tracks_df['theta']]])
#print(tracks_numd)
#print(tracks[2])
#-----------------------------------------------

tracks_df.to_csv('Tracks.csv')


#--------------------REGRESSION---------------------

r_sq = []
coef = []
length = []
un_tr = tracks_df['track_number'].unique().tolist()

for i in un_tr:
    if len(tracks_df[tracks_df['track_number'] == i]) > 1:
        x = tracks_df[tracks_df['track_number'] == i][['x', 'z']]
        y = tracks_df[tracks_df['track_number'] == i]['y']
        model = LinearRegression().fit(x, y)
        r_sq.append(model.score(x, y))
        coef.append(model.coef_)
    else: 
        r_sq.append(None)
        coef.append(None)
    length.append(len(tracks_df[tracks_df['track_number'] == i]))


regress = pd.DataFrame(data = un_tr, columns = ['track_number'])
regress['r_squared'] = r_sq
regress['coef_x_z'] = coef
regress['length'] = length

regress[regress['r_squared'] > 0.90]

regress.head(5)