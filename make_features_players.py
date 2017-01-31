from __future__ import division
import csv
import numpy as np
import random
from sets import Set

#game 2864,2846 - wrong team id

def readData(games_data_filename, players_data_filename):
	"""Reads LoL data from .csv files
	returns game_stats, team_stats, player_stats
	"""
	game_stats = readGameFile(games_data_filename)
	game_stats, player_stats = readPlayerFileAndFillStats(players_data_filename, game_stats)
	return game_stats, player_stats


def readGameFile(games_data_filename):
	"""Reads LoL data from .csv file
	returns incomplete game_stats, team_stats (these need to be filled in readPlayerFileAndFillStats)
	"""
	game_stats = {}
	
	with open(games_data_filename) as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	    	game_id = row['game_id']
	    	team_id = row['team_id']
	    	winner_id = row['winner_id']
	    	loser_id = None
	    	
	    	win = 0
	    	if team_id == winner_id:
	    		win = 1
	    	else:
	    		loser_id = team_id

	    	if not game_stats.get(game_id):
	    		game_stats[game_id] = {'winner_team_id': winner_id, 'loser_team_id':'', 'winner_player_ids':[], 'loser_player_ids':[], 'winner_kills': 0, 'loser_kills': 0, 'winner_deaths': 0, 'loser_deaths': 0, 'winner_assists': 0, 'loser_assists': 0, 'winner_gold': 0, 'loser_gold': 0}

	    	if loser_id is not None:
	    		game_stats[game_id]['loser_team_id'] = loser_id
	return game_stats

def readPlayerFileAndFillStats(players_data_filename, game_stats):
	"""Reads LoL data from .csv file and fills missing data in game_stats, team_stats
	returns complete game_stats, team_stats, player_stats
	"""
	player_stats = {}
	game_stats_clean = {}
	game_stats = fillGameStats(players_data_filename, game_stats)

	with open(players_data_filename) as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	    	game_id = row['game_id']

	    	if isGameStatsValid(game_stats[game_id]):

	    		player_id = row['player_id']
	    		team_id = row['team_id']
	    		kills = row['kill']
	    		deaths = row['death']
	    		assists = row['assists']
	    		gold = row['gold_earned']

	    		if not game_stats.get(game_id):
	    			print('no game id')

	    		kills = int(kills)
	    		deaths = int(deaths)
	    		assists = int(assists)
	    		gold = int(gold)

	    		if not game_stats_clean.get(game_id):
	    			game_stats_clean[game_id] = game_stats[game_id]

	    		win = 0
	    		if game_stats[game_id]['winner_team_id'] == team_id:
	    			win = 1
	    			
	    		if not player_stats.get(player_id):
	    			player_stats[player_id] = {'games_played': 1, 'wins': win, 'loses': 1 - win, 'kills': kills, 'deaths': deaths, 'assists': assists, 'gold': gold, 'team_ids': Set([team_id]), 'game_stats': {}}
	    		else:
	    			player_stats[player_id]['games_played'] += 1
	    			player_stats[player_id]['wins'] += win
	    			player_stats[player_id]['loses'] += 1 - win
	    			player_stats[player_id]['kills'] += kills
	    			player_stats[player_id]['deaths'] += deaths
	    			player_stats[player_id]['assists'] += assists
	    			player_stats[player_id]['gold'] += gold
	    			player_stats[player_id]['team_ids'].add(team_id)

	    		player_stats[player_id]['game_stats'][game_id] = {'wins': win, 'loses': 1 - win, 'kills': kills, 'deaths': deaths, 'assists': assists, 'gold': gold, 'team_id': team_id}
	    	

	return game_stats_clean, player_stats

def fillGameStats(players_data_filename, game_stats):

	with open(players_data_filename) as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	    	game_id = row['game_id']
	    	player_id = row['player_id']
	    	team_id = row['team_id']
	    	kills = row['kill']
	    	deaths = row['death']
	    	assists = row['assists']
	    	gold = row['gold_earned']

	    	if not game_stats.get(game_id):
	    		print('no game id')

	    	kills = int(kills)
	    	deaths = int(deaths)
	    	assists = int(assists)
	    	gold = int(gold)

	    	win = 0
	    	if game_stats[game_id]['winner_team_id'] == team_id:
	    		win = 1
	    		game_stats[game_id]['winner_player_ids'].append(player_id)
	    		game_stats[game_id]['winner_kills'] += kills
	    		game_stats[game_id]['winner_deaths'] += deaths
	    		game_stats[game_id]['winner_assists'] += assists
	    		game_stats[game_id]['winner_gold'] += gold

	        else:
	    		game_stats[game_id]['loser_player_ids'].append(player_id)
	    		game_stats[game_id]['loser_kills'] += kills
	    		game_stats[game_id]['loser_deaths'] += deaths
	    		game_stats[game_id]['loser_assists'] += assists
	    		game_stats[game_id]['loser_gold'] += gold

	return game_stats

