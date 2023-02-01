"""
pip install statsbombpy
pip install pandas
pip install numpy
"""
import json

from mplsoccer import Pitch
from statsbombpy import sb
import pandas as pd
import numpy as np

# Get competitions - using statsbomb open data
comp = sb.competitions()
comp.to_csv('competitions.csv', index=False)

# UEFA Women's Euro taken from competition csv
df = sb.matches(competition_id=53, season_id=106)
df.to_csv('matches.csv', index=False)

# Find a match_id required - England Germany 2-1 in the final, blog example
match = 3847567
match_events = sb.events(match_id=match)

# split locations into x and y components
match_events[['location_x', 'location_y']] = match_events['location'].apply(pd.Series)
match_events[['pass_end_location_x', 'pass_end_location_y']] = match_events['pass_end_location'].apply(pd.Series)

# split the shot_end_locations into x,y and z - some z missing
match_events['shot_end_location_x'], match_events['shot_end_location_y'], \
    match_events['shot_end_location_z'] = np.nan, np.nan, np.nan

end_locations = np.vstack(match_events.loc[match_events.type == 'Shot'].shot_end_location.apply(
    lambda x: x if len(x) == 3 else x + [np.nan]).values)

match_events.loc[match_events.type == 'Shot', 'shot_end_location_x'] = end_locations[:, 0]
match_events.loc[match_events.type == 'Shot', 'shot_end_location_y'] = end_locations[:, 1]
match_events.loc[match_events.type == 'Shot', 'shot_end_location_z'] = end_locations[:, 2]

# clean up and choose the columns wanted
events_df = match_events[[
    'index', 'id', 'duration', 'match_id', 'minute', 'second', 'pass_angle', 'pass_height', 'pass_length', 'pass_outcome',
    'pass_recipient', 'pass_shot_assist', 'period', 'play_pattern', 'player', 'player_id', 'position', 'possession',
    'possession_team', 'possession_team_id', 'shot_type', 'shot_outcome', 'team', 'timestamp', 'type', 'location_x',
    'location_y', 'pass_end_location_x', 'pass_end_location_y', 'shot_end_location_x', 'shot_end_location_y',
    'shot_end_location_z'
]]
events_df.to_csv('match_events.csv', index=False)

formation = match_events.loc[match_events['type'] == 'Starting XI'].set_index('id', 'player')
df = formation[['tactics']]
data = df['tactics'].tolist()

n = 0
starting = pd.DataFrame(columns=['Names'])

#Print both teams lineup and export that to a CSV
for item in data:
    names = [player['player']['name'] for player in data[n]['lineup']]
    df_a = pd.DataFrame(names, columns=['Names'])
    starting = starting.append(df_a, ignore_index = True)
    n = n+1
starting.to_csv('starting.csv', index=False)

# If you need a copy of a pitch or want to create your own - check out MPLSoccer for more
pitch = pitch = Pitch(pitch_type='statsbomb', pitch_color='#ffffff', line_color='#555555')
fig, ax = pitch.draw()
fig.show()
fig.savefig('fig.png')
