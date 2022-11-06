from sportsreference.nhl.teams import Teams
import pandas as pd

teams = Teams(2022)
df = pd.DataFrame()

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('nhl_data.xlsx', engine='xlsxwriter')

for team in teams:
    df = df.append({'name': team.name,
                    'abbreviation': team.abbreviation,
                    'team.name': team.name,
                    'average_age': team.average_age,
                    'games_played': team.games_played,
                    'goals_for': team.goals_for,
                    'losses': team.losses,
                    'overtime_losses': team.overtime_losses,
                    'penalty_killing_percentage': team.penalty_killing_percentage,
                    'points': team.points,
                    'points_percentage': team.points_percentage,
                    'power_play_goals': team.power_play_goals,
                    'power_play_goals_against': team.power_play_goals_against,
                    'power_play_opportunities': team.power_play_opportunities,
                    'power_play_opportunities_against': team.power_play_opportunities_against,
                    'power_play_percentage': team.power_play_percentage,
                    'rank': team.rank,
                    'save_percentage': team.save_percentage,
                    'shooting_percentage': team.shooting_percentage,
                    'short_handed_goals': team.short_handed_goals,
                    'short_handed_goals_against': team.short_handed_goals_against,
                    'shots_against': team.shots_against,
                    'shots_on_goal': team.shots_on_goal,
                    'simple_rating_system': team.simple_rating_system,
                    'strength_of_schedule': team.strength_of_schedule,
                    'wins': team.wins
                    }, ignore_index=True)

df.to_excel(writer, sheet_name='2022')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
exit()
