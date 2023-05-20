import requests
import pandas as pd
import datetime
from datetime import timedelta
 
# Get yesterday's date
yesterday = datetime.date.today() - timedelta(1)

# Get today's date
today = datetime.date.today()

# Set the base URL for the NHL API
base_url = "https://statsapi.web.nhl.com/api/v1"

# Set the endpoint for the teams
teams_endpoint = "/teams"

# Send a GET request to the NHL API
response = requests.get(base_url + teams_endpoint)

# Parse the response as a dictionary
response_dict = response.json()

# Create an empty list to store the team ids
team_id_list = []

# Iterate over the teams in the response
for team in response_dict['teams']:
    # Extract the team id
    team_id = team['id']

    # Append the team id to the team_id_list
    team_id_list.append(team_id)

# Create a set of the team ids
team_id_set = set(team_id_list)

# Convert the set to a list
team_id_list = list(team_id_set)

# Create an empty list to store the gamePk values
gamePk_list = []

# Iterate over the team ids in the team_id_list
for team_id in team_id_list:
    # Set the endpoint for the specific team
    team_endpoint = f"/schedule?startDate=2022-10-07&endDate={yesterday}&teamId={team_id}"

    # Send a GET request to the NHL API
    response = requests.get(base_url + team_endpoint)

    # Parse the response as a dictionary
    response_dict = response.json()

    # Iterate over the games in the response
    for game in response_dict['dates']:
        # Extract the gamePk value
        gamePk = game['games'][0]['gamePk']

        # Append the gamePk value to the gamePk_list
        gamePk_list.append(gamePk)

# Create a set of the gamePk values
gamePk_set = set(gamePk_list)

# Convert the set to a list
gamePk_list = list(gamePk_set)

    # Read the csv file into a dataframe
    # existing_df = pd.read_csv('nhl_play_by_play_data_all_games.csv')

    # Create a set of the gamePk values in the existing dataframe
    # existing_gamePk_set = set(existing_df['gamePk'])

# Create an empty dataframe to store the plays data
plays_df = pd.DataFrame()

# Iterate over the gamePk values in the gamePk_list
for gamePk in gamePk_list:

    # Set the endpoint for the specific game
    game_endpoint = f"/game/{gamePk}/feed/live"

    # Send a GET request to the NHL API
    response = requests.get(base_url + game_endpoint)

    # Parse the response as a dictionary
    response_dict = response.json()

    # Get the game type from the response dictionary
    game_type = response_dict['gameData']['game']['type']

    # Get the season from the response dictionary
    season = response_dict['gameData']['game']['season']

    # Get the away team from the response dictionary
    away_team = response_dict['gameData']['teams']['away']['name']

    # Get the home team from the response dictionary
    home_team = response_dict['gameData']['teams']['home']['name']

    # Get the venue played from the response dictionary
    venue = response_dict['gameData']['teams']['home']['venue']['name']

    # Create a temporary Pandas dataframe from the plays data
    temp_plays_df = pd.json_normalize(response_dict['liveData']['plays']['allPlays'])

    # Add the game type and gamePk columns to temp_plays_df
    temp_plays_df['game_type'] = game_type
    temp_plays_df['season'] = season
    temp_plays_df['gamePk'] = gamePk
    temp_plays_df['home_team'] = home_team
    temp_plays_df['away_team'] = away_team
    temp_plays_df['venue_played'] = venue

    # Define a function to extract the players data to a new dataframe
    def extract_players(row):
        # Check if the players column is a list
        if not isinstance(row['players'], list):
            # Return an empty dataframe
            return pd.DataFrame()

        # Create an empty dataframe to store the player data
        player_data = pd.DataFrame(columns=['about.eventIdx', 'player_id', 'player_name', 'player_type'])

        # Iterate over the players in the list
        for player in row['players']:
            # Extract the player's data
            eventIdx = row['about.eventIdx']
            player_id = player['player']['id']
            player_name = player['player']['fullName']
            player_type = player['playerType']

            # Append a row containing the player's data to the player_data dataframe
            player_data = player_data.append({
                'about.eventIdx': eventIdx,
                'player_id': player_id,
                'player_name': player_name,
                'player_type': player_type
            }, ignore_index=True)

        # Return the player_data dataframe
        return player_data

    # Check if temp_plays_df is empty
    if temp_plays_df.empty:
        # Return an empty dataframe
        temp_players_df = pd.DataFrame()
    else:
        # Apply the extract_players function to the temp_plays_df dataframe and store the results
        temp_players_df = temp_plays_df.apply(extract_players, axis=1)
            
        # Combine the dataframes in the temp_players_df Series into a single dataframe
        temp_players_df = pd.concat(temp_players_df.values, axis=0).reset_index(drop=True)

        # Drop the players column from the temp_plays_df dataframe
        temp_plays_df = temp_plays_df.drop(columns=['players'])

        # Join the temp_plays_df and temp_players_df dataframes
        temp_plays_df = temp_plays_df.merge(temp_players_df, on=['about.eventIdx'], how='outer')

        # Create a Pandas dataframe from response_dict['gameData']['players'] using pd.json_normalize()
        players_df = pd.json_normalize(response_dict['gameData']['players'])

        # Create a dataframe of all ID columns
        unique_id = players_df.columns.str.extract('(ID[^.]*)').values.tolist()

        # Create a list from the data frame
        unique_id_list = [item for sublist in unique_id for item in sublist]

        # Deduplicate the list by converting it to a set then back to a list
        unique_id = list(set(unique_id_list))

        # Initialize an empty list to store the player data
        player_data = []

    # Iterate over each unique ID in unique_id
    for player_id in unique_id:
        # Extract the player data from the response dictionary
        player_info = response_dict['gameData']['players'][player_id]
                    
        # Append the player data to the player_data list
        player_data.append(player_info)

    # Convert the player_data list to a Pandas dataframe
    players_df = pd.json_normalize(player_data)

    players_df = players_df.add_prefix('player_')

    # Merge the player data with players_df
    temp_plays_df = temp_plays_df.merge(players_df, on=['player_id'], how='outer')

    # Drop all rows in temp_plays_df that don't have a result.eventCode
    temp_plays_df = temp_plays_df.dropna(subset=['result.eventCode'])

    # Append the data from the current game to the plays_df dataframe
    plays_df = plays_df.append(temp_plays_df)

# Export the data to a CSV file
plays_df.to_csv('nhl_play_by_play_data_all_games.csv')
