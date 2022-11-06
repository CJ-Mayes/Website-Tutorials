from bs4 import BeautifulSoup
import requests
import pandas as pd

url = input('What is the url of the race you want to copy?')
req = requests.get(url)

soup = BeautifulSoup(req.text, "html.parser")
table_body = soup.find(id="gc")

df_rows = []

rows = table_body.find_all('tr')
for row in rows:
    row_all = row.find_all('td')
    row_clean = [x.text.strip() for x in row_all]
    if len(row_clean) == 0:
        print('the list is empty')
    else:
        df_rows.append(row_clean)

header = ["Position", "Born", "Nationality", "Name","Team","UCI","Time"]

df = pd.DataFrame.from_records(df_rows, columns=header)
print(df)

df.to_csv('Table.csv', index=False)
df.to_csv(r'Text_Table.txt', header=header, index=None, sep=' ', mode='w')
