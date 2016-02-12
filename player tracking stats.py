import requests
import json
import pandas as pd
import numpy as np

# Passing stats per game
url_pass = 'http://stats.nba.com/js/data/sportvu/2014/passingData.json'
resp = requests.get(url_pass)
data = json.loads(resp.text)
passes = pd.DataFrame(data['resultSets'][0]['rowSet'], columns=data['resultSets'][0]['headers'])
passes = passes[passes.TEAM_ABBREVIATION != 'TOTAL']
passes['PASS_TOT'] = passes.PASS * passes.GP

teams = pd.read_csv('C:/Users/Chris/Documents/Kaydabi/Team abbreviations.csv')
passes = pd.merge(teams, passes, on='TEAM_ABBREVIATION', how='outer')

team_pass = pd.DataFrame(passes.groupby('TEAM_NAME').PASS_TOT.sum())
team_pass['PASS_GAME'] = team_pass.PASS_TOT / 82
team_pass['TEAM_NAME'] = team_pass.index

# Miscellaneous stats per possession
url_misc_poss = 'http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Misc&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerPossession&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision='
resp = requests.get(url_misc_poss)
data = json.loads(resp.text)
misc_poss = pd.DataFrame(data['resultSets'][0]['rowSet'], columns=data['resultSets'][0]['headers'])

# Miscellaneous stats totals
url_misc_total = 'http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Misc&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision='
resp = requests.get(url_misc_total)
data = json.loads(resp.text)
misc_total = pd.DataFrame(data['resultSets'][0]['rowSet'], columns=data['resultSets'][0]['headers'])

misc_poss['POSS'] = (misc_total.MIN / misc_poss.MIN) / 82

team_pass = pd.merge(team_pass, misc_poss, on='TEAM_NAME', how='outer')
team_pass['PASS_POSS'] = team_pass.PASS_GAME / team_pass.POSS

team_pass.PASS_POSS.mean()