import requests
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import playbyplayv2
from nba_api.stats.endpoints import shotchartdetail
import json
import pandas as pd
import time

"""Get the games so we can choose what one we want to look at"""
try:
    result = leaguegamefinder.LeagueGameFinder(
        season_nullable='2020-21',
        season_type_nullable="Playoffs"
    )
    time.sleep(5)
except requests.exceptions.ReadTimeout:
    print('Timeout error for games')
    time.sleep(5)

"""Export the games to CSV"""
all_games = result.get_data_frames()[0]
all_games.to_csv('Games.csv', index=False)

"""Take an example Game_ID from the Games CSV"""
game_id = '0042000406'

"""Print the Play by Play"""
try:
    pbp = playbyplayv2.PlayByPlayV2(game_id)
    pbp = pbp.get_data_frames()[0]
    pbp.to_csv('PBP.csv', mode='w', index=False, header=True)
    time.sleep(5)
except requests.exceptions.ReadTimeout:
    print('Timeout error for plays')
    time.sleep(5)

"""Find the shot details for the chosen game"""
try:
    response = shotchartdetail.ShotChartDetail(
        team_id=0,  # When set to zero it takes all teams
        player_id=0,  # When set to zero it takes all players
        game_id_nullable='0042000406', # 10 digit value
        context_measure_simple='FGA',  # All shots, Default is 'PTS' (Shots Made)
        season_type_all_star='Playoffs'
    )
    content = json.loads(response.get_json())
except requests.exceptions.ReadTimeout:
    print('Timeout error for shots')
    time.sleep(5)

"""Transform shot data contents into dataframe"""
results = content['resultSets'][0]
headers = results['headers']
rows = results['rowSet']
df = pd.DataFrame(rows)
df.columns = headers

"""Write Shot location to CSV"""
df.to_csv('ShotData.csv', index=False)
