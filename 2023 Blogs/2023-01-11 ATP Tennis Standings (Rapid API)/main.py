import requests
import json
import pandas as pd

# set the endpoint URL and headers
endpoint = "https://tennisapi1.p.rapidapi.com/api/tennis/rankings/atp"

headers = {
    "X-RapidAPI-Key": "Redacted please change KEY.....",
    "X-RapidAPI-Host": "tennisapi1.p.rapidapi.com"
}

# send a GET request to the endpoint
response = requests.get(endpoint, headers=headers)
print(response)

# convert the json response to a python dictionary
data = json.loads(response.text)
print(data)

rank_list = []
name_list = []
points_list = []

a = 0

    # loop through the data and write the values to the csv file
for item in data['rankings']:
    # access the first item in the rankings list
    ranking = data['rankings'][a]
    # access the name
    name = ranking['rowName']
    # access the ranking
    rank = ranking['ranking']
    # access the points
    points = ranking['points']
    # print the details
    print("Name:", name)
    print("Ranking:", rank)
    print("Points:", points)
    rank_list.append(rank)
    name_list.append(name)
    points_list.append(points)
    a = a + 1

# Calling DataFrame constructor after zipping
# both lists, with columns specified
df = pd.DataFrame(list(zip(rank_list, name_list, points_list)),
                  columns=['Rank', 'Name', 'Points'])
df.to_csv(r'ATP_rankings.csv', index=False)

print("ATP Rankings successfully written to ATP_rankings.csv")
