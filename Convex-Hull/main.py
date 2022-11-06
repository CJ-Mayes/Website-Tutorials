import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull
from mplsoccer.pitch import Pitch
from scipy import stats
from statsbombpy import sb

# Get competitions
comp = sb.competitions()

# Get Matches from Womens World Cup - 2020/21
match = sb.matches(competition_id=72, season_id=30)

#Find a match
match = 69321
df = sb.events(match_id=match)

# Filter to passes
events = df[(df.type == 'Pass')].copy()

# split locations into x and y components
events[['x', 'y']] = df['location'].apply(pd.Series)

#Combo box, choose players
options = events["team"].unique()
options = options.tolist()
options = [x for x in options if str(x) != 'nan']
print(options)

# Choose Team
team = "United States Women's"

# filter for the team we want and reset the index so that we can use for loops over it
events_us = events[events['team'] == team].reset_index()
events_us = events_us[['player','team','type','x','y']]

p = []
for i in events_us.player.unique():
    p.append(i)
    p.sort()

    # Initialize empty dictionary
    player_dict = {}

    for i in p:
        player_dict[i] = pd.DataFrame(events_us[events_us['player'] == i])

#Combo box, choose players
options = events_us["player"].unique()
options = options.tolist()

#player = playerlist.value
player = 'Crystal Alyssia Dunn Soubrier'
player_df = player_dict[player]

#filter that dataframe to exclude outliers. Anything over a z score of 3 will be excluded for the data points
test = player_df[(np.abs(stats.zscore(player_df[['x','y']])) < 3)]
test = test[['x', 'y']]
test = test.dropna()

#Create an array of the x/y coordinate groups
points = test[['x', 'y']].values

#Set up pitch
pitch = Pitch(pitch_type='statsbomb',linewidth=5, spot_scale=0.007,
             pitch_color='#0d183f',line_color='w')
fig,ax = pitch.draw(figsize=(13, 11), constrained_layout=False, tight_layout=True)
fig.set_facecolor('#0d183f')

#Inverse the y-axis
plt.gca().invert_yaxis()

#plot the pass locations
plt.scatter(player_df.x, player_df.y, marker='o', s=250, c='red',
            linewidth = 3, edgecolor='w')

#Create the convex hull
hull = ConvexHull(test[['x','y']])

#Loop through each of the hull's simplices
for i in hull.simplices:
    plt.plot(points[i, 0], points[i, 1], 'yellow', ls ='--')
    plt.fill(points[hull.vertices,0], points[hull.vertices,1], c='white', alpha=0.04)

#Title & Annotations
fig.suptitle(player +"'s Territory Map", fontsize=31, color='yellow',
            fontfamily = "Courier New", fontweight = "bold",y=0.9)

highlight_textprops =\
    [{"color": "crimson","fontweight": 'bold'}]

# If you want to see what the original chart looks like you can use plt.show()
#plt.show()

#Drop the x and y, only to add the x and y from the test df again just for precaution purposes,
#in the event that the test df has gone through a filtering process based on the std deviation
player_df = player_df.drop(['x','y'], axis = 1)
player_df['x']=test['x']
player_df['y']=test['y']
player_df = player_df.dropna()

player_df = player_df.reset_index(drop = True)

#Vertices that make up the outer shape of the hull
o = points[hull.vertices]
dfa = pd.DataFrame(o,
                  columns = ['x','y'])
dfa

data1 = pd.DataFrame(o, columns=list('xy')).to_dict('r')
data2 = pd.DataFrame(points, columns=list('xy')).to_dict('r')

data1 = pd.DataFrame(data1)
data1['pathID'] = range(1, len(data1) + 1)
data2 = pd.DataFrame(data2)

df3=pd.merge(data1,data2, how='inner')
df3 = df3.drop_duplicates(subset=['x', 'y'], keep='last').reset_index(drop=True)

df3['player'] = player_df['player']
df3['team'] = player_df['team']
df3['type'] = player_df['type']

df3 = df3[['player','team','type','x','y','pathID']]

#for the purpose of merging the two dataframes, name one of either x or y as a dummy
player_df = player_df.rename({'x': 'oldx'}, axis=1)

#merge it so we can find the values that do coincide with the hull points
merged = player_df.merge(df3, how='left',
                    left_on=['player','team','type','oldx','y'],
                    right_on=['player','team','type','x','y'])

#create a new column, if it is N/A, it means the point is not a hull
merged['HullPoint'] = np.where((merged['x'].isnull()),"no","yes")

#drop the x variable because it's served its purpose in helping us identify the columns
merged = merged.drop(['x'],axis=1)

#rename the oldx to x back
merged = merged.rename({'oldx': 'x'}, axis=1)
merged.to_csv('dataset.csv')
