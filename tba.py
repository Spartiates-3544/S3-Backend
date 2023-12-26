import requests
from dotenv import dotenv_values

env = dotenv_values(dotenv_path='secrets.env')

key = env['API_KEY']
baseurl = env['BASE_URL']

headers = {'X-TBA-Auth-Key' : key}

#Check if API Key is valid
if requests.get(baseurl + '/team/frc3544', headers).status_code == 401:
    raise Exception("API Key is invalid!")

def getTeamInfo(team_key):
    if requests.get(baseurl + f'/team/{team_key}', headers).status_code != 200:
        raise Exception("Team information request failed. Check team code/number.")
    else:
        return requests.get(baseurl + f'/team/{team_key}', headers)

def getEventInfo(event_key):
    if requests.get(baseurl + f'/event/{event_key}', headers).status_code != 200:
        raise Exception("Event information request failed. Check event code.")
    else:
        return requests.get(baseurl + f'/event/{event_key}', headers)
