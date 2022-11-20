"""
pip install statsbombpy
pip install pandas
pip install numpy
"""

from statsbombpy import sb
import pandas as pd
from pandas import json_normalize
import numpy as np

# Get competitions
comp = sb.competitions()
comp.to_csv('competitions.csv', index=False)

# Get Matches from WSL - 2020/21
df = sb.matches(competition_id=37, season_id=90)
df.to_csv('matches.csv', index=False)

# Find a match_id required
match = 3764235
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
    'index', 'id', 'duration', 'match_id', 'minute', 'pass_angle', 'pass_height', 'pass_length', 'pass_outcome',
    'pass_recipient', 'pass_shot_assist', 'period', 'play_pattern', 'player', 'player_id', 'position', 'possession',
    'possession_team', 'possession_team_id', 'shot_type', 'shot_outcome', 'team', 'timestamp', 'type', 'location_x',
    'location_y', 'pass_end_location_x', 'pass_end_location_y', 'shot_end_location_x', 'shot_end_location_y',
    'shot_end_location_z'
]]
events_df.to_csv('match_events.csv', index=False)

# create separate data sheet with freeze frame
shots = match_events.loc[match_events['type'] == 'Shot'].set_index('id', 'match')

shot_freeze_frame = match_events['shot_freeze_frame']

ffs = {}

for id_, row in shots.iterrows():
    try:
        ff = json_normalize(row.shot_freeze_frame, sep="_")
        ff = ff.assign(x=ff.apply(lambda x: x.location[0], axis=1)). \
            assign(y=ff.apply(lambda x: x.location[1], axis=1)). \
            drop('location', axis=1). \
            assign(id=id_)
        ffs[id_] = ff
    except:
        pass

# concatenate all the Freeze Frame dataframes
ff_df = pd.concat(ffs)
ff_df.to_csv('match_shot_freeze_frames.csv', index=False)
