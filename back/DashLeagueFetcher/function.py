import json

from Fetcher import Fetcher
from MatchupRandomizer import MatchupRandomizer

# parameters
n_cycles = 6
current_season = 3
current_cycle = 4

def get_response(statusCode=200, body='', message=''):
    return {
        'statusCode': statusCode,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(dict(data=body, message=message))
    }

def handler(event, context):
    try:
        print(event)

        fetcher = Fetcher(
            current_season=current_season,
            n_cycles=n_cycles
        )

        data_by_tiers_season_cycle, data_by_matchups_season_cycle = fetcher.fetch_data()

        matchupRandomizer = MatchupRandomizer(
            data_by_matchups_season_cycle=data_by_matchups_season_cycle,
            data_by_tiers_season_cycle=data_by_tiers_season_cycle,
            current_season=current_season,
            current_cycle=current_cycle
        )

        matchups = matchupRandomizer.get_matchups()
    except Exception as e:
        print(e)

        return get_response(statusCode=500, message=str(e))

    return get_response(body=matchups)