import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}

# Initialize empty lists to store player names and values
all_player_names = []
all_player_values = []

# Initial page
base_url = "https://www.transfermarkt.co.uk/premier-league/marktwerte/wettbewerb/GB1/pos//detailpos/0/altersklasse/alle/plus/1"
pageTree = requests.get(base_url, headers=headers)
soup = BeautifulSoup(pageTree.content, 'html.parser')

# Number of pages to iterate through (adjust this based on the actual number of pages)
num_pages = 5

for page_number in range(1, num_pages + 1):
    # Find all player rows in the table
    player_rows = soup.find_all('tr', {'class': ['odd', 'even']})

    # Iterate through each player row
    for player_row in player_rows:
        # Extract player name
        player_name_tag = player_row.find('td', {'class': 'hauptlink'})
        player_name = player_name_tag.find('a').text.strip() if player_name_tag else None
        all_player_names.append(player_name)

        # Extract player value
        player_value_tag = player_row.find('td', {'class': 'rechts'})
        player_value = player_value_tag.span.text.strip() if player_value_tag else None
        all_player_values.append(player_value)

    # Find the link to the next page
    next_page_link = soup.find('a', {'class': 'tm-pagination__link', 'title': f'Page {page_number + 1}'})

    # Break the loop if there is no next page link
    if not next_page_link:
        break

    # Construct the URL for the next page
    next_page_url = base_url + next_page_link['href']
    pageTree = requests.get(next_page_url, headers=headers)
    soup = BeautifulSoup(pageTree.content, 'html.parser')

# Create a DataFrame to store the data
df = pd.DataFrame({'Player Name': all_player_names, 'Player Value': all_player_values})

# Export the DataFrame to a CSV file
df.to_csv('player_data.csv', index=False)
