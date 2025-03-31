import sys
sys.path.insert(0, 'site-packages')

import json
import traceback
from typing import Dict, Any

from app.analysis.fantasy_league_analysis.league import League
from app.analysis.fantasy_league_analysis.export import export_league, export_team


def handler(event: Dict[str, Any], context: Any) -> str:
    event_body = json.loads(event["body"])
    if event_body["method"] == "league-analysis":
        return json.dumps(handle_league_analysis(event_body))

    if event_body["method"] == "wakeup-league-analysis":
        print("Received wakeup")
        return json.dumps({})


def handle_league_analysis(event_body: Dict[str, Any]) -> Dict[str, Any]:
    print("Received request for league analysis")
    try:
        # Argument reqs
        # ESPN: sport, leagueId, year, (espnS2, for private leagues)
        # Sleeper: leagueId, year
        league = League(event_body)
        league_export = {
            "league": export_league(league),
            "teams": [export_team(team, league) for team in league.teams],
        }
    except Exception as e:
        print(traceback.format_exc())
        return {"errorMessage": str(e)}

    return league_export
