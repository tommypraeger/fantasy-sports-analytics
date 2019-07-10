from league import League

fields = {
    'sport':None,
    'leagueId':None,
    'year':None,
    'swid':None,
    'espn_s2':None
}

inputQuestions = {
    'sport':'\nEnter which sport this league is for (football, baseball, or basketball): ',
    'leagueId':'\nEnter the league ID number for your league (go to your fantasy league and it should show up next to "leagueId=" in the url): ',
    'year':'\nEnter the year this league took place? (if you go to your fantasy team, you might see it in the url next to "seasonId"): ',
    'swid':'\nIf this is a private league, enter your SWID (otherwise just click enter). This is a cookie ESPN uses for authentication (you can find this if you go to https://www.espn.com/ in Chrome and look at cookies for ESPN (click the lock to the left of the url and then click cookies and look for espn.com then look for SWID): ',
    'espn_s2':'\nIf this is a private league, enter your espn_s2 (otherwise just click enter). This is a cookie ESPN uses for authentication (you can find this if you go to https://www.espn.com/ in Chrome and look at cookies for ESPN (click the lock to the left of the url and then click cookies and look for espn.com then look for espn_s2): '
}
def validateResponse(field, response):
    if field == 'sport':
        return response == 'baseball' or response == 'football' or response == 'basketball'
    elif field == 'leagueId' or field == 'year':
        try:
            int(response)
            return True
        except ValueError:
            return False
    return True
def collectFields():
    for field in inputQuestions.keys():
        fields[field] = input(inputQuestions[field])
        while not validateResponse(field, fields[field]):
            print('\nThat didn\'t seem to be a valid response. Try again.')
            fields[field] = input(inputQuestions[field])

try:
    config = open('config.txt')
    lines = [[word.strip() for word in line.split('=')] for line in config.readlines()]
    for line in lines:
        field = line[0]
        if field not in fields.keys() or len(line) != 2:
            print('\nLooks like you haven\'t filled in your config.txt file (at least not correctly).\nI\'ll just ask you for the information individually.')
            collectFields()
            break
        fields[field] = line[1]
    if not fields['sport'] or not fields['leagueId'] or not fields['year']:
        print('Looks like you\'re missing an essential field.\nI\'ll ask you for the information individually.')
        collectFields()
except FileNotFoundError:
    print('Looks like you deleted the config.txt file (or something like that). That\'s ok, I\'ll just ask you for the information individually.')
    collectFields()

league = League(fields)
league.fetchLeague()