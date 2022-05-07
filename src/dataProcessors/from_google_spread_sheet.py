import logging
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
        # Extract and print all of the values
        sheet = google_sheet.worksheet(sheet_name)
        raw_data = sheet.get_all_records()

        return raw_data

    def update_user_data(self, user_data_dict):
        user_data_list = []
        columns = []
        for _, user_object in user_data_dict.items():
            object_dict = user_object._asdict()
            user_data = []
            columns = object_dict.keys()
            for _, data in object_dict.items():
                user_data.append(data)
            user_data_list.append(user_data)

        user_data_dataframe = pandas.DataFrame(user_data_list, columns=columns)
        google_sheet = self.client.open(SHEET_NAME)
        sheet = google_sheet.worksheet("플레이어 데이터")
        sheet.update("A2", user_data_dataframe.values.tolist())

    def update_user_sheet_data_from_google(self, sheet_data: dict):
        user_raw_data = self.get_all_data_from_sheet(SHEET_NAME, "플레이어 데이터")
        user_data = DataProcessingService().get_user_data_dict(user_raw_data)

        sheet_data.update({"플레이어": user_data})


class DataProcessingService:
    def generate_sheet_data(self):
        google_api = GoogleAPI()

        equipment_raw_data = google_api.get_all_data_from_sheet(SHEET_NAME, "장비뽑기")
        equipment_data = self.classify_items_by_grade(equipment_raw_data)
        hunting_raw_data = google_api.get_all_data_from_sheet(SHEET_NAME, "사냥")
        hunting_data = self.classify_items_by_grade(hunting_raw_data)
        fishing_raw_data = google_api.get_all_data_from_sheet(SHEET_NAME, "낚시")
        fishing_data = self.classify_items_by_grade(fishing_raw_data)

        cooking_raw_data = google_api.get_all_data_from_sheet(SHEET_NAME, "요리")
        cooking_data = self.get_cooking_list(cooking_raw_data)
        user_raw_data = google_api.get_all_data_from_sheet(SHEET_NAME, "플레이어 데이터")
        user_data = self.get_user_data_dict(user_raw_data)
        comment_raw_data = google_api.get_all_data_from_sheet(SHEET_NAME, "활동 랜덤 스크립트")
        comment_data = self.get_comment_list(comment_raw_data)

        sheet_data = dict(
            장비=equipment_data,
            사냥=hunting_data,
            낚시=fishing_data,
            요리=cooking_data,
            플레이어=user_data,
            코멘트=comment_data
        )
        return sheet_data

    def classify_items_by_grade(self, raw_data):
        classified_data = defaultdict(list)

        for data_dict in raw_data:
            item = namedtuple("Item", data_dict.keys())(*data_dict.values())
            classified_data[item.등급].append(item)
        return classified_data

    def get_cooking_list(self, raw_data):
        cooking_list = []
        for data_dict in raw_data:
            cooking = namedtuple("Item", data_dict.keys())(*data_dict.values())
            cooking_list.append(cooking)
        return cooking_list

    def get_user_data_dict(self, raw_data):
        user_data_dict = {}
        for data_dict in raw_data:
            user = namedtuple("Item", data_dict.keys())(*data_dict.values())
            user_data_dict.update(
                {user.id: user}
            )
        return user_data_dict

    def get_comment_list(self, raw_data):
        classified_data = defaultdict(list)
        dataframe = pandas.DataFrame.from_dict(raw_data)
        for comments in dataframe.columns:
            classified_data.update({comments: dataframe[comments]})

        return classified_data


