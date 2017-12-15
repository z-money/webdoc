from __future__ import print_function
import httplib2
import os
from pprint import pprint
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def append(spreadsheet_id, values, range, service, value_input_option = 'RAW', insert_data_option = 'INSERT_ROWS', major_dimension = 'ROWS'):

    value_range_body = {
        "range": range,
        "majorDimension": major_dimension,
        "values": values,
    }

    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()
    return response


def dict_to_values(dict):
    values = []
    for key in dict:
        values.append([key, dict[key]['status'], dict[key]['page']])
    return values


def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheet_id = '1_sjswq4RcnoLT6DLZzxgKxoEl1LUsa1Mb6b7nkzipdQ'


    clear_range = 'A:D'

    clear_values_request_body = {
        # TODO: Add desired entries to the request body.
    }
    request = service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=clear_range, body=clear_values_request_body)
    response = request.execute()

    data = json.load(open('results.json'))
    append_range = 'A:C'
    values = dict_to_values(data)
    append(spreadsheet_id, values, append_range, service)

    # result = service.spreadsheets().values().get(
    #     spreadsheetId=spreadsheetId, range=rangeName).execute()
    # values = result.get('values', [])

    # if not values:
    #     print('No data found.')
    # else:
    #     for row in values:
    #         # Print columns A and E, which correspond to indices 0 and 4.
    #         print('%s' % row[0])


if __name__ == '__main__':
    main()
