# Make sure you have downloaded the appropriate version of Chrome WebDriver from
# https://sites.google.com/a/chromium.org/chromedriver/downloads

DRIVER_PATH = r"C:\Users\Cj.Mayes\insertyourpath\chromedriver.exe"
import html

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

options = webdriver.ChromeOptions()
# Set any additional options as needed
# For example, to run Chrome headless:
# options.add_argument("--headless")

driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)

driver.get("https://www.tennisabstract.com/charting/20240602-W-Roland_Garros-R16-Iga_Swiatek-Anastasia_Potapova.html")

# Wait for 10 seconds until the element is visible and clickable
wait = WebDriverWait(driver, 10)
button = wait.until(EC.element_to_be_clickable((By.ID, "pointlog")))

# Click the button element
button.click()

# Now that the page content has loaded, capture the page source
html_content = driver.page_source
driver.quit()  # Ensure the driver is closed after fetching the data

soup = BeautifulSoup(html_content, 'html.parser')

# Find the table. Assuming 'forecast' is the correct id based on the context you've provided; if not, adjust as needed
forecast_table = soup.find('span', id='forecast').find('table')

data = []  # Will hold our extracted data

for row in forecast_table.find_all('tr')[1:]:  # Process the rows in the table, skipping the header row
    cols = row.find_all('td')

    if len(cols) == 5:  # Ensure the row has the expected number of columns
        server = html.unescape(cols[0].text.strip())
        sets = html.unescape(cols[1].text.strip())
        games = html.unescape(cols[2].text.strip())
        points = html.unescape(cols[3].text.strip())
        commentary = html.unescape(cols[4].text.strip())

        data.append({
            'Server': server,
            'Sets': sets,
            'Games': games,
            'Points': points,
            'Commentary': commentary
        })

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

# Optionally, before exporting, you can further clean up if you suspect additional HTML entities or specific formats
# For spaces, the html.unescape should generally cover it, but here's an example of manual replacement
# df = df.applymap(lambda text: text.replace(u'\xa0', ' ') if isinstance(text, str) else text)

df.replace({'\xa0': ' ', '&nbsp;': ' '}, regex=True, inplace=True)

# Now, exporting the cleaned DataFrame to a text file
df.to_csv('points_data.txt', index=False, sep='\t', encoding='UTF-8')

# Notes:
# - Ensure Selenium, BeautifulSoup, and pandas are installed in your environment.
# - Confirm the correct WebDriver path and web page URL.
# - This script clicks a button to load the table, so ensure the ID used for clicking is correct.
