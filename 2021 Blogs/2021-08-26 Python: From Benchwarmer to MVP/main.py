
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
    time.sleep(3)
    all_games = result.get_data_frames()[0]
    all_games.to_csv('Games.csv', index=False)
    game_id = all_games.iloc[:, 4]
    game_id_list = game_id.values.tolist()
    game_id_list = list(set(game_id_list))
except requests.exceptions.ReadTimeout:
    print('Timeout error for games')
    time.sleep(3)

"""Print the First Game with header"""
pbp = playbyplayv2.PlayByPlayV2(game_id_list[0])
pbp = pbp.get_data_frames()[0]
pbp.to_csv('PBP.csv', mode='w', index=False, header=True)

game_counter = 1

"""Print the remainder games without header"""
for i in game_id_list[1::]:
    try:
        pbp = playbyplayv2.PlayByPlayV2(game_id_list[game_counter])
        pbp = pbp.get_data_frames()[0]
        pbp.to_csv('PBP.csv', mode='a', index=False, header=False)
        time.sleep(3)
        print(f"{game_counter} has been exported for plays")
        game_counter = game_counter + 1
    except requests.exceptions.ReadTimeout:
        print('Timeout error for plays')
        time.sleep(3)

"""Print the first with a header"""
response = shotchartdetail.ShotChartDetail(
        team_id=0,
        player_id=0,
        game_id_nullable=game_id_list[0],
        context_measure_simple='FGA',
        season_type_all_star='Playoffs'
        )

content = json.loads(response.get_json())
results = content['resultSets'][0]
headers = results['headers']
rows = results['rowSet']
df = pd.DataFrame(rows)
df.to_csv('ShotData.csv', mode='w', index=False, header=True)


"""Find the shot details for the chosen game"""
game_counter = 1

for i in game_id_list[1::]:
    try:
        response = shotchartdetail.ShotChartDetail(
        team_id=0,
        player_id=0,
        game_id_nullable=game_id_list[game_counter],
        context_measure_simple='FGA',
        season_type_all_star='Playoffs'
        )
        content = json.loads(response.get_json())
        results = content['resultSets'][0]
        rows = results['rowSet']
        df = pd.DataFrame(rows)
        headers = results['headers']
        df.columns = headers
        df.to_csv('ShotData.csv', mode='a', index=False, header=False)
        print(f"{game_counter} has been exported for shots")
        game_counter = game_counter + 1
        time.sleep(3)
    except ValueError:
        print(f"The {game_counter} has an error for shots")
        game_counter = game_counter + 1
        time.sleep(3)
        pass
    except requests.exceptions.ReadTimeout:
        print('Timeout error for shot')
        time.sleep(3)
