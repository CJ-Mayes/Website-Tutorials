"""
https://statsbomb.com/news/statsbomb-release-free-2023-womens-world-cup-data/
the competition id (72) and season id (107) to pull the data.
"""
import ast
import json

from statsbombpy import sb
import pandas as pd

# Get competitions
comp = sb.competitions()
#comp.to_csv('competitions.csv', index=False)

#Get Matches
df = sb.matches(competition_id=72, season_id=107)
#df.to_csv('matches.csv', index=False)

# Find a match_id required - final WWC
match = 3906390
match_events = sb.events(match_id=match)
#print(match_events)
#match_events.to_csv('match_events.csv', index=False)

# Find freeze frames
match_frames = sb.frames(match_id=match, fmt='dataframe')
#match_frames.to_csv('match_frames.csv', index=False)


# Create a DataFrame
df = pd.DataFrame(match_frames)

# Create a list to store the new rows
new_rows = []

# Iterate through the DataFrame
for index, row in df.iterrows():
    visible_area = row['visible_area']
    location = row['location']

    # Split the visible_area list into x and y coordinates
    for i in range(0, len(visible_area), 2):
        x = visible_area[i]
        y = visible_area[i + 1]

        new_row = {
            'id': row['id'],
            'x': x,
            'y': y,
            'match_id': row['match_id'],
            'teammate': row['teammate'],
            'actor': row['actor'],
            'keeper': row['keeper'],
            'location': location
        }

        new_rows.append(new_row)

# Create a new DataFrame from the list of new rows
new_df = pd.DataFrame(new_rows)

# Reset the index of the new DataFrame
new_df.reset_index(drop=True, inplace=True)

# Print the new DataFrame
new_df.to_csv('visibility_data.csv', index=False)
