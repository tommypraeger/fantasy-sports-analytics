from app.analysis.fantasy_league_analysis.league import League
from app.analysis.fantasy_league_analysis.export import export_league, export_team

def handler(event, context):
    try:
        # Argument reqs
        # ESPN: sport, leagueId, year, (espnS2, for private leagues)
        # Sleeper: leagueId, year
        league = League(event)
        league_export = {
            'league': export_league(league),
            'teams': [export_team(team) for team in league.teams]
        }
    except Exception as e:
        print(str(e))
        return {
            'errorMessage': str(e)
        }    
    
    return league_export
