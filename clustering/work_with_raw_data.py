import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

tracks = []
track_id = 0
with open("../data/event.txt", "r") as f:
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

un_tr = tracks_df['track_number'].unique().tolist()

tracks_df.to_csv('../data/Tracks.csv')

indice = []
for i in un_tr:
    if len(tracks_df[tracks_df['track_number'] == i]['theta'].unique()) > 1:
        indice.append(i)

len(indice)

#different thetas in the same tracks
tracks_df[tracks_df['track_number'].isin(indice)]
tracks_df[tracks_df['track_number'] == 65]


#------------------r*phi------------------------
tracks_df['rphi'] = np.sign(tracks_df['y']) * np.sign(tracks_df['x']) *  np.sqrt(tracks_df['x']**2 * tracks_df['y']**2)  * tracks_df['phi'] 

tracks_df[tracks_df['hit-index'] == 21806.0]

tracks_df[tracks_df['track_number'] == 1269]

tracks_df['r'] = np.sign(tracks_df['y']) * np.sqrt(tracks_df['x']**2 * tracks_df['y']**2) 

tracks_df[['track_number','rphi', 'z', 'r', 'phi']].to_csv('check_line.csv')

#plt.scatter(tracks_df[tracks_df['track_number'] == 2]['rphi'], tracks_df[tracks_df['track_number'] == 2]['z']) 
#tracks_df[tracks_df['track_number'] == 3][['track_number','r', 'phi', 'z', 'x', 'y']]


#monotonous check

#--------------------REGRESSION---------------------

r_sq = []
coef = []
length = []

tracks_df['constant'] = 1

for i in un_tr:
    if len(tracks_df[tracks_df['track_number'] == i]) > 1:
        x = tracks_df[tracks_df['track_number'] == i][['constant', 'rphi']]
        y = tracks_df[tracks_df['track_number'] == i]['z']
        model = LinearRegression().fit(x, y)
        r_sq.append(model.score(x, y))
        coef.append(model.coef_)
    else: 
        r_sq.append(None)
        coef.append(model.coef_)
    length.append(len(tracks_df[tracks_df['track_number'] == i]))


regress = pd.DataFrame(data = un_tr, columns = ['track_number'])
regress['r_squared'] = r_sq
regress['coef_x_z'] = coef
regress['length'] = length

regress.to_csv('data_for_cluster.csv')

regress[regress['r_squared'] > 0.99]

regress.head(5)