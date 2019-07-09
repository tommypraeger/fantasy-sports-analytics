from league import League
import sys

fields = {
    'sport':None,
    'leagueId':None,
    'year':None,
    'swid':None,
    'espn_s2':None
}
def collectFields():
    pass

if len(sys.argv) != 2:
    collectFields()
else:
    try:
        config = open(sys.argv[1])
    except FileNotFoundError:
        print('I\'m unable to open your txt file.\nI\'ll just ask you for the information individually.')
        collectFields()
    lines = [[word.strip() for word in line.split('=')] for line in config.readlines()]
    for line in lines:
        field = line[0]
        if field not in fields.keys():
            print('Uh oh. Looks like you have an incorrect field in your txt file.\nI\'ll just ask you for the information individually.')
            collectFields()
            break
        fields[field] = line[1]
    if not fields['sport'] or not fields['leagueId'] or not fields['year']:
        print('Looks like you\'re missing an essential field.\nI\'ll ask you for the information individually.')
        collectFields()

league = League(fields)
league.fetchLeague()