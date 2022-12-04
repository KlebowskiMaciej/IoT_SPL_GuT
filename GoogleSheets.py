from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

#Connect Var
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = '1Zp1LpEPU9mKX3K8ayC0PYN-GMqW9NP41S88rpUiwMv0'
SAMPLE_RANGE_NAME = 'A:E'


class GoogleWrite:
     
	def send(self,val,Times):
		creds = None
		
		#Maybe could cut.. ToDo
		if os.path.exists('token.json'):
			creds = Credentials.from_authorized_user_file('token.json', SCOPES)
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
				creds = flow.run_local_server(port=0)
			# Dane uwierzytelniające zostają zapisane w pliku ‘token.json’
			with open('token.json', 'w') as token:
				token.write(creds.to_json())

		service = build('sheets', 'v4', credentials=creds)

		# Uruchomienie usługi dostępu do arkusza
		sheet = service.spreadsheets()
		result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
		values = result.get('values', [])
		
		liczby = (
      			( str(val)),
         		(str(Times)))

		if not values:
			print('No data found.')
		else:
			print('Name, Major:')

		bodyexample = {
						"range": "A:B",
						"majorDimension": 'ROWS',
						"values": [ liczby ]
		}

		request = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="A:B", valueInputOption='USER_ENTERED', body=bodyexample)
		response = request.execute()
		print(response)


