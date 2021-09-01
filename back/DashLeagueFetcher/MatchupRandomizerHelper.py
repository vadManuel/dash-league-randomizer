import random
import json


class MatchupRandomizerHelper:
	def __init__(self):
		self.__teams_dictionary__ = dict()

		for tier in self.data_by_tiers_season_cycle[self.current_cycle]:
			self.__teams_dictionary__[tier] = dict.fromkeys(
				self.data_by_tiers_season_cycle[self.current_cycle][tier],
				dict(
					played_in_tier=[],
					played=[],
					not_played=[],
				)
			)
			
		# creating seed from current season and cycle
		season_seed = self.current_season*1e3
		cycle_seed = self.current_cycle*1e0
		seed = int(season_seed + cycle_seed)

		# seed random
		random.seed(seed)

		# initalize
		self.__build_teams_dictionary__()
		self.__initialize_graphs__()

		with open(f'./_dash_league_season-{self.current_season}_cycle-{self.current_cycle}.json', 'w') as f:
			json.dump(self.__teams_dictionary__, f)


	def check_graph_solved(self, graph):
		return all(len(graph.edges([team])) == self.n_matchups_per_team for team in self.teams)


	def check_current_team(self, graph, team):
		return len(graph.edges([team])) == self.n_matchups_per_team
	

	def __get_matchups__(self, availability_graph, matchup_graph, i=0, j=0):
		if self.check_graph_solved(matchup_graph):
			return True, availability_graph, matchup_graph

		if i >= self.n_teams:
			return False, availability_graph, matchup_graph

		availability_graph_copy = availability_graph.copy()
		matchup_graph_copy = matchup_graph.copy()

		team = self.teams[i]

		if self.check_current_team(matchup_graph_copy, team):
			for t in self.teams:
				if availability_graph_copy.has_edge(t, team):
					availability_graph_copy.remove_edge(t, team)
					
			return self.__get_matchups__(availability_graph_copy, matchup_graph_copy, i+1, 0)

		valid_edges = list(availability_graph.edges(team))

		if j >= len(valid_edges):
			return False, availability_graph, matchup_graph

		other_team = valid_edges[j][1]

		availability_graph_copy.remove_edge(team, other_team)

		matchup_graph_copy.add_edge(team, other_team)

		if self.check_current_team(matchup_graph_copy, team):
			for t in self.teams:
				if availability_graph_copy.has_edge(t, team):
					availability_graph_copy.remove_edge(t, team)

			return self.__get_matchups__(availability_graph_copy, matchup_graph_copy, i+1, 0)
		
		isValid, A, M = self.__get_matchups__(availability_graph_copy, matchup_graph_copy, i, j+1)

		if isValid:
			return True, A, M

		return self.__get_matchups__(availability_graph, matchup_graph, i, j+1)
	

	def __initialize_graphs__(self):
		for team in self.__teams_dictionary__['dasher']:
			self.availability_graph.add_node(team)
			self.matchup_graph.add_node(team)

		for team in self.__teams_dictionary__['dasher']:
			connections = []
			for matchup in self.__teams_dictionary__['dasher'][team]['not_played']:
				connections.append((team, matchup))

			self.availability_graph.add_edges_from(connections)

		teams = list(self.__teams_dictionary__['dasher'].keys())
		teams.sort(key=lambda team: len(self.__teams_dictionary__['dasher'][team]['not_played']))
	

	def __build_teams_dictionary__(self):
		'''
		This method builds a dictionary of teams by tier, which contains the matchup to be played in the current season. It will prevent matches that have been played in the current season from reoccuring. If it fails to find non-rematches, it only then will return rematches.
		'''
		
		for tier in self.data_by_tiers_season_cycle[self.current_cycle]:
			teams = self.data_by_tiers_season_cycle[self.current_cycle][tier]

			for team in teams:
				played = []

				# Gotta love O(n^2)
				for cycle in range(1, self.current_cycle+1):
					_matchups = self.data_by_matchups_season_cycle[cycle]

					# Sometimes teams join late and therefore may not exist in past cycles
					if team in _matchups:
						existing_matchups = _matchups[team]
						played.extend(set(existing_matchups))

				# a set of played matches 
				played = set(played)

				# Check if any teams in the selected matchup_cycle
				# are not playing in the current cycle of the season.
				# In other words, the intersection of the teams in the
				# selected matchup cycle and the current cycle of the season
				played_in_tier = played & set(teams)

				# exclusive left join on the sets of teams in the current tier,
				# played and non full matchups, and the currently selected team
				not_played = set(teams) - (played | set([team]))

				self.__teams_dictionary__[tier][team] = dict(
					played_in_tier=list(played_in_tier),
					played=list(played),
					not_played=list(not_played),
				)
		