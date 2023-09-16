"""
https://statsbomb.com/news/statsbomb-release-free-2023-womens-world-cup-data/
the competition id (72) and season id (107) to pull the data.
"""

from statsbombpy import sb

# Get competitions
comp = sb.competitions()
comp.to_csv('competitions.csv', index=False)

#Get Matches
df = sb.matches(competition_id=72, season_id=107)
df.to_csv('matches.csv', index=False)

# Find a match_id required - final WWC
match = 3906390
match_events = sb.events(match_id=match)
match_events.to_csv('match_events.csv', index=False)

# Find freeze frames
match_frames = sb.frames(match_id=match, fmt='dataframe')
match_frames.to_csv('match_frames.csv', index=False)
