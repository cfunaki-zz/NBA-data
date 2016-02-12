import pandas as pd
import numpy as np
import math

directory = "C:/Users/Chris/Documents/Shot charts"
year = 2015

shots_raw = pd.read_csv('%s/NBA data project/raw_data/%d_shots_raw.csv' % (directory, year),
                        names=["GRID_TYPE", "GAME_ID", "GAME_EVENT_ID", "PLAYER_ID", "PLAYER_NAME",
                        "TEAM_ID", "TEAM_NAME", "PERIOD", "MINUTES_REMAINING", "SECONDS_REMAINING",
                        "EVENT_TYPE", "ACTION_TYPE", "SHOT_TYPE", "SHOT_ZONE_BASIC", "SHOT_ZONE_AREA",
                        "SHOT_ZONE_RANGE", "SHOT_DISTANCE", "LOC_X", "LOC_Y", "SHOT_ATTEMPTED_FLAG", "SHOT_MADE_FLAG"])

# Convert minutes to seconds
shots_raw['SECONDS'] = (shots_raw['MINUTES_REMAINING'] * 60) + shots_raw['SECONDS_REMAINING']

# Points per basket
shots_raw.loc[[shots_raw['SHOT_TYPE'] == '3PT Field Goal'], 'SHOT_TYPE'] = 3
shots_raw.loc[[shots_raw['SHOT_TYPE'] == '2PT Field Goal'], 'SHOT_TYPE'] = 2

# Create dictionary for each gameid and the teams involved
games = {}
gameids = np.unique(shots_raw['GAME_ID'].values.ravel())
for gameid in gameids:
    teams = shots_raw['TEAM_NAME'][shots_raw['GAME_ID'] == gameid]
    teams = np.unique(teams.values.ravel())
    games[gameid] = teams

# Add opposing team variable
shots_raw['OPP_TEAM'] = 0
for i in range(0, len(shots_raw.index)-1):
    if shots_raw.loc[i, 'TEAM_NAME'] == games[shots_raw.loc[i, 'GAME_ID']][0]:
        shots_raw.loc[i, 'OPP_TEAM'] = games[shots_raw.loc[i, 'GAME_ID']][1]
    else:
        shots_raw.loc[i, 'OPP_TEAM'] = games[shots_raw.loc[i, 'GAME_ID']][0]

# Save the desired variables into a new DataFrame
shots = shots_raw[['PLAYER_NAME', 'TEAM_NAME', 'OPP_TEAM', 'LOC_X', 'LOC_Y', 'SHOT_MADE_FLAG', 'SHOT_TYPE', 'PERIOD', 'SECONDS']]
shots.columns = ['player', 'team', 'opp_team', 'x', 'y', 'made', 'ppb', 'period', 'seconds']

# Find which region a shot location is in
def find_region10(x, y):
    # 0.3971 .9806 2.3812 0.73815
    s1 = 0.3971
    s2 = 0.9806
    s3 = 2.3812
    s4 = (137.5 - (s2*80)) / 80
    
    region = -1
    # inside
    if (x >= -80) and (x <= 80) and (y <= 137.5 + s4*x) and (y <= 137.5 - s4*x):
        region = 1
    # baseline right
    if (x < -80) and (x >= -220) and (y < -s2*x) and (x**2 + y**2 <= 237.5**2):
        region = 2
    # midrange right
    if (x <= 0) and (y >= -s2*x) and (y > 137.5 + s4*x) and (x**2 + y**2 <= 237.5**2):
        region = 3
    # midrange left
    if (x > 0) and (y >= s2*x) and (y > 137.5 - s4*x) and (x**2 + y**2 <= 237.5**2):
        region = 4
    # baseline left
    if (x > 80) and (x <= 220) and (y < s2*x) and (x**2 + y**2 <= 237.5**2):
        region = 5
    # right corner
    if (x < -220) and (y < -s1*x):
        region = 6
    # outside right
    if (y >= -s1*x) and (y < -s3*x) and (x**2 + y**2 > 237.5**2):
        region = 7
    # outside middle
    if (y >= -s3*x) and (y >= s3*x) and (x**2 + y**2 > 237.5**2):
        region = 8
    # outside left
    if (y >= s1*x) and (y < s3*x) and (x**2 + y**2 > 237.5**2):
        region = 9
    # left corner
    if (x > 220) and (y < s1*x):
        region = 10
    return region

# Create grid of points
def point_matrix():
    point_matrix = []
    x = -245
    y = -47.5
    while x < 250:
        temp = pd.DataFrame({'x': [x],
                             'y': [y],
                             'region': [find_region10(x, y)]})
        point_matrix.append(temp)
        y = y + 10
        if y == 312.5:
            y = -47.5
            x = x + 10
    point_matrix = pd.concat(point_matrix, ignore_index=True)
    return point_matrix

# Add box locations for x and y, as well as region number
shots['x_box'] = shots.apply(lambda shot: (math.floor(shot['x'] / 10.0) * 10.0 + 5), axis=1)
shots['y_box'] = shots.apply(lambda shot: ((math.floor((shot['y'] + 2.5) / 10.0) * 10.0) + 2.5), axis=1)
shots['region'] = shots.apply(lambda shot: find_region10(shot['x'], shot['y']), axis=1)

# Write data to csv file
shots.to_csv(path_or_buf='%s/NBA data project/processed_shots/shots_%d.csv' % (directory, year),
             index=False)

########## START HERE ###############

# Read in clean file of all shots
shots = pd.read_csv('%s/NBA data project/processed_shots/shots_%d.csv' % (directory, year))

shots = shots[shots['y'] < 307.5]

subsetby = 'player'
filters = ['Dwight Howard']
subset = shots[shots[subsetby].isin(filters)]

subset = subset.sort(['region'])
shots_reg = subset.groupby('region').made.count()
made_reg = subset.groupby('region').made.sum()
pts_reg = made_reg * subset.groupby('region').ppb.mean()
fg_reg = made_reg / shots_reg
pps_reg = pts_reg / shots_reg

all_shots_reg = shots.groupby('region').made.count()
all_made_reg = shots.groupby('region').made.sum()
all_fg_reg = all_made_reg / all_shots_reg

region_stats = pd.DataFrame({'region': subset['region'].unique(),
                             'shots_reg': shots_reg,
                             'made_reg': made_reg,
                             'pts_reg': pts_reg,
                             'fg_reg': fg_reg,
                             'all_fg_reg': all_fg_reg,
                             'pps_reg': pps_reg})

boxes = point_matrix()

shots_box = subset.groupby(['x_box', 'y_box']).made.count()
shots_box = shots_box.reset_index()
shots_box.columns = ['x', 'y', 'shots']

made_box = subset.groupby(['x_box', 'y_box']).made.sum()
made_box = made_box.reset_index()
made_box.columns = ['x', 'y', 'made']

pts_box = made_box['made'] * subset.groupby(['x_box', 'y_box']).ppb.mean().reset_index()['ppb']
fg_box = made_box['made'] / shots_box['shots']
pps_box = pts_box / shots_box['shots']

box_stats = pd.DataFrame({'x': shots_box['x'],
                          'y': shots_box['y'],
                          'shots_box': shots_box['shots'],
                          'made_box': made_box['made'],
                          'pts_box': pts_box,
                          'fg_box': fg_box,
                          'pps_box': pps_box})

# Merge box matrix with the box stats
boxes = pd.merge(boxes, box_stats, on=['x', 'y'], how='outer')
# Merge the boxes with the region stats
boxes = pd.merge(boxes, region_stats, on='region', how='left')
