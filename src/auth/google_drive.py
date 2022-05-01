import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials

logger = logging.getLogger()


class GoogleClient:
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.keyfile = ""


    def google_auth(self):
        # use credits to create a client to interact with the Google Drive API
        credit = ServiceAccountCredentials.from_json_keyfile_name(self.keyfile, self.scope)
        client = gspread.authorize(credit)

        return client
