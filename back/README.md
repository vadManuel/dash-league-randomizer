# Backend

## Data Endpoint

Endpoint Base: `https://dashleague.games/wp-json/api/v1/stats/data`

### Current Standings

```txt
https://dashleague.games/wp-json/api/v1/stats/data?data=standings
```

### Past Matchups

```txt
https://dashleague.games/wp-json/api/v1/stats/data?data=matchups
https://dashleague.games/wp-json/api/v1/stats/data?data=matchups&season=<number>
https://dashleague.games/wp-json/api/v1/stats/data?data=matchups&cycle=<number>
https://dashleague.games/wp-json/api/v1/stats/data?data=matchups&season=<number>&cycle=<number>
```

### Current Tiers

```txt
https://dashleague.games/wp-json/api/v1/stats/data?data=tiers
https://dashleague.games/wp-json/api/v1/stats/data?data=tiers&cycle=<number>
https://dashleague.games/wp-json/api/v1/stats/data?data=tiers&tier=<string>
https://dashleague.games/wp-json/api/v1/stats/data?data=tiers&cycle=<number>&tier=<string>
https://dashleague.games/wp-json/api/v1/stats/data?data=tiers&cycle=<number>&tier=<string>&mmr
```
