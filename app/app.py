# https://developers.google.com/sheets/api/guides/values#python_4
# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/create
import os
import requests
import json
import sys
from dotenv import load_dotenv
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

load_dotenv()
SAMPLE_SPREADSHEET_ID = os.getenv('SAMPLE_SPREADSHEET_ID')
SAMPLE_RANGE_NAME = os.getenv('SAMPLE_RANGE_NAME')
WRITE_RANGE_NAME  = os.getenv('WRITE_RANGE_NAME')

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main(params):
    creds = None
    SERVICE_ACCOUNT_FILE = './credentials.json'
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    if params[1] == "1":
        getListOfPages(sheet) 
    else:    
        writeSpreadSheet(sheet, [params[2],params[3]])

def writeSpreadSheet(sheet, data):
    values =[data]
    body = {
        'values': values
    }
    request = sheet.values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, 
        range=WRITE_RANGE_NAME,
        valueInputOption="RAW", 
        body=body)
    #request = sheet.values().update(
    #    spreadsheetId=SAMPLE_SPREADSHEET_ID, 
    #    range=WRITE_RANGE_NAME, 
    #    valueInputOption="RAW", 
    #    body=body)
    result = request.execute()    
    print(result)

def getListOfPages(sheet):
    result = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="List"+SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    listOfUrls=""
    for urls in values:
        for url in urls:
            listOfUrls=url if not len(listOfUrls) else listOfUrls+","+str(url)
    print(listOfUrls)


if __name__ == '__main__':
    main(sys.argv)