import logging
import pandas
from collections import defaultdict
from src.dataProcessors.models.items import Monster, Cooking
from src.dataProcessors.models.user import User
from src.auth.google_drive import GoogleClient

logger = logging.Logger
grades = ["전설", "초희귀", "희귀", "평범", "꽝"]

class GoogleAPI:
    def __init__(self):
        self.client = GoogleClient().google_auth()

    def get_all_data_from_sheet(self, spread_name, sheet_name):
        google_sheet = self.client.open(spread_name)
        # Extract and print all of the values
        sheet = google_sheet.worksheet(sheet_name)
        data = sheet.get_all_records()
        dataframe = pandas.DataFrame.from_dict(data)

        return dataframe

    def update_user_data(self, spread_name, sheet_name, user_data_dict):
        user_data_list = []
        for _, data in user_data_dict.items():
            object_dict = data.__dict__
            user_data = []
            for _, data in object_dict.items():
                user_data.append(data)
            user_data_list.append(user_data)

        columns = ["이름", "크리스탈", "스테미나", "떡밥", "B급장비개수", "C급장비개수", "골드"]
        user_data_dataframe = pandas.DataFrame(user_data_list, columns=columns)
        google_sheet = self.client.open(spread_name)
        sheet = google_sheet.worksheet(sheet_name)
        sheet.update("A2", user_data_dataframe.values.tolist())


class DataProcessingService:
    def classify_by_grade(self, dataframe):
        classified_data = defaultdict(list)

        for data in dataframe.values:
            classified_data[data[1]].append(
                Monster(
                    name=data[0],
                    grade=data[1],
                    image=data[2],
                    description=data[3],
                    recipe=data[4]
                )
            )
        return classified_data

    def get_cooking_list(self, dataframe):
        cooking_list = []
        for data in dataframe.values:
            cooking_list.append(Cooking(
                name=data[0],
                description=data[1],
                ingredient=data[2]
            ))
        return cooking_list

    def get_user_data_dict(self, dataframe):
        user_data_dict = {}
        for data in dataframe.values:
            user_data_dict.update(
                {
                    data[0]: User(
                        이름=data[0],
                        크리스탈=data[1],
                        스테미나=data[2],
                        떡밥=data[3],
                        B급장비개수=data[4],
                        C급장비개수=data[5],
                        골드=data[6]
                    )
                }
            )

        return user_data_dict

    def get_comment_list(self, dataframe):
        comment_dict = {
            "사냥 멘트": [],
            "낚시 멘트": [],
            "평가": [],
        }
        for data in dataframe.values:
            comment_dict["사냥 멘트"].append(data[0])
            comment_dict["낚시 멘트"].append(data[1])
            comment_dict["평가"].append(data[2])

        comment_dict["사냥 멘트"] = list(filter(None, comment_dict["사냥 멘트"]))
        comment_dict["낚시 멘트"] = list(filter(None, comment_dict["낚시 멘트"]))
        comment_dict["평가"] = list(filter(None, comment_dict["평가"]))

        return comment_dict


