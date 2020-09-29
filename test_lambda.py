from lambda_local.main import call
from lambda_local.context import Context

import application

def main():
    event = {
        "sport": "football",
        "platform": "espn",
        "leagueId": "264572",
        "year": "2020",
        "espnS2": "AEBZdjDCIUphHU4R2CzpqU0nyreubFNqzmP%2FCzWFwfL%2BCLG%2BxVjYoVuW6poxYdqU8gT3F4ni3GtVrj%2ByB1lzMgSirVPEsly0STsdhOY8yfiPvB4opi7xjJs7x7y2al5hSKwq4L6xHrX%2FBQIOeG2GNUZ0U1ZyOiWFkOlCwpDxZ8wbofUb2wwbj0zicjYcdrnCGF0VT5dxpZZm0jOsvMbMREiAUk8DJkizayo%2FSFPzsAoQvcqSgl9nuciiD3pKwnt8RiXye810jW42eswyhhBN18Kr"
    }
    context = Context(5)

    call(application.handler, event, context)

    event = {
        "sport": "football",
        "platform": "espn",
        "leagueId": "1667842",
        "year": "2020",
        "espnS2": "AEBZdjDCIUphHU4R2CzpqU0nyreubFNqzmP%2FCzWFwfL%2BCLG%2BxVjYoVuW6poxYdqU8gT3F4ni3GtVrj%2ByB1lzMgSirVPEsly0STsdhOY8yfiPvB4opi7xjJs7x7y2al5hSKwq4L6xHrX%2FBQIOeG2GNUZ0U1ZyOiWFkOlCwpDxZ8wbofUb2wwbj0zicjYcdrnCGF0VT5dxpZZm0jOsvMbMREiAUk8DJkizayo%2FSFPzsAoQvcqSgl9nuciiD3pKwnt8RiXye810jW42eswyhhBN18Kr"
    }
    context = Context(5)

    call(application.handler, event, context)

if __name__ == "__main__":
    main()
