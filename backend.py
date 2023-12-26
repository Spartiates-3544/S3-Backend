import qrcode
import json
import os
from datetime import datetime
import pandas as pd
from dotenv import dotenv_values

env = dotenv_values(dotenv_path='secrets.env')
MATCH_DIRECTORY = 'matches'
OUTPUT_DIRECTORY = 'output'

def scanAndDecode():
    if not os.path.isdir('matches'):
        os.mkdir(MATCH_DIRECTORY)

    response = str(qrcode.detect())
    responseJson = response.strip()
    responseJson = json.loads(responseJson)
    
    with open('{}/{}{}.json'.format(MATCH_DIRECTORY, responseJson['general']['matchType'], responseJson['general']['matchNumber']), 'w') as file:
        file.write(response)

def generateExcel():
    try:
        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%dT%H%M')
        table = pd.DataFrame()

        for filename in os.listdir(MATCH_DIRECTORY):
            with open(os.path.join(MATCH_DIRECTORY, filename)) as file:
                data = pd.json_normalize(json.load(file))
                table = pd.concat([table, data])

        if not os.path.isdir(OUTPUT_DIRECTORY):
            try:
                os.mkdir(OUTPUT_DIRECTORY)
            except FileExistsError as e:
                print(e)
            else:
                table.to_excel('{directory:}/{filename:}.xlsx'.format(directory = OUTPUT_DIRECTORY, filename = timestamp), index=False)
        else:
            table.to_excel('{directory:}/{filename:}.xlsx'.format(directory = OUTPUT_DIRECTORY, filename = timestamp), index=False)
    except:
        raise Exception('Error generating excel file! Check console output.')