def isGameStatsValid(game_stat_row):
	if (game_stat_row['winner_kills'] == 0) & (game_stat_row['loser_kills'] == 0):
		return False
	else:
		return True

def cleanData(game_stats, team_stats, player_stats):
	#game_stats_clean = {}
	#team_stats_clean = {}
	#player_stats_clean = {}

	#for game_id in game_stats.keys():
	#	if isGameDataValid(game_stats[game_id]):


	return game_stats_clean, team_stats_clean, player_stats_clean

def makeTeamStatsForGame(player_ids, player_stats, game_id):
	team_stats = {}
	for i in range(len(player_ids)):
		for attr in player_stats[player_ids[i]].keys():
			if attr in ['kills', 'deaths', 'assists', 'gold', 'wins']:
				attr_value = player_stats[player_ids[i]][attr] - player_stats[player_ids[i]]['game_stats'][game_id][attr]
				games_played = player_stats[player_ids[i]]['games_played'] - 1
				games_played = 1 if games_played < 1 else games_played
				players_n = 5
				team_stats[attr] = team_stats.get(attr, 0) + (attr_value / games_played / players_n) # divide by players_n because we want average of average
	return team_stats

def createFeatures(game_stats, player_stats):
	"""creates features for each game from game_stats, team_stats, player_stats
	returns features, labels
	"""
	features = []
	labels = []
	game_ids = []

	for game_id in game_stats.keys():
		
		winner_player_ids = game_stats[game_id]['winner_player_ids']
		loser_player_ids = game_stats[game_id]['loser_player_ids']

		features_row = {}

		winner_team_stats = makeTeamStatsForGame(winner_player_ids, player_stats, game_id)
		loser_team_stats = makeTeamStatsForGame(loser_player_ids, player_stats, game_id)
		
		if random.choice([0, 1]) == 1:#to have approximately 50% of 1s and 50% of 0s, so our predictions wouldn't be biased
			for attr in winner_team_stats.keys():
				features_row[attr] = winner_team_stats[attr] - loser_team_stats[attr]
			if len(features_row.keys()) > 0:
				features.append(features_row)
				labels.append(1)
		else:
			for attr in winner_team_stats.keys(): 
				features_row[attr] = loser_team_stats[attr] - winner_team_stats[attr]
			
			if len(features_row.keys()) > 0:
				features.append(features_row)
				labels.append(0)

		game_ids.append(game_id)

	return features, labels

def writeFeatures(features, labels, output_filename):
	"""write features and labels to csv file"""
	with open(output_filename, 'w') as csvfile:
	    fieldnames = features[0].keys()
	    fieldnames.append('label')
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	    writer.writeheader()
	    for i in range(len(features)):
	    	features[i]['label'] = labels[i]
	    	writer.writerow(features[i])

	return

#read data, create features, write features to a new .csv file
train_game_stats, train_player_stats = readData('data/game_teams_train.csv', 'data/game_player_teams_train.csv')
train_features, train_labels = createFeatures(train_game_stats, train_player_stats)
for player_id in train_player_stats.keys():
	print 'player id: ', player_id, ' gp: ', train_player_stats[player_id]['games_played'], ' wins: ' ,train_player_stats[player_id]['wins'], ' kills: ', train_player_stats[player_id]['kills'], ' deaths: ', train_player_stats[player_id]['deaths'], ' assists: ', train_player_stats[player_id]['assists'], ' gold: ', train_player_stats[player_id]['gold'] 
	for game_id in train_player_stats[player_id]['game_stats'].keys():
		print '------', game_id, train_player_stats[player_id]['game_stats'][game_id]

writeFeatures(train_features, train_labels, 'data/train_features.csv')

test_game_stats, test_player_stats = readData('data/game_teams_test.csv', 'data/game_player_teams_test.csv')
test_features, test_labels = createFeatures(test_game_stats, test_player_stats)
writeFeatures(test_features, test_labels, 'data/test_features.csv')

print('done')
