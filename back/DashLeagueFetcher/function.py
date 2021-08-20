import json

from Fetcher import Fetcher
from MatchupRandomizer import MatchupRandomizer

parameter_keys = ['n_cycles', 'current_season', 'current_cycle']

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
        body = json.loads(event['body'])

        error_message = ''

        # build a string of errors if keys n_cycles, current_season, current_cycle are not in body or type is not int
        for key in parameter_keys:
            if 'n_cycles' not in body or not isinstance(body['n_cycles'], int):
                error_message += f'Key "{key}" missing or is not of type int.\n'
        
        if error_message != '':
            return get_response(400, message=error_message)

        # parameters
        n_cycles = body['n_cycles']
        current_season = body['current_season']
        current_cycle = body['current_cycle']

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