from src.auth.twitter import TwitterClient
import logging
from src.dataProcessors.from_text_file import RWDataFromTextFile
import time
from src.dataProcessors.from_google_spread_sheet import DataProcessingService
from src.tweetBot.update_tweet import TweetBot

logger = logging.Logger
activity_list = ["오늘의운세", "[사냥]", "[요리]", "[낚시]", "[장비뽑기]", "[로또뽑기]", "[일괄판매]"]

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
