import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the Selenium WebDriver with the Microsoft Edge driver
driver = webdriver.Edge()  # Assumes msedgedriver.exe is in a directory included in the system PATH environment variable

# Navigate to the page
url = 'https://www.darts24.com/match/Wbsu8DF5/#/match-summary/match-summary'
driver.get(url)

# Wait for the parent element that contains the dart throw rows to be present
dart_throws_container = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'matchHistoryRowWrapper'))
)

# Extract the dart throw rows
dart_throw_rows = dart_throws_container.find_elements(By.CLASS_NAME, 'matchHistoryRow__dartThrows')


# Function to check if a score is a high throw (140 or 180)
def is_high_throw(score):
    return score == '140' or score == '180'


# Create a CSV file to store the data
csv_file = open('dart_throws.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Leg', 'Player 1', 'Player 2', 'High_Throw_Flag'])  # Write the header row

leg_num = 1  # Leg index

# Extract and write the dart throw data to the CSV file
for row in dart_throw_rows:
    dart_throws = row.text.split(',')

    for dart_throw in dart_throws:
        p1_score, p2_score = map(str.strip, dart_throw.strip().split(':'))

        player1_score = re.sub(r'[^\d]', '', p1_score)  # Remove non-digit characters from player 1's score
        player2_score = re.sub(r'[^\d]', '', p2_score)  # Remove non-digit characters from player 2's score

        if player2_score.endswith('140') or player2_score.endswith('180'):
            high_throw_flag = player2_score[-3:]
            player2_trimmed_score = player2_score[:-3]
        else:
            high_throw_flag = ""
            player2_trimmed_score = player2_score

        csv_writer.writerow([leg_num, player1_score, player2_trimmed_score, high_throw_flag])

    leg_num += 1

# Close the CSV file
csv_file.close()

# Close the browser
driver.quit()
