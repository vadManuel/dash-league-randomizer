import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

class Fetcher:
	def __init__(self, current_season=None, n_cycles=6):
		self.current_season = current_season
		self.n_cycles = n_cycles

	def __get_data_by_season_cycle__(self, url=None, season=None):
		data = dict()

		for cycle in range(1, self.n_cycles + 1):
			# building url for current_season and enumerated cycle
			_url = url.replace('<season>', str(season)).replace('<cycle>', str(cycle))

			response = requests.get(_url, headers=headers)
			_data = response.json()
			data[cycle] = _data['data']

		return data

	def fetch_data(self):
		# endpoint for tiers per season per cycle
		url_tiers_season_cycle = 'https://dashleague.games/wp-json/api/v1/stats/data?data=tiers&season=<season>&cycle=<cycle>'
		data_by_tiers_season_cycle = self.__get_data_by_season_cycle__(url=url_tiers_season_cycle, season=self.current_season)

		# endpoint for matchups per season per cycle
		url_matchups_season_cycle = 'https://dashleague.games/wp-json/api/v1/stats/data?data=matchups&season=<season>&cycle=<cycle>'
		data_by_matchups_season_cycle = self.__get_data_by_season_cycle__(url=url_matchups_season_cycle, season=self.current_season)

		return data_by_tiers_season_cycle, data_by_matchups_season_cycle