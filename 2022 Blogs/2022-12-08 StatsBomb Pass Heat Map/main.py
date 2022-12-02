from statsbombpy import sb
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# Get competitions
comp = sb.competitions()
comp.to_csv('competitions.csv', index=False)

# Get Matches - UEFA Women's Euro
df = sb.matches(competition_id=53, season_id=106)
df.to_csv('matches.csv', index=False)

# Find a match_id required
match = 3847567
df = sb.events(match_id=match)

df_pass = df.loc[(df['type'] == 'Pass') & (df['team'] == "England Women's")]

location_xy = df_pass.location.apply(pd.Series)
# Save events locations to a Series with 2 columns location_xy = df_pass.location.apply(pd. Series)
# #Rename columns to x and y
location_xy.columns = ['x', 'y']
# Drop NaN
location_xy.dropna(inplace=True)
# Pitch setup
pitch = Pitch(pitch_type='statsbomb', figsize=(16, 9), layout=(1, 4), line_zorder=2, pitch_color='#22312b', line_color='white', orientation='vertical')

# Draw the pitch
fig, ax = pitch.draw(figsize=(16, 9),  nrows=1,  ncols=4)

# 4 Heatmap variations specified by number of bins (x, y) for horizontal pitch
bins = [(1, 5), (6, 1), (6, 5), (3,2.5)]

for i, bin in enumerate(bins):
    bin_statistic = pitch.bin_statistic(location_xy.x, location_xy.y, statistic='count', bins=bin)
    pitch.heatmap(bin_statistic, ax=ax[i], cmap='RdYlBu', edgecolors='black')
    pitch.scatter(location_xy.x, location_xy.y, c='white', s=10, ax=ax[i])
    bin_statistic['statistic'] = (pd.DataFrame((bin_statistic['statistic'] / bin_statistic['statistic'].sum())).applymap(lambda x: '{:.0%}'.format(x)).values)
    pitch.label_heatmap(bin_statistic, color='black', fontsize=10, ax=ax[i], ha='center', va='bottom')

# Alternative method using mpl soccer documentation
pitch = Pitch(line_zorder=2, pitch_color='#22312b',orientation='vertical', axis= True)
fig, ax = pitch.draw()
x = location_xy.x
y = location_xy.y
stats = pitch.bin_statistic_positional(x, y)
pitch.heatmap_positional(stats, edgecolors='black', cmap='RdYlBu', ax=ax)
pitch.scatter(x, y, c='white', s=10, ax=ax)
text = pitch.label_heatmap(stats, color='black', ax=ax, fontsize=10, ha='center')

plt.show()