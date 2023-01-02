#pip install lxml - you will need a parser
# Install all the packages below
#Thanks to Mckay Johns for the original code

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

#scrape a single game shots. We will allow users to enter a base url
base_url = 'https://understat.com/match/'
match = '18362'
url = base_url+match

#Use requests to get the webpage and BeautifulSoup to parse the page
res = requests.get(url)
soup = BeautifulSoup(res.content, 'lxml')
scripts = soup.find_all('script')

#get only the shotsData from the script
strings = scripts[1].string

# strip unnecessary symbols and get only JSON data
ind_start = strings.index("('")+2
ind_end = strings.index("')")
json_data = strings[ind_start:ind_end]
json_data = json_data.encode('utf8').decode('unicode_escape')

#convert string to json format
data = json.loads(json_data)
print(data)

x = []
y = []
xG = []
result = []
team = []
data_away = data['a']
data_home = data['h']
minute = []
shotType = []
player = []
match_id = []
situation = []
player_assisted = []
lastAction = []

for index in range(len(data_home)):
    for key in data_home[index]:
        if key == 'X':
            x.append(data_home[index][key])
        if key == 'Y':
            y.append(data_home[index][key])
        if key == 'h_team':
            team.append(data_home[index][key])
        if key == 'xG':
            xG.append(data_home[index][key])
        if key == 'result':
            result.append(data_home[index][key])
        if key == 'minute':
            minute.append(data_home[index][key])
        if key == 'shotType':
            shotType.append(data_home[index][key])
        if key == 'player':
            player.append(data_home[index][key])
        if key == 'match_id':
            match_id.append(data_home[index][key])
        if key == 'situation':
            situation.append(data_home[index][key])
        if key == 'player_assisted':
            player_assisted.append(data_home[index][key])
        if key == 'lastAction':
            lastAction.append(data_home[index][key])

for index in range(len(data_away)):
    for key in data_away[index]:
        if key == 'X':
            x.append(data_away[index][key])
        if key == 'Y':
            y.append(data_away[index][key])
        if key == 'a_team':
            team.append(data_away[index][key])
        if key == 'xG':
            xG.append(data_away[index][key])
        if key == 'result':
            result.append(data_away[index][key])
        if key == 'minute':
            minute.append(data_away[index][key])
        if key == 'shotType':
            shotType.append(data_away[index][key])
        if key == 'player':
            player.append(data_away[index][key])
        if key == 'match_id':
            match_id.append(data_away[index][key])
        if key == 'situation':
            situation.append(data_away[index][key])
        if key == 'player_assisted':
            player_assisted.append(data_away[index][key])
        if key == 'lastAction':
            lastAction.append(data_away[index][key])

col_names = ['x','y','xG','result','team','minute','shotType','player','match_id','situation','player_assisted','lastAction']
df = pd.DataFrame([x,y,xG,result,team,minute,shotType,player,match_id,situation,player_assisted,lastAction],index=col_names)
df = df.T

df.to_csv(r'data.csv', index=False, header=True)
