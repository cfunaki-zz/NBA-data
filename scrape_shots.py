
def scrape_shots():
    """
    with open('E:/NBA data project/all_shot_data.csv','rU') as csvfile:
        reader=csv.reader(csvfile)
        data1=[row for row in reader]
    """
    headers=["GRID_TYPE","GAME_ID","GAME_EVENT_ID","PLAYER_ID","PLAYER_NAME","TEAM_ID","TEAM_NAME","PERIOD","MINUTES_REMAINING","SECONDS_REMAINING","EVENT_TYPE","ACTION_TYPE","SHOT_TYPE","SHOT_ZONE_BASIC","SHOT_ZONE_AREA","SHOT_ZONE_RANGE","SHOT_DISTANCE","LOC_X","LOC_Y","SHOT_ATTEMPTED_FLAG","SHOT_MADE_FLAG"]
    games=[]
    for row in data1:
        games.append(row[0])
    for year in range(2013,2014,1):
        all_shots=[]
        print year
        y2=int(str(year)[2:])
        y3=y2+1
        if y2==99:
            y3=0
        season=str(year)+"-"+str("%02d" % (y3,))
        for gameid in range(1,1250,1):
            if gameid not in games:
                game="002"+"%02d" % (y2,)+"%05d" % (gameid,)
                if game not in games:
                    nba_call_url='http://stats.nba.com/stats/shotchartdetail?Season=%s&SeasonType=Regular%%20Season&TeamID=0&PlayerID=0&GameID=%s&Outcome=&Location=&Month=0&SeasonSegment=&DateFrom=&Dateto=&OpponentTeamID=0&VsConference=&VsDivision=&Position=&RookieYear=&GameSegment=&Period=0&LastNGames=0&ContextMeasure=FGA' % (season,game)
                    #nba_box_url='http://stats.nba.com/stats/boxscore?StartPeriod=0&EndPeriod=0&StartRange=0&EndRange=0&RangeType=0&GameID=%s' % (game)
                    print gameid
                    plays=urllib2.urlopen(nba_call_url)
                    #box=urllib2.urlopen(nba_box_url)
                    try:
                        data=json.load(plays)
                    except:
                        print 'Data failed to load'
                        data=json.load({"resource":"shotchartdetail","parameters":{"LeagueID":null,"Season":"1996-97","SeasonType":"Regular Season","TeamID":0,"PlayerID":0,"GameID":"0029601987","Outcome":null,"Location":null,"Month":0,"SeasonSegment":null,"DateFrom":null,"DateTo":null,"OpponentTeamID":0,"VsConference":null,"VsDivision":null,"Position":null,"RookieYear":null,"GameSegment":null,"Period":0,"LastNGames":0,"ClutchTime":null,"AheadBehind":null,"PointDiff":null,"RangeType":null,"StartPeriod":null,"EndPeriod":null,"StartRange":null,"EndRange":null,"ContextFilter":"","ContextMeasure":"FGA"},"resultSets":[{"name":"Shot_Chart_Detail","headers":["GRID_TYPE","GAME_ID","GAME_EVENT_ID","PLAYER_ID","PLAYER_NAME","TEAM_ID","TEAM_NAME","PERIOD","MINUTES_REMAINING","SECONDS_REMAINING","EVENT_TYPE","ACTION_TYPE","SHOT_TYPE","SHOT_ZONE_BASIC","SHOT_ZONE_AREA","SHOT_ZONE_RANGE","SHOT_DISTANCE","LOC_X","LOC_Y","SHOT_ATTEMPTED_FLAG","SHOT_MADE_FLAG"],"rowSet":[]},{"name":"LeagueAverages","headers":["GRID_TYPE","SHOT_ZONE_BASIC","SHOT_ZONE_AREA","SHOT_ZONE_RANGE","FGA","FGM","FG_PCT"],"rowSet":[["League Averages","Above the Break 3","Back Court(BC)","Back Court Shot",85,2,0.024],["League Averages","Above the Break 3","Center(C)","24+ ft.",2961,1004,0.339],["League Averages","Above the Break 3","Left Side Center(LC)","24+ ft.",6391,2096,0.328],["League Averages","Above the Break 3","Right Side Center(RC)","24+ ft.",4938,1713,0.347],["League Averages","Backcourt","Back Court(BC)","Back Court Shot",207,9,0.043],["League Averages","In The Paint (Non-RA)","Center(C)","8-16 ft.",4311,1896,0.44],["League Averages","In The Paint (Non-RA)","Center(C)","Less Than 8 ft.",14430,6313,0.437],["League Averages","In The Paint (Non-RA)","Left Side(L)","8-16 ft.",1893,781,0.413],["League Averages","In The Paint (Non-RA)","Right Side(R)","8-16 ft.",1741,714,0.41],["League Averages","Left Corner 3","Left Side(L)","24+ ft.",3068,1214,0.396],["League Averages","Mid-Range","Center(C)","16-24 ft.",7169,2906,0.405],["League Averages","Mid-Range","Center(C)","8-16 ft.",1668,710,0.426],["League Averages","Mid-Range","Left Side Center(LC)","16-24 ft.",9900,4050,0.409],["League Averages","Mid-Range","Left Side(L)","16-24 ft.",9842,4158,0.422],["League Averages","Mid-Range","Left Side(L)","8-16 ft.",13794,5376,0.39],["League Averages","Mid-Range","Right Side Center(RC)","16-24 ft.",11226,4357,0.388],["League Averages","Mid-Range","Right Side(R)","16-24 ft.",9029,3715,0.411],["League Averages","Mid-Range","Right Side(R)","8-16 ft.",12668,5036,0.398],["League Averages","Restricted Area","Center(C)","Less Than 8 ft.",70575,38643,0.548],["League Averages","Right Corner 3","Right Side(R)","24+ ft.",2689,1079,0.401]]}]})
					#boxscore=json.load(box)
					#month=boxscore['resultSets'][0]['rowSet'][0][5][4:6]
					#day=boxscore['resultSets'][0]['rowSet'][0][5][6:8]
					teams=list(set([row[6] for row in data['resultSets'][0]['rowSet']]))
					for row in data['resultSets'][0]['rowSet']:
						# (gameid, player, offense team, defense team, 3pt, made, year, regular/post (0/1), quarter, second remaining, x, y, month, day)
						three=0
						if row[12]=='3PT Field Goal':
							three=1
						if row[6]==teams[0]:
							temp=[game,row[4],teams[0],teams[1],three,row[20],year,0,row[7],row[8]*60+row[9],row[17],row[18]]
						if row[6]==teams[1]:
							temp=[game,row[4],teams[1],teams[0],three,row[20],year,0,row[7],row[8]*60+row[9],row[17],row[18]]
						all_shots.append(temp)
		for gameid in range(1,407,1):
			if gameid not in games:
				game="004"+"%02d" % (y2,)+"%05d" % (gameid,)
				if game not in games:
					nba_call_url='http://stats.nba.com/stats/shotchartdetail?Season=%s&SeasonType=Playoffs&TeamID=0&PlayerID=0&GameID=%s&Outcome=&Location=&Month=0&SeasonSegment=&DateFrom=&Dateto=&OpponentTeamID=0&VsConference=&VsDivision=&Position=&RookieYear=&GameSegment=&Period=0&LastNGames=0&ContextMeasure=FGA' % (season,game)
					#nba_box_url='http://stats.nba.com/stats/boxscore?StartPeriod=0&EndPeriod=0&StartRange=0&EndRange=0&RangeType=0&GameID=%s' % (game)
					print game
					plays=urllib2.urlopen(nba_call_url)
					#box=urllib2.urlopen(nba_box_url)
					try:
						data=json.load(plays)
					except:
						print 'DATA DID NOT LOAD'
						data=json.load({"resource":"shotchartdetail","parameters":{"LeagueID":null,"Season":"1996-97","SeasonType":"Regular Season","TeamID":0,"PlayerID":0,"GameID":"0029601987","Outcome":null,"Location":null,"Month":0,"SeasonSegment":null,"DateFrom":null,"DateTo":null,"OpponentTeamID":0,"VsConference":null,"VsDivision":null,"Position":null,"RookieYear":null,"GameSegment":null,"Period":0,"LastNGames":0,"ClutchTime":null,"AheadBehind":null,"PointDiff":null,"RangeType":null,"StartPeriod":null,"EndPeriod":null,"StartRange":null,"EndRange":null,"ContextFilter":"","ContextMeasure":"FGA"},"resultSets":[{"name":"Shot_Chart_Detail","headers":["GRID_TYPE","GAME_ID","GAME_EVENT_ID","PLAYER_ID","PLAYER_NAME","TEAM_ID","TEAM_NAME","PERIOD","MINUTES_REMAINING","SECONDS_REMAINING","EVENT_TYPE","ACTION_TYPE","SHOT_TYPE","SHOT_ZONE_BASIC","SHOT_ZONE_AREA","SHOT_ZONE_RANGE","SHOT_DISTANCE","LOC_X","LOC_Y","SHOT_ATTEMPTED_FLAG","SHOT_MADE_FLAG"],"rowSet":[]},{"name":"LeagueAverages","headers":["GRID_TYPE","SHOT_ZONE_BASIC","SHOT_ZONE_AREA","SHOT_ZONE_RANGE","FGA","FGM","FG_PCT"],"rowSet":[["League Averages","Above the Break 3","Back Court(BC)","Back Court Shot",85,2,0.024],["League Averages","Above the Break 3","Center(C)","24+ ft.",2961,1004,0.339],["League Averages","Above the Break 3","Left Side Center(LC)","24+ ft.",6391,2096,0.328],["League Averages","Above the Break 3","Right Side Center(RC)","24+ ft.",4938,1713,0.347],["League Averages","Backcourt","Back Court(BC)","Back Court Shot",207,9,0.043],["League Averages","In The Paint (Non-RA)","Center(C)","8-16 ft.",4311,1896,0.44],["League Averages","In The Paint (Non-RA)","Center(C)","Less Than 8 ft.",14430,6313,0.437],["League Averages","In The Paint (Non-RA)","Left Side(L)","8-16 ft.",1893,781,0.413],["League Averages","In The Paint (Non-RA)","Right Side(R)","8-16 ft.",1741,714,0.41],["League Averages","Left Corner 3","Left Side(L)","24+ ft.",3068,1214,0.396],["League Averages","Mid-Range","Center(C)","16-24 ft.",7169,2906,0.405],["League Averages","Mid-Range","Center(C)","8-16 ft.",1668,710,0.426],["League Averages","Mid-Range","Left Side Center(LC)","16-24 ft.",9900,4050,0.409],["League Averages","Mid-Range","Left Side(L)","16-24 ft.",9842,4158,0.422],["League Averages","Mid-Range","Left Side(L)","8-16 ft.",13794,5376,0.39],["League Averages","Mid-Range","Right Side Center(RC)","16-24 ft.",11226,4357,0.388],["League Averages","Mid-Range","Right Side(R)","16-24 ft.",9029,3715,0.411],["League Averages","Mid-Range","Right Side(R)","8-16 ft.",12668,5036,0.398],["League Averages","Restricted Area","Center(C)","Less Than 8 ft.",70575,38643,0.548],["League Averages","Right Corner 3","Right Side(R)","24+ ft.",2689,1079,0.401]]}]})
					#boxscore=json.load(box)
					#month=boxscore['resultSets'][0]['rowSet'][0][5][4:6]
					#day=boxscore['resultSets'][0]['rowSet'][0][5][6:8]
					teams=list(set([row[6] for row in data['resultSets'][0]['rowSet']]))
					for row in data['resultSets'][0]['rowSet']:
						# (gameid, player, offense team, defense team, 3pt, made, year, regular/post (0/1), quarter, second remaining, x, y)
						three=0
						if row[12]=='3PT Field Goal':
							three=1
						if row[6]==teams[0]:
							temp=[game,row[4],teams[0],teams[1],three,row[20],year,1,row[7],row[8]*60+row[9],row[17],row[18]]
						if row[6]==teams[1]:
							temp=[game,row[4],teams[1],teams[0],three,row[20],year,1,row[7],row[8]*60+row[9],row[17],row[18]]
						all_shots.append(temp)
		with open('E:/NBA data project/all_shot_data.csv','a') as csvfile:
			writer=csv.writer(csvfile)
			for row in all_shots:
				writer.writerow(row)