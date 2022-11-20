from cricscraper.cricinfo import CricInfo
import pandas as pd

match = CricInfo("1289634")

match_name = match.match_name()
match_dates = match.match_dates()


# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('match_data.xlsx', engine='xlsxwriter')

match_playing11 = match.playing11()
match_playing11.to_excel(writer, sheet_name='match_playing11')

# Write each dataframe to a different worksheet.
match_summary = match.summary()
match_summary[0].to_excel(writer, sheet_name='match_summary')
match_summary[1].to_excel(writer, sheet_name='match_summary1')

# Write each dataframe to a different worksheet.
match_scorecard = match.scorecard()
match_scorecard[0].to_excel(writer, sheet_name='match_scorecard1')
match_scorecard[1].to_excel(writer, sheet_name='match_scorecard2')
match_scorecard[2].to_excel(writer, sheet_name='match_scorecard3')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
exit()
