import http.server
import os
import socketserver
import webbrowser
from contextlib import contextmanager

import export
from league import League

fields = {
    'sport':None,
    'league_id':None,
    'year':None,
    'swid':None,
    'espn_s2':None
}

input_questions = {
    'sport':'\nEnter which sport this league is for (football or baseball): ',
    'league_id':'\nEnter the league ID number for your league (go to your fantasy league and it should show up next to "leagueId=" in the url): ',
    'year':'\nEnter the year this league took place? (if you go to your fantasy team, you might see it in the url next to "seasonId"): ',
    'swid':'\nIf this is a private league, enter your SWID (otherwise just click enter). This is a cookie ESPN uses for authentication (you can find this if you go to https://www.espn.com/ in Chrome and look at cookies for ESPN (click the lock to the left of the url and then click cookies and look for espn.com then look for SWID): ',
    'espn_s2':'\nIf this is a private league, enter your espn_s2 (otherwise just click enter). This is a cookie ESPN uses for authentication (you can find this if you go to https://www.espn.com/ in Chrome and look at cookies for ESPN (click the lock to the left of the url and then click cookies and look for espn.com then look for espn_s2): '
}

def validate_response(field, response):
    '''Validate that responses are somewhat valid'''
    # sport can only take on these values
    if field == 'sport':
        response = response.lower()
        return response == 'baseball' or response == 'football'
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

# From cdunn2001 on StackOverflow: https://stackoverflow.com/questions/431684/how-do-i-change-directory-cd-in-python/24176022#24176022
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

try:
    # First try to read config.txt
    config = open('myconfig.txt')
    # lines = a 2 element list field and value for each line of config.txt
    lines = [[word.strip() for word in line.split('=')] for line in config.readlines()]
    for line in lines:
        field = line[0]
        fields[field] = line[1]
    if not fields['sport'] or not fields['league_id'] or not fields['year']:
        print('\nLooks like you haven\'t filled in your config.txt file (at least not correctly).\nI\'ll just ask you for the information individually.')
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

print('Exporting data to html...')
export.export_league(league)
for team in league.teams:
    export.export_team(team, league)

with cd('site'):
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    while True:
        try:
            httpd = socketserver.TCPServer(("localhost", PORT), Handler)
            print('Serving website at http://localhost:{}/'.format(PORT))
            print('ctrl-c to quit server')
            web_url = 'http://localhost:{}/'.format(PORT)
            webbrowser.open(web_url)
            httpd.allow_reuse_address = True
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
            print('Server Stopped')
            break
        except OSError:
            PORT += 1
            print('Server Stopped')
        except:
            httpd.server_close()
            print('Server Stopped')
            break
