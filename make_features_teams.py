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
	game_stats, team_stats, player_stats = readPlayerFileAndFillStats(players_data_filename, game_stats)
	return game_stats, team_stats, player_stats


def readGameFile(games_data_filename):
	"""Reads LoL data from .csv file
	returns incomplete game_stats, team_stats (these need to be filled in readPlayerFileAndFillStats)
	"""
	game_stats = {}
	team_stats = {}
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

def readPlayerFileAndFillStats(players_data_filename, game_stats):
	"""Reads LoL data from .csv file and fills missing data in game_stats, team_stats
	returns complete game_stats, team_stats, player_stats
	"""
	player_stats = {}
	team_stats = {}
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
		    	

		    	if not team_stats.get(team_id):
	    			team_stats[team_id] = {'games_played': 1, 'wins': 0, 'loses': 0, 'kills': 0, 'deaths': 0, 'assists': 0, 'gold': 0, 'player_ids': Set([]), 'game_ids': Set([]), 'player_stats': []}
	    		
	    		team_stats[team_id]['wins'] += win/5
	    		team_stats[team_id]['loses'] += (1 - win)/5
		    	team_stats[team_id]['kills'] += kills
		    	team_stats[team_id]['deaths'] += deaths
		    	team_stats[team_id]['assists'] += assists
		    	team_stats[team_id]['gold'] += gold
		    	team_stats[team_id]['player_ids'].add(player_id)
		    	team_stats[team_id]['game_ids'].add(game_id)
		    	team_stats[team_id]['games_played'] = len(team_stats[team_id]['game_ids'])


		    	if not player_stats.get(player_id):
		    		player_stats[player_id] = {'games_played': 1, 'wins': win, 'loses': 1 - win, 'kills': kills, 'deaths': deaths, 'assists': assists, 'gold': gold, 'team_ids': Set([team_id])}
		    	else:
		    		player_stats[player_id]['games_played'] += 1
		    		player_stats[player_id]['wins'] += win
		    		player_stats[player_id]['loses'] += 1 - win
		    		player_stats[player_id]['kills'] += kills
		    		player_stats[player_id]['deaths'] += deaths
		    		player_stats[player_id]['assists'] += assists
		    		player_stats[player_id]['gold'] += gold
		    		player_stats[player_id]['team_ids'].add(team_id)

		    	#team_stats[team_id]['player_stats'].append({player_id: player_stats[player_id]})

	return game_stats_clean, team_stats, player_stats

def createFeatures(game_stats, team_stats, player_stats):
	"""creates features for each game from game_stats, team_stats, player_stats
	returns features, labels
	"""
	features = []
	labels = []
	game_ids = []

	for game_id in game_stats.keys():
		winner_team_id = game_stats[game_id]['winner_team_id']
		loser_team_id = game_stats[game_id]['loser_team_id']

		if not team_stats.get(winner_team_id):
			print([game_id, game_stats[game_id]])

		winner_team = team_stats[winner_team_id]
		loser_team = team_stats[loser_team_id]
		features_row = {}

		#if team played only 1 game its stats will be erased anyway, this is to prevent division by 0
		if winner_team['games_played'] == 1:
			winner_team['games_played'] = 2
		if loser_team['games_played'] == 1:
			loser_team['games_played'] = 2
		
		if random.choice([0, 1]) == 1:#to have approximately 50% of 1s and 50% of 0s, so our predictions wouldn't be biased
			for attr in winner_team.keys(): 
				if attr in ['kills', 'deaths', 'assists', 'gold']:
					#don't count stats of this game for its features
				    winner_attr = (winner_team[attr] - game_stats[game_id]['winner_' + attr]) / (winner_team['games_played'] - 1)
				    loser_attr = (loser_team[attr] - game_stats[game_id]['loser_' + attr]) / (loser_team['games_played'] - 1)
				    features_row[attr] = winner_attr - loser_attr

			winner_attr = (winner_team['wins'] - 1) / (winner_team['games_played'] - 1)
			loser_attr = loser_team['wins'] / (loser_team['games_played'] - 1)
			features_row['wins'] = winner_attr - loser_attr

			features.append(features_row)
			labels.append(1)
		else:
			for attr in winner_team.keys(): 
				if attr in ['kills', 'deaths', 'assists', 'gold']:
				    winner_attr = (winner_team[attr] - game_stats[game_id]['winner_' + attr]) / (winner_team['games_played'] - 1)
				    loser_attr = (loser_team[attr] - game_stats[game_id]['loser_' + attr]) / (loser_team['games_played'] - 1)
				    features_row[attr] = loser_attr - winner_attr

			winner_attr = (winner_team['wins'] - 1) / (winner_team['games_played'] - 1)
			loser_attr = loser_team['wins'] / (loser_team['games_played'] - 1)
			features_row['wins'] = loser_attr - winner_attr

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
train_game_stats, train_team_stats, train_player_stats = readData('data/game_teams_train.csv', 'data/game_player_teams_train.csv')
train_features, train_labels = createFeatures(train_game_stats, train_team_stats, train_player_stats)
writeFeatures(train_features, train_labels, 'data/train_features.csv')

test_game_stats, test_team_stats, test_player_stats = readData('data/game_teams_test.csv', 'data/game_player_teams_test.csv')
test_features, test_labels = createFeatures(test_game_stats, test_team_stats, test_player_stats)
writeFeatures(test_features, test_labels, 'data/test_features.csv')

print('done')
