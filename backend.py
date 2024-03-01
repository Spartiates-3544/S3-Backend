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
    
    with open('{}/{}{}.json'.format(MATCH_DIRECTORY, responseJson['general']['matchType']['value'], responseJson['general']['matchNumber']['value']), 'w') as file:
        file.write(response)

def generateExcel():
    # try:
        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%dT%H%M')
        table = pd.DataFrame()

        rawDataSheet = 'rawData'

        writer = pd.ExcelWriter('{directory:}/{filename:}.xlsx'.format(directory = OUTPUT_DIRECTORY, filename = timestamp), engine  = 'xlsxwriter')

        for filename in os.listdir(MATCH_DIRECTORY):
            with open(os.path.join(MATCH_DIRECTORY, filename)) as file:
                matchJson = json.load(file)
                data = pd.json_normalize(matchJson)
                table = pd.concat([table, data])

        if not os.path.isdir(OUTPUT_DIRECTORY):
            try:
                os.mkdir(OUTPUT_DIRECTORY)
            except FileExistsError as e:
                print(e)
            # else:
            #     table.to_excel('{directory:}/{filename:}.xlsx'.format(directory = OUTPUT_DIRECTORY, filename = timestamp), index=False)
        else:
            table.to_excel(writer, index=False, sheet_name = rawDataSheet)

        # adjust the column widths based on the content
        worksheet = writer.sheets[rawDataSheet]    

        for i, col in enumerate(table.columns):
            width = max(table[col].apply(lambda x: len(str(x))).max(), len(col))
            worksheet.set_column(i, i, width)

        writer.close()
    # except:
    #     raise Exception('Error generating excel file! Check console output.')
            
generateExcel()
