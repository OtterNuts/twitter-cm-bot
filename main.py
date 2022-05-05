from src.auth.twitter import TwitterClient
from src.auth.google_drive import GoogleClient
import logging
from src.dataProcessors.from_text_file import RWDataFromTextFile
import time
from src.dataProcessors.from_google_spread_sheet import GoogleAPI, DataProcessingService
from src.tweetBot.update_tweet import TweetBot

logger = logging.Logger

#activity_list = ["오늘의운세", "[낚시]", "[사냥]", "[요리]", "[장비뽑기]", "[tmi보기]", "[하급장비판매]", "[일괄판매]", "[중급장비판매]", "[할로윈요리]"]
activity_list = ["오늘의운세", "[사냥]", "[요리]", "[낚시]", "[장비뽑기]", "[로또뽑기]", "[불꽃놀이]"]


def main():
    # get all spreadsheet data from google spreadsheet
    sheet_data = DataProcessingService().generate_sheet_data()
    print("data is ready")

    # operate tweet bot
    twitter_client = TwitterClient().tweeter_auth()
    latest_mention = RWDataFromTextFile().open_file()
    since_id = int(latest_mention)
    while True:
        since_id = TweetBot().check_mentions(twitter_client, activity_list, since_id, sheet_data)
        time.sleep(15)


if __name__ == "__main__":
    main()
