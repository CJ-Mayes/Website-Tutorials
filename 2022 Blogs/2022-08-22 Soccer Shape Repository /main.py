import requests
import os

#Top 6
d={'Name':['Son Heung-Min','Mohamed Salah','Cristiano Ronaldo','Harry Kane','Sadio Mané','Jamie Vardy'],
      'ID':[186,306,874,184,304,18788],
      'photo':['https://media.api-sports.io/football/players/186.png'
              ,'https://media.api-sports.io/football/players/306.png'
              ,'https://media.api-sports.io/football/players/874.png'
              ,'https://media.api-sports.io/football/players/184.png'
              , 'https://media.api-sports.io/football/players/304.png'
              , 'https://media.api-sports.io/football/players/18788.png']
     }

players = d['ID']

n = 0

# Check if "images" folder exists, if not, create it
if not os.path.exists('./images'):
    os.mkdir('./images')

for i in players:
    # Check if image already exists, if it does, skip it
    if os.path.exists(f'./images/{players[n]}.png'):
        print(f"Player #{players[n]} already downloaded, skipping")

    else:
        # Make the request to the URL to get the image
        image = requests.get(f"https://media.api-sports.io/football/players/{players[n]}.png")

        # If the URL returns status code "200 Successful", save the image into the "images" folder.
        if image.status_code == 200:
            file = open(f"./images/{players[n]}.png", "wb+")
            file.write(image.content)
            file.close()
            print(f"Player #{players[n]} successfully downloaded!")

        # If the URL returns a status code other than "200 Successful", alert the user and don't save the image
        else:
            print(f"Player #{players[n]} returned HTTP Status {image.status_code}, skipping")

    n = n+1
