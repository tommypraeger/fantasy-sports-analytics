import requests

from app.analysis.fantasy_league_analysis.models import (
    League as LeagueModel,
    LeagueInfo,
    Team,
    Matchup,
    Platform,
)
from app.analysis.fantasy_league_analysis.common import (
    perform_team_analysis,
    get_curr_matchups_played,
)


def fetch_league(league: LeagueModel, league_info: LeagueInfo) -> None:
    """Load league and set metadata for league and teams"""
    league.id = league_info.league_id
    league.year = league_info.year
    league.sport = league_info.sport
    league.platform = Platform.SLEEPER

    # Necessary Sleeper API URLs
    league_url = f"https://api.sleeper.app/v1/league/{league.id}"
    teams_url = f"https://api.sleeper.app/v1/league/{league.id}/rosters"
    users_url = f"https://api.sleeper.app/v1/league/{league.id}/users"

    with requests.Session() as session:
        # Fetch league data
        league_resp = session.get(league_url)
        if league_resp.status_code >= 400:
            raise Exception("Failed to fetch league data. Check your league ID.")
        league_json = league_resp.json()

        # Fetch teams data
        teams_resp = session.get(teams_url)
        if teams_resp.status_code >= 400:
            raise Exception("Failed to fetch teams data. Check your league ID.")
        teams_json = teams_resp.json()

        # Fetch users data
        users_resp = session.get(users_url)
        if users_resp.status_code >= 400:
            raise Exception("Failed to fetch users data. Check your league ID.")
        users_json = users_resp.json()

        # Set league metadata
        league.name = league_json["name"]
        league.total_matchups = league_json["settings"]["playoff_week_start"] - 1
        league.num_teams = len(teams_json)

        # Create teams from rosters and users data
        user_map = {user["user_id"]: user["display_name"] for user in users_json}
        for roster in teams_json:
            roster_id = str(roster["roster_id"])
            team = Team(
                id=roster_id,
                name=user_map.get(roster["owner_id"], f"Team {roster['roster_id']}")
            )
            league.teams.append(team)
            league.team_map[roster_id] = team

        # Create standardized matchups directly from the schedule
        create_standardized_matchups(league, session)

        # Get current matchups played using the common function
        league.curr_matchups_played = get_curr_matchups_played(league)

    # Can't do analysis with less than 2 games played
    if league.curr_matchups_played < 2:
        raise Exception("There must have been at least 2 matchups played already.")

    # Perform team analysis
    perform_team_analysis(league)


def create_standardized_matchups(league: LeagueModel, session: requests.Session) -> None:
    """Fetch and convert Sleeper schedule format to standardized matchup format"""
    for week in range(1, league.total_matchups + 1):
        matchups_url = f"https://api.sleeper.app/v1/league/{league.id}/matchups/{week}"
        matchups_resp = session.get(matchups_url)
        if matchups_resp.status_code >= 400:
            raise Exception("Failed to fetch matchups data. Check your league ID.")
        matchups = matchups_resp.json()

        # Group matchups by matchup_id to find pairs of teams
        matchup_groups = {}
        for matchup in matchups:
            matchup_id = str(matchup["matchup_id"])
            if matchup_id not in matchup_groups:
                matchup_groups[matchup_id] = []
            matchup_groups[matchup_id].append(matchup)

        # Create standardized matchups from pairs
        for matchup_id, matchup_pair in matchup_groups.items():
            if len(matchup_pair) != 2:
                continue  # Skip if not a complete matchup pair

            home_team = matchup_pair[0]
            away_team = matchup_pair[1]

            matchup = Matchup(
                matchup_id=matchup_id,
                week=week,
                home_team_id=str(home_team["roster_id"]),
                away_team_id=str(away_team["roster_id"]),
                home_score=home_team.get("points") or home_team.get("custom_points"),
                away_score=away_team.get("points") or away_team.get("custom_points"),
                is_playoffs=False
            )
            matchup.platform = Platform.SLEEPER
            league.matchups.append(matchup)
