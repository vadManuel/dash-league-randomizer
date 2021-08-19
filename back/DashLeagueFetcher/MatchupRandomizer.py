import random

class MatchupRandomizer:
	'''
	This module provides access to the matchup generator, `get_matchups`.

	Parameters:
		`data_by_tiers_season_cycle`
		(dict) A dictionary containing teams as described by the season, cycle, and tier.
		
		`data_by_matchups_season_cycle`
		(dict) A dictionary containing the teams played matchups as described by the season and cycle.

		`current_season`
		(int) The current numerical season.
		
		`current_cycle`
		(int) The current numerical cycle.

	Returns:
		`teams_matchups_cycle`
		Contains a dictionary of teams by tier.

		Each team is a dictionary containing the following properties:

			`played_in_tier`
			Teams which have been played in the current tier.

			`played`
			Teams which have been played in the current season.

			`not_played`
			Teams which have not been played in the current season and current.

			`matchups`
			A list of 2 teams that have not been played in the current season and tier.
  '''

	def __init__(self, data_by_tiers_season_cycle=dict(), data_by_matchups_season_cycle=dict(), current_season=None, current_cycle=None):
		self.data_by_tiers_season_cycle = data_by_tiers_season_cycle
		self.data_by_matchups_season_cycle = data_by_matchups_season_cycle
		self.current_cycle = current_cycle

		self.all_teams = [team for tier in data_by_tiers_season_cycle[current_cycle] for team in data_by_tiers_season_cycle[current_cycle][tier]]

		# creating seed from current season and cycle
		season_seed = current_season*1e3
		cycle_seed = current_cycle*1e0
		seed = int(season_seed + cycle_seed)

		# seed random
		random.seed(seed)

	def get_matchups(self):
		'''
		This method builds a dictionary of teams by tier, which contains the matchup to be played in the current season. It will prevent matches that have been played in the current season from reoccuring. If it fails to find non-rematches, it only then will return rematches.
		'''
		teams_matchups_cycle = dict()
		teams_play_count = dict.fromkeys(self.all_teams, 0)

		for tier in self.data_by_tiers_season_cycle[self.current_cycle]:
			teams = self.data_by_tiers_season_cycle[self.current_cycle][tier]

			for team in teams:
				if tier not in teams_matchups_cycle:
					teams_matchups_cycle[tier] = dict()

				teams_played = []

				# Gotta love O(n^2)
				for cycle in self.data_by_matchups_season_cycle:
					_matchups = self.data_by_matchups_season_cycle[cycle]

					# Sometimes teams join late and therefore may not exist in past cycles
					if team in _matchups:
						existing_matchups = _matchups[team]
						teams_played.extend(set(existing_matchups))

				# a set of teams that will already be played 2 times in this cycle
				full_matchups = set()

				for _team in teams_played:
					if _team in teams_play_count and teams_play_count[_team] > 1:
						full_matchups.add(_team)

				# a set of played matches 
				played = set(teams_played)

				# an exclusive left join on the set of played matches and full_matchups
				played_and_non_full_matchups = played - full_matchups

				# Check if any teams in the selected matchup_cycle
				# are not playing in the current cycle of the season.
				# In other words, the intersection of the teams in the
				# selected matchup cycle and the current cycle of the season
				played_in_tier = played_and_non_full_matchups & set(teams)

				# exclusive left join
				not_played = set(teams) - played_and_non_full_matchups - set([team])

				matchups = set()

				# if and only if there are not enough teams not_played, then rematch
				if len(not_played) < 2:
					n_rematches = 2 - len(not_played)
					rematches = set(random.sample(played_in_tier, n_rematches))
					matchups = not_played | rematches
				else:
					# randomly pick 2 teams from not_played
					matchups = set(random.sample(not_played, 2))
				
				for matchup in list(matchups):
					teams_play_count[matchup] += 1

				teams_matchups_cycle[tier][team] = dict(
					played_in_tier=list(played_in_tier),
					played=list(played),
					not_played=list(not_played),
					matchups=list(matchups)
				)
		
		return teams_matchups_cycle
