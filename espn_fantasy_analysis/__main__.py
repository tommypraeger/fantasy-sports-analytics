from league import League
import export

fields = {
    'sport':None,
    'league_id':None,
    'year':None,
    'swid':None,
    'espn_s2':None
}

input_questions = {
    'sport':'\nEnter which sport this league is for (football, baseball, or basketball): ',
    'league_id':'\nEnter the league ID number for your league (go to your fantasy league and it should show up next to "leagueId=" in the url): ',
    'year':'\nEnter the year this league took place? (if you go to your fantasy team, you might see it in the url next to "seasonId"): ',
    'swid':'\nIf this is a private league, enter your SWID (otherwise just click enter). This is a cookie ESPN uses for authentication (you can find this if you go to https://www.espn.com/ in Chrome and look at cookies for ESPN (click the lock to the left of the url and then click cookies and look for espn.com then look for SWID): ',
    'espn_s2':'\nIf this is a private league, enter your espn_s2 (otherwise just click enter). This is a cookie ESPN uses for authentication (you can find this if you go to https://www.espn.com/ in Chrome and look at cookies for ESPN (click the lock to the left of the url and then click cookies and look for espn.com then look for espn_s2): '
}

def validate_response(field, response):
    '''Validate that responses are somewhat valid'''
    # sport can only take on these values
    if field == 'sport':
        return response == 'baseball' or response == 'football' or response == 'basketball'
    # league_id and year must be a number at the very least
    elif field == 'league_id' or field == 'year':
        try:
            int(response)
            return true
        except ValueError:
            return False
    return True

def collect_fields():
    '''Collect the necessary metadata and auth info from the user'''
    for field in input_questions.keys():
        fields[field] = input(input_questions[field])
        # Ask again if response was not valid
        while not validate_response(field, fields[field]):
            print('\nThat didn\'t seem to be a valid response. Try again.')
            fields[field] = input(input_questions[field])

try:
    # First try to read config.txt
    config = open('myconfig.txt')
    # lines = a 2 element list field and value for each line of config.txt
    lines = [[word.strip() for word in line.split('=')] for line in config.readlines()]
    for line in lines:
        field = line[0]
        # field must be an expected field and line must have 1 equals sign
        if field not in fields.keys() or len(line) != 2:
            print('\nLooks like you haven\'t filled in your config.txt file (at least not correctly).\nI\'ll just ask you for the information individually.')
            collect_fields()
            break
        fields[field] = line[1]
    # In case they deleted these lines from config.txt for some reason
    if not fields['sport'] or not fields['league_id'] or not fields['year']:
        print('Looks like you\'re missing an essential field.\nI\'ll ask you for the information individually.')
        collect_fields()
except FileNotFoundError:
    # In case I can't open config.txt
    print('\nLooks like you deleted the config.txt file (or something like that). That\'s ok, I\'ll just ask you for the information individually.')
    collect_fields()

print('Fetching league data...')
league = League(fields)
league.fetch_league()

print('Doing calculations...')
league.perform_team_analysis()
#league.perform_league_analysis()
league.teams.sort(key=lambda team: sum(team.win_likelihoods[:league.curr_matchups_played]), reverse=True)

print('Exporting data to csv...')
export.export_league(league)
for team in league.teams:
    export.export_team(team)