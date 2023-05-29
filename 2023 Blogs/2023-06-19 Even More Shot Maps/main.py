"""
This code is designed for beginners using Understat. It will not express best practice
in python coding but serves as a basis for those wanting to find their own datasets
"""
import pandas as pd
from understatapi import UnderstatClient

understat = UnderstatClient()

league_choice = 'EPL'
season_choice = '2022'
league_player_data = understat.league(league=league_choice).get_player_data(season=season_choice)

# Convert list to dataframe to get league data for chosen league and season
df = pd.DataFrame(league_player_data, columns=['id', 'player_name', 'games','time', 'goals', 'xG', 'assists'
                                               , 'xA', 'shots', 'key_passes', 'yellow_cards', 'red_cards', 'position'
                                               , 'team_title', 'npg', 'npxG', 'xGChain', 'xGBuildup'])
df.to_csv(r'league_player_data.csv', index=False)

player_id = df["id"]
print(f'There are {player_id.count()} players in the league for the chosen season')

# Get data for every shot the player has taken in a league match (for chosen season)
player_ct = 0

""" This data looks at the number of players in the league, It will not filter the season or teams.
This means: 
> Player A that plays in the premier league in the chosen season.
> Player A's shot data will then be accumulated across all understat seasons.
> This means if Player A was in a different league in the previous year that data will pull through.
> Please filter to current season and the h_teams you are after!
"""

for i in range(0,554):
    df2 = understat.player(player=player_id[player_ct]).get_shot_data()
    df4 = pd.DataFrame(df2, columns=['id', 'minute', 'result', 'Goal', 'X', 'Y', 'xG'
                , 'player', 'h_a', 'player_id', 'situation', 'season', 'shotType'
                , 'match_id', 'h_team', 'a_team', 'h_goals', 'a_goals', 'date',
                                        'player_assisted', 'last_action'])
    df4.to_csv('player_shot_data_all_comp.csv', mode='a', header=True)
    player_ct = player_ct + 1
    print(player_ct)
