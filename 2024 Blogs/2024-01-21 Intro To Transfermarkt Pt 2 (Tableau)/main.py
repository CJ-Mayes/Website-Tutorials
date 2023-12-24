import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}

# Initialize empty lists to store player information
all_player_data = []

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
        # Extract player information
        player_name_tag = player_row.find('td', {'class': 'hauptlink'})
        player_position_tag = player_row.find_all('td', {'class': None})[2]
        player_age_tag = player_row.find_all('td', {'class': 'zentriert'})[2]

        player_club_tag = player_row.find_all('td', {'class': 'zentriert'})[3].find('a')
        player_club = player_club_tag['title'] if player_club_tag else None

        # Extract player position
        player_position = player_position_tag.text.strip() if player_position_tag else None

        # Extract player age
        player_age = player_age_tag.text.strip() if player_age_tag else None

        # Extract current market value from the player's profile page
        player_link_tag = player_name_tag.find('a')
        if player_link_tag:
            player_link = player_link_tag['href']
            player_page_url = f"https://www.transfermarkt.co.uk{player_link}"
            player_page_tree = requests.get(player_page_url, headers=headers)
            player_page_soup = BeautifulSoup(player_page_tree.content, 'html.parser')

            # Extract current market value
            current_value_wrapper = player_page_soup.find('a', {'class': 'data-header__market-value-wrapper'})
            if current_value_wrapper:
                current_value_text = current_value_wrapper.text.replace('€', '').replace('m', '').strip()
                # Split value and date
                current_value_parts = current_value_text.split('Last update: ')
                player_current_value = current_value_parts[0].strip() if len(current_value_parts) > 0 else None
                last_update_date = current_value_parts[1].strip() if len(current_value_parts) > 1 else None
            else:
                player_current_value = None
                last_update_date = None
        else:
            player_current_value = None
            last_update_date = None

        # Extract player values
        player_values_tags = player_row.find_all('td', {'class': 'rechts'})
        player_max_value = player_values_tags[0].find('span', {'class': 'cp'}).text.strip() if player_values_tags and len(player_values_tags) > 0 else None

        player_data = {
            'Name': player_name_tag.find('a').text.strip() if player_name_tag else None,
            'Club': player_club,
            'Position': player_position,
            'Age': player_age,
            'Current_Value': player_current_value,
            'Last_Update_Date': last_update_date,
            'Max_Value': player_max_value
        }
        all_player_data.append(player_data)

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
df = pd.DataFrame(all_player_data)

# Export the DataFrame to a CSV file
df.to_csv('player_data.csv', index=False)
