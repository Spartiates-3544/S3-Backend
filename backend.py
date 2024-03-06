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
    if not os.path.isdir(MATCH_DIRECTORY):
        os.mkdir(MATCH_DIRECTORY)

    response = str(qrcode.detect())
    responseJson = response.strip()
    responseJson = json.loads(responseJson)
        
    for match in responseJson:
        path = os.path.join(MATCH_DIRECTORY, '{}{}_{}.json'.format(match['General']['matchType'], match['General']['matchNumber'], match['General']['teamNb']))   
        with open(path, 'w') as file:
            file.write(json.dumps(match))

def scanAndDecode(image):
    if not os.path.isdir(MATCH_DIRECTORY):
        os.mkdir(MATCH_DIRECTORY)

    response = str(qrcode.detect(image))
    responseJson = response.strip()
    responseJson = json.loads(responseJson)
    
    if isinstance(responseJson, list):
        for match in responseJson:
            path = os.path.join(MATCH_DIRECTORY, '{}{}_{}.json'.format(match['General']['matchType'], match['General']['matchNumber'], match['General']['teamNb']))   
            with open(path, 'w') as file:
                file.write(json.dumps(match))
    else:
        path = os.path.join(MATCH_DIRECTORY, '{}{}_{}.json'.format(responseJson['General']['matchType'], responseJson['General']['matchNumber'], responseJson['General']['teamNb']))   
        with open(path, 'w') as file:
            file.write(json.dumps(responseJson))

#This is what has to be changed every year
def generateExcel():
    # try:
        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%dT%H%M')
        rawDataTable = pd.DataFrame()

        rawDataSheetName = 'rawData'
        averagesDataSheetName = 'Team Averages'

        teamList = []

        if not os.path.isdir(OUTPUT_DIRECTORY):
            try:
                os.mkdir(OUTPUT_DIRECTORY)
            except FileExistsError as e:
                print(e)
            else:
                writer = pd.ExcelWriter('{directory:}/{filename:}.xlsx'.format(directory = OUTPUT_DIRECTORY, filename = timestamp), engine='xlsxwriter')
        else:
            writer = pd.ExcelWriter('{directory:}/{filename:}.xlsx'.format(directory = OUTPUT_DIRECTORY, filename = timestamp), engine='xlsxwriter')

        #Create table of all data in matches directory
        for filename in os.listdir(MATCH_DIRECTORY):
            with open(os.path.join(MATCH_DIRECTORY, filename)) as file:
                matchJson = json.load(file)

                #Create list of teams
                team = matchJson['General']['teamNb']
                if not team in teamList:
                    teamList.append(team)

                data = pd.json_normalize(matchJson)
                rawDataTable = pd.concat([rawDataTable, data])

        #Export to excel
        rawDataTable.to_excel(writer, index=False, sheet_name = rawDataSheetName)

        #Adjust the column widths based on the content
        rawDataWorksheet = writer.sheets[rawDataSheetName]    
        for i, col in enumerate(rawDataTable.columns):
            width = max(rawDataTable[col].apply(lambda x: len(str(x))).max(), len(col))
            rawDataWorksheet.set_column(i, i, width)
        
        #Calculate point averages for every team and make DataFrame
        averagesDataTable = pd.DataFrame()

        for team in teamList:
            teamRows = rawDataTable.loc[rawDataTable['General.teamNb'] == team]
            averagesDict = {
                'ampAutonAverage' : teamRows['Autonome.ampPts'].mean(), 'speakerAutonAverage' : teamRows['Autonome.speakerPts'].mean(),
                'ampTeleopAverage' : teamRows['Tele-Op.ampPts'].mean(), 'speakerTeleopAverage' : teamRows['Tele-Op.speakerPts'].mean()
                }
            table = pd.DataFrame(data=averagesDict, index=[team])
            averagesDataTable = pd.concat([averagesDataTable, table])

        #Export to excel
        averagesDataTable.to_excel(writer, index=True, sheet_name=averagesDataSheetName)

        #Adjust the column width based on the content
        averagesWorksheet = writer.sheets[averagesDataSheetName]
        for i, col in enumerate(averagesDataTable.columns):
            width = max(averagesDataTable[col].apply(lambda x: len(str(x))).max(), len(col))
            averagesWorksheet.set_column(i, i, width)

        writer.close()
    # except:
    #     raise Exception('Error generating excel file! Check console output.')
            
generateExcel()
# scanAndDecode()
