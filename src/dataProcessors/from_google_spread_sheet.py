import logging
import time

import gspread.exceptions
import pandas
from collections import defaultdict, namedtuple
from src.auth.google_drive import GoogleClient

logger = logging.Logger
SHEET_NAME = "bot-data-example"

class GoogleAPI:
    def __init__(self):
        self.client = GoogleClient().google_auth()

    def get_all_data_from_sheet(self, spread_name, sheet_name):
        google_sheet = self.client.open(spread_name)

        try:
            # Extract and print all of the values
            sheet = google_sheet.worksheet(sheet_name)
            raw_data = sheet.get_all_records()

        except gspread.exceptions.APIError as error:
            print(error)
            time.sleep(30)
            raw_data = self.get_all_data_from_sheet(self, spread_name, sheet_name)

        return raw_data

    def update_user_data(self, user_data_dict):
        user_data_list = []
        for _, user_object in user_data_dict.items():
            user_data_list.append([data for data in user_object.values()])

        try:
            google_sheet = self.client.open(SHEET_NAME)
            sheet = google_sheet.worksheet("플레이어 데이터")
            sheet.update("A2", user_data_list)

        except gspread.exceptions.APIError as error:
            print(error)
            time.sleep(30)
            self.update_user_data(user_data_dict)

    def update_user_sheet_data_from_google(self, sheet_data: dict):

        try:
            user_raw_data = self.get_all_data_from_sheet(SHEET_NAME, "플레이어 데이터")
            user_data = DataProcessingService().get_user_data_dict(user_raw_data)
            sheet_data.update({"플레이어": user_data})

        except gspread.exceptions.APIError as error:
            print(error)
            time.sleep(30)
            self.update_user_sheet_data_from_google(sheet_data)


class DataProcessingService:
    def generate_sheet_data(self):
        google_api = GoogleAPI()

        equipment_raw_data = google_api.get_all_data_from_sheet(SHEET_NAME, "장비뽑기")
        equipment_data = self.classify_items_by_grade(equipment_raw_data)
        hunting_raw_data = google_api.get_all_data_from_sheet(SHEET_NAME, "사냥")
        hunting_data = self.classify_items_by_grade(hunting_raw_data)
        fishing_raw_data = google_api.get_all_data_from_sheet(SHEET_NAME, "낚시")
        fishing_data = self.classify_items_by_grade(fishing_raw_data)

        cooking_data = google_api.get_all_data_from_sheet(SHEET_NAME, "요리")
        comment_raw_data = google_api.get_all_data_from_sheet(SHEET_NAME, "활동 랜덤 스크립트")
        comment_data = self.get_comment_list(comment_raw_data)

        #### 새로운 시트를 추가할 경우 이 아래에 넣어주세요 ####

        sheet_data = dict(
            장비=equipment_data,
            사냥=hunting_data,
            낚시=fishing_data,
            요리=cooking_data,
            코멘트=comment_data
        )

        #### 새로운 시트 데이터를 추가한 경우 위의 sheet_data에도 데이터를 추가해주세요. ####

        return sheet_data

    def classify_items_by_grade(self, raw_data):
        classified_data = defaultdict(list)

        for item in raw_data:
            classified_data[item["등급"]].append(item)
        return classified_data

    def get_user_data_dict(self, raw_data):
        user_data_dict = {}
        for user in raw_data:
            user_data_dict.update(
                {user["id"]: user}
            )
        return user_data_dict

    def get_comment_list(self, raw_data):
        classified_data = defaultdict(list)
        dataframe = pandas.DataFrame.from_dict(raw_data)
        for comments in dataframe.columns:
            classified_data.update({comments: dataframe[comments]})

        return classified_data


