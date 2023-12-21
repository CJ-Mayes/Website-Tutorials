import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}

# Initialize empty lists to store player information and teams
all_player_data = []

# Initial page
base_url = "https://www.transfermarkt.co.uk/premier-league/transfers/wettbewerb/GB1/plus/?saison_id=2022&s_w=w&leihe=1&intern=0&intern=1"

pageTree = requests.get(base_url, headers=headers)
soup = BeautifulSoup(pageTree.content, 'html.parser')

# Extract teams from the page and filter out empty strings
teams = soup.select('h2.content-box-headline a')
teams_list = [team.text.strip() for team in teams if team.text.strip()]

# Function to extract player information for a given team
def extract_player_data(team_name, team_div, transfer_type):
    transfer_table = team_div.find_all('table')

    # Use the first table for incoming transfers and the second for outgoing transfers
    if transfer_table and len(transfer_table) >= 2:
        headers = [th.text.strip() for th in transfer_table[transfer_type].find('thead').find_all('th')]
        rows = transfer_table[transfer_type].find('tbody').find_all('tr')

        for row in rows:
            data = [td.text.strip() for td in row.find_all('td')]
            player_data = [team_name, 'In' if transfer_type == 0 else 'Out'] + data
            all_player_data.append(player_data)

# Iterate through each team and extract player information for both incoming and outgoing transfers
for team_name in teams_list:
    team_anchor = soup.find('a', text=team_name)
    team_div = team_anchor.find_parent('div', class_='box') if team_anchor else None

    # Check if the team_div is found
    if team_div:
        # Extract incoming transfers
        extract_player_data(team_name, team_div, transfer_type=0)

        # Extract outgoing transfers
        extract_player_data(team_name, team_div, transfer_type=1)

# Create a DataFrame from the collected player data
columns = ['Team', 'Transfer Direction', 'Player', 'Age', 'Nationality', 'Position', 'Short Position', 'Market Value', 'Left Team', 'Left Team Flag', 'Fee']
df = pd.DataFrame(all_player_data, columns=columns)

# Display the DataFrame
print(df)

# Export the DataFrame to a CSV file
df.to_csv('transfer_data.csv', index=False)
