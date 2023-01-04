import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

# replace variables with values for your account
# Leave grant type as 'refresh_token'
payload = {
    'client_id': "xxxxx",
    'client_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'refresh_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']

print("Access Token = {}\n".format(access_token))
header = {'Authorization': 'Bearer ' + access_token}

# First loop starts on page 1.
# It will then loop through any further pages required.
request_page_num = 1
all_activities = []

while True:
    param = {'per_page': 200, 'page': request_page_num}
    # initial request, where we request the first page of activities - 200 per page
    my_dataset = requests.get(activites_url, headers=header, params=param).json()

    # If the response is empty we will leave the loop, otherwise we will keep collecting data
    if len(my_dataset) == 0:
        print("No more activities")
        break

    # If the all_activities populated, continue
    if all_activities:
        print("all_activities populated")
        all_activities.extend(my_dataset)

    # Create all activities from the dataset
    else:
        print("all_activities is needing to be populated")
        all_activities = my_dataset

    request_page_num += 1

import pandas as pd

df = pd.DataFrame(all_activities)

# Check dataframe has been created
print(df)
# Create Dataset
df.to_csv(r'Strava_data.csv', index=False, header=True)
