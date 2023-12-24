import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from statsbombpy import sb
from mplsoccer import Pitch, Sbopen
import os

# Get competitions
comp = sb.competitions()

# Find a match_id required
match_id = 3906390
match_events = sb.events(match_id=match_id)

# Filter frames to include only frames when a shot was taken
shot_frame_ids = match_events[match_events['type'] == 'Shot']['id'].unique()
frames, visible = Sbopen().frame(match_id)
print(frames)
frames_details = pd.DataFrame()

# Specify the absolute path to the folder where the images will be saved
output_folder = os.path.abspath("output_frames")

# Create the output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Dataframe to store frame details
frames_details = pd.DataFrame()

# Draw plot for each shot frame and save as an image
for idx, frame_id in enumerate(shot_frame_ids):
    frame_data = frames[frames['id'] == frame_id].copy()  # Make a copy to avoid SettingWithCopyWarning
    teammate_locs = frame_data[frame_data.teammate]
    opponent_locs = frame_data[~frame_data.teammate]

    # Check if 'visible_area' is available for the current frame
    if frame_id in visible['id'].unique():
        visible_area_data = visible[visible['id'] == frame_id].visible_area.values
        if len(visible_area_data) > 0:
            visible_area = np.array(visible_area_data[0]).reshape(-1, 2)

            # Draw plot
            p = Pitch(pitch_type='statsbomb')
            fig, ax = p.draw(figsize=(12, 8))

            # Plot Voronoi
            team1, team2 = p.voronoi(frame_data.x, frame_data.y, frame_data.teammate)
            t1 = p.polygon(team1, ax=ax, fc='red', ec='white', lw=3, alpha=0.4)
            t2 = p.polygon(team2, ax=ax, fc='grey', ec='white', lw=3, alpha=0.4)

            # Plot players
            sc1 = p.scatter(teammate_locs.x.iloc[0:], teammate_locs.y.iloc[0:], c='grey', s=80, ec='k', ax=ax)
            sc2 = p.scatter(opponent_locs.x, opponent_locs.y, c='red', s=80, ec='k', ax=ax)

            # Plot the first player with a slightly bigger size
            sc3 = p.scatter(teammate_locs.x.iloc[0], teammate_locs.y.iloc[0], c='None', edgecolors='black', s=120, linewidths=2, ax=ax)


            # Plot the visible area with the same colors
            visible_polygon = p.polygon([visible_area], color='None', ec='k', linestyle='--', lw=2, ax=ax)
            for p1 in t1:
                p1.set_clip_path(visible_polygon[0])
                p1.set_facecolor('grey')  # Team color
                p1.set_edgecolor('white')
            for p2 in t2:
                p2.set_clip_path(visible_polygon[0])
                p2.set_facecolor('red')
                p2.set_edgecolor('white')

            plt.title(f'Frame ID: {frame_id}')

            # Save the figure with an index in the filename
            output_path = os.path.join(output_folder, f"frame_{idx}_{frame_id}.png")
            plt.savefig(output_path, bbox_inches='tight')
            plt.close()
        else:
            print(f"No 'visible_area' information for Frame ID: {frame_id}")
    else:
        print(f"No visibility information for Frame ID: {frame_id}")

