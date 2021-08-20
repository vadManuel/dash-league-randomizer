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
			A list of n_matchups_per_team teams that have not been played in the current season and tier.
  '''

	def __init__(self, data_by_tiers_season_cycle=dict(), data_by_matchups_season_cycle=dict(), current_season=None, current_cycle=None, n_matchups_per_team=2, debug=False):
		self.data_by_tiers_season_cycle = data_by_tiers_season_cycle
		self.data_by_matchups_season_cycle = data_by_matchups_season_cycle
		self.current_cycle = current_cycle
		self.n_matchups_per_team = n_matchups_per_team
		self.debug = debug

		self.teams_matchups_cycle = dict()

		for tier in self.data_by_tiers_season_cycle[self.current_cycle]:
			self.teams_matchups_cycle[tier] = dict.fromkeys(
				self.data_by_tiers_season_cycle[self.current_cycle][tier],
				dict(
					played_in_tier=[],
					played=[],
					not_played=[],
					matchups=[],
					rematches=[],
					excess_matchups=[]
				)
			)
			
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
		
		for tier in self.data_by_tiers_season_cycle[self.current_cycle]:
			teams = self.data_by_tiers_season_cycle[self.current_cycle][tier]

			for team in teams:
				# the matchups for the currently selected team
				team_matchups = set(self.teams_matchups_cycle[tier][team]['matchups'])

				n_matchups_pending = self.n_matchups_per_team - len(team_matchups)

				played = []

				# Gotta love O(n^2)
				for cycle in self.data_by_matchups_season_cycle:
					_matchups = self.data_by_matchups_season_cycle[cycle]

					# Sometimes teams join late and therefore may not exist in past cycles
					if team in _matchups:
						existing_matchups = _matchups[team]
						played.extend(set(existing_matchups))

				# a set of played matches 
				played = set(played)

				# a set of teams that will already be played n_matchups_per_team times in this cycle
				full_matchups = set()

				if self.debug:
					print(tier)

				for _tier in self.teams_matchups_cycle:
					for _team in teams:
						if _team in self.teams_matchups_cycle[_tier]:
							_team_matchups = self.teams_matchups_cycle[_tier][_team]['matchups']

							if self.debug:
								print(_team, _team_matchups)
							if len(_team_matchups) >= self.n_matchups_per_team:
								full_matchups.add(_team)
				
				# Check if any teams in the selected matchup_cycle
				# are not playing in the current cycle of the season.
				# In other words, the intersection of the teams in the
				# selected matchup cycle and the current cycle of the season
				played_in_tier = played & set(teams)

				# exclusive left join on the sets of teams in the current tier,
				# played and non full matchups, and the currently selected team
				not_played = set(teams) - (played | set([team]))

				available_matchups = (not_played | team_matchups) - full_matchups

				if self.debug:
					print()
					print('full_matchups', full_matchups)
					print('played_in_tier', played_in_tier)
					print('not_played', not_played)
					print('available_matchups', available_matchups)

				matchups = set(team_matchups)
				rematches = set()
				excess_matchups = set()

				if self.debug:
					print()
					print('current matchups', matchups)

				# if and only if there are not enough teams not_played, then rematch
				if len(available_matchups) < n_matchups_pending:
					match_pool = set(teams) - full_matchups

					if len(match_pool) < n_matchups_pending:
						match_pool = match_pool | played_in_tier
						if self.debug:
							print('REPLAYING')
					
					if len(match_pool) < n_matchups_pending:
						excess_matchup_pool = set(random.sample(set(teams) - match_pool, n_matchups_pending - len(match_pool)))
						match_pool = match_pool | excess_matchup_pool
						if self.debug:
							print('NOT ENOUGH TEAMS')

					more_matchups = set(random.sample(match_pool, n_matchups_pending))

					for matchup in more_matchups:
						if matchup in played_in_tier:
							rematches.add(matchup)
						elif matchup in teams:
							excess_matchups.add(matchup)

					if self.debug:
						print('rematches/excess', more_matchups)
					matchups = matchups | more_matchups
				else:
					# randomly pick n_matchups_per_team teams from not_played
					more_matchups = set(random.sample(available_matchups, n_matchups_pending))
					
					if self.debug:
						print('new matchups', more_matchups)
					matchups = matchups | more_matchups
				
				if self.debug:
					print()

				for matchup in matchups:
					matchup_properties = self.teams_matchups_cycle[tier][matchup]

					self.teams_matchups_cycle[tier][matchup] = dict(
						played_in_tier=list(matchup_properties['played_in_tier']),
						played=list(matchup_properties['played']),
						not_played=list(matchup_properties['not_played']),
						matchups=list(set(matchup_properties['matchups']) | set([team])),
						rematches=list(matchup_properties['rematches']),
						excess_matchups=list(matchup_properties['excess_matchups']),
					)

					if self.debug:
						print('added to', matchup, self.teams_matchups_cycle[tier][matchup]['matchups'])

				self.teams_matchups_cycle[tier][team] = dict(
					played_in_tier=list(played_in_tier),
					played=list(played),
					not_played=list(not_played),
					matchups=list(matchups),
					rematches=list(rematches),
					excess_matchups=list(excess_matchups),
				)
				
				if self.debug:
					print('updated', team, self.teams_matchups_cycle[tier][team]['matchups'])
					print('-'*30)

		return self.teams_matchups_cycle
		