from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Initialize Google Sheets API client with SussyBaka.json
def get_google_sheets_service():
    credentials = Credentials.from_service_account_file('SussyBaka')
    return build('sheets', 'v4', credentials=credentials)

def read_sheet(sheet_id, range_name):
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    return result.get('values', [])

def update_sheet(sheet_id, range_name, values):
    service = get_google_sheets_service()
    body = {'values': values}
    sheet = service.spreadsheets()
    sheet.values().update(spreadsheetId=sheet_id, range=range_name, valueInputOption="RAW", body=body).execute()
