from back.DashLeagueFetcher.MatchupRandomizerHelper import MatchupRandomizerHelper
import networkx as nx


class MatchupRandomizer(MatchupRandomizerHelper):
	'''
	This module provides access to the matchup generator, `__get_matchups__`.

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

	def __init__(self, data_by_tiers_season_cycle=dict(), data_by_matchups_season_cycle=dict(), current_season=None, current_cycle=None, n_matchups_per_team=2):
		self.data_by_tiers_season_cycle = data_by_tiers_season_cycle
		self.data_by_matchups_season_cycle = data_by_matchups_season_cycle
		self.current_season = current_season
		self.current_cycle = current_cycle
		self.n_matchups_per_team = n_matchups_per_team

		self.availability_graph = nx.Graph()
		self.matchup_graph = nx.Graph()
		self.teams = data_by_tiers_season_cycle[current_cycle]['dasher']
		self.n_teams = len(self.teams)

		self.__teams_dictionary__ = dict()

		super().__init__()
	

	def get_matchups(self):
		if not all(len(self.availability_graph.edges([team])) > 1 for team in self.teams):
			raise Exception('Matchup graph is not valid.')

		isValid, _, matchup_graph = self.__get_matchups__(self.availability_graph, self.matchup_graph)

		if not isValid:
			raise Exception('Unable to find valid matchups.')
		
		return matchup_graph
		