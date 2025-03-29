import requests
from typing import List, Dict

from app.analysis.fantasy_league_analysis.models import (
    League as LeagueModel,
    LeagueInfo,
    Team,
    Matchup,
    Platform,
    Sport,
)
from app.analysis.fantasy_league_analysis.common import (
    perform_team_analysis,
    get_curr_matchups_played,
)


# Map of sports to their ESPN API game IDs
SPORT_MAP = {
    Sport.FOOTBALL: "ffl",
    Sport.BASEBALL: "flb",
    Sport.BASKETBALL: "fba",
}


def fetch_league(league: LeagueModel, league_info: LeagueInfo) -> None:
    """Load league and set metadata for league and teams"""
    league.id = league_info.league_id
    league.year = league_info.year
    league.sport = league_info.sport
    league.platform = Platform.ESPN

    if league.sport not in SPORT_MAP:
        raise ValueError(f"{league.sport} is not a valid sport for ESPN.")

    # Necessary ESPN API URLs
    game_id = SPORT_MAP[league.sport]
    league_url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/{game_id}/seasons/{league.year}/segments/0/leagues/{league.id}"
    teams_url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/{game_id}/seasons/{league.year}/segments/0/leagues/{league.id}?view=mTeam"
    users_url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/{game_id}/seasons/{league.year}/segments/0/leagues/{league.id}?view=kona_league_info"
    schedule_url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/{game_id}/seasons/{league.year}/segments/0/leagues/{league.id}?view=mMatchupScore"

    headers = {}
    if league_info.espn_s2:
        headers["Cookie"] = f"espn_s2={league_info.espn_s2}"

    with requests.Session() as session:
        session.headers.update(headers)
        
        # Make requests and check if they succeed
        league_resp = session.get(league_url)
        if league_resp.status_code >= 400:
            raise Exception("Failed to fetch league data. Check your league ID and ESPN S2 cookie if needed.")
            
        teams_resp = session.get(teams_url)
        if teams_resp.status_code >= 400:
            raise Exception("Failed to fetch teams data. Check your league ID and ESPN S2 cookie if needed.")

        users_resp = session.get(users_url)
        if users_resp.status_code >= 400:
            raise Exception("Failed to fetch users data. Check your league ID and ESPN S2 cookie if needed.")

        schedule_resp = session.get(schedule_url)
        if schedule_resp.status_code >= 400:
            raise Exception("Failed to fetch league schedule")
        schedule_json = schedule_resp.json()["schedule"]

        league_json = league_resp.json()
        teams_json = teams_resp.json()
        users_json = users_resp.json()

        league.name = league_json["settings"]["name"]
        league.total_matchups = max(
            item['matchupPeriodId']
            for item in schedule_json
            if item.get('playoffTierType') == 'NONE'
        )
        league.num_teams = len(league_json["members"])
        
        # Create teams from teams and users data
        for team_data in teams_json["teams"]:
            team = Team(
                id=str(team_data["id"]),
                name=team_data["name"]
            )
            league.teams.append(team)
            league.team_map[str(team_data["id"])] = team

        # Create standardized matchups
        create_standardized_matchups(league, schedule_json)
        
        # Get current matchups played using the common function
        league.curr_matchups_played = get_curr_matchups_played(league)

    # Can't do analysis with less than 2 games played
    if league.curr_matchups_played < 2:
        raise Exception("There must have been at least 2 matchups played already.")

    # Perform team analysis
    perform_team_analysis(league)


def create_standardized_matchups(league: LeagueModel, schedule: List[Dict]) -> None:
    """Convert ESPN schedule format to standardized matchup format"""
    for matchup_data in schedule:
        if matchup_data.get("playoffTierType") != "NONE":
            continue
        matchup = Matchup(
            matchup_id=str(matchup_data["id"]),
            week=matchup_data["matchupPeriodId"],
            home_team_id=str(matchup_data["home"]["teamId"]),
            away_team_id=str(matchup_data["away"]["teamId"]),
            home_score=matchup_data["home"]["totalPoints"],
            away_score=matchup_data["away"]["totalPoints"],
            is_playoffs=matchup_data.get("playoffTierType", "") != ""
        )
        matchup.platform = Platform.ESPN
        league.matchups.append(matchup)
