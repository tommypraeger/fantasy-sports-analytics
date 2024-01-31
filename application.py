import json
from app.analysis.fantasy_league_analysis.league import League
from app.analysis.fantasy_league_analysis.export import export_league, export_team


def handler(event, context):
    event_body = json.loads(event["body"])
    if event_body["method"] == "league-analysis":
        print("Received request for league analysis")
        try:
            # Argument reqs
            # ESPN: sport, leagueId, year, (espnS2, for private leagues)
            # Sleeper: leagueId, year
            league = League(event_body)
            league_export = {
                "league": export_league(league),
                "teams": [export_team(team) for team in league.teams],
            }
        except Exception as e:
            print(str(e))
            return {"errorMessage": str(e)}

        return json.dumps(league_export)

    if event_body["method"] == "wakeup-league-analysis":
        print("Received wakeup")
        return json.dumps({})
