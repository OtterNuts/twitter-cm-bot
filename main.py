from src.auth.twitter import TwitterClient
from src.auth.google_drive import GoogleClient
import logging
from src.dataProcessors.from_text_file import RWDataFromTextFile
import time
from src.dataProcessors.from_google_spread_sheet import GoogleAPI, DataProcessingService
from src.tweetBot.update_tweet import TweetBot

logger = logging.Logger

#activity_list = ["오늘의운세", "[낚시]", "[사냥]", "[요리]", "[장비뽑기]", "[tmi보기]", "[하급장비판매]", "[일괄판매]", "[중급장비판매]", "[할로윈요리]"]
activity_list = ["오늘의운세", "[사냥]", "[요리]", "[로또뽑기]", "[불꽃놀이]"]


def main():
    # get all spreadsheet data from google spreadsheet
    google_api = GoogleAPI()
    data_process_service = DataProcessingService()

    hunting_raw_data = google_api.get_all_data_from_sheet("server_burangza", "사냥v2")
    hunting_data = data_process_service.classify_by_grade(hunting_raw_data)
    cooking_raw_data = google_api.get_all_data_from_sheet("server_burangza", "요리")
    cooking_data = data_process_service.get_cooking_list(cooking_raw_data)
    user_raw_data = google_api.get_all_data_from_sheet("플레이어", "test")
    user_data = data_process_service.get_user_data_dict(user_raw_data)
    comment_raw_data = google_api.get_all_data_from_sheet("server_burangza", "활동 랜덤 스크립트")
    comment_data = data_process_service.get_comment_list(comment_raw_data)

    sheet_data = dict(
        사냥=hunting_data,
        요리=cooking_data,
        플레이어=user_data,
        코멘트=comment_data
    )

    print("data is ready")
    time.sleep(10)

    # operate tweet bot
    twitter_client = TwitterClient().tweeter_auth()
    latest_mention = RWDataFromTextFile().open_file()
    since_id = int(latest_mention)
    while True:
        since_id = TweetBot().check_mentions(twitter_client, activity_list, since_id, sheet_data)
        time.sleep(15)


if __name__ == "__main__":
    main()
