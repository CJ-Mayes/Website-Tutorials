"""
This code is designed for beginners using Understat. It will not express best practice
in python coding but serves as a basis for those wanting to find their own datasets
"""
from understatapi import UnderstatClient

understat = UnderstatClient()

print('Please make sure you type the answer EXACTLY as seen as below: capitals letters/underscores')
print('EPL, La_Liga, Bundesliga, Serie_A, Ligue_1, RFPL')

League_choice = input("What league would you like to look at? Type one:\n")

print('What season would you like to look at? Type as YYYY (E.g:2019)')
season_choice = input("Pick a season:\n")

# get data for every player playing in the Premier League in 2020/21
league_player_data = understat.league(league=League_choice).get_player_data(season=season_choice)

# Print into an excel document all the league player data
df = league_player_data
df.to_csv(r'league_player_data.csv', index=False)

player_id = league_player_data["id"]
teams = league_player_data["team_title"]
myset = set(teams)

print(f'There are {player_id.count()} players in the league for the chosen season')

# Get data for every shot the player has taken in a league match (for chosen season)
player_ct = 0
#The counter will print increasing values of 1 until it loops through all the players in the league
with open("player_shot_data.csv", "w") as myfile:
    for i in player_id:
        df2 = understat.player(player=player_id[player_ct]).get_shot_data()
        if player_ct == 0:
            df_filtered = df2[df2['season'] == season_choice]
            df3 = df_filtered.loc[df_filtered['h_team'].isin(myset)]
            df3.to_csv("player_shot_data.csv", mode='a', header=True, index=False)
            player_ct = player_ct + 1
            print(player_ct)
        elif df2.shape[0] == 0:
            print('DataFrame is empty')
            player_ct = player_ct + 1
            print(player_ct)
        else:
            df_filtered = df2[df2['season'] == season_choice]
            df3 = df_filtered.loc[df_filtered['h_team'].isin(myset)]
            player_ct = player_ct + 1
            print(player_ct)
            df3.to_csv("player_shot_data.csv", mode='a', header=False, index=False)
