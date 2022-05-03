import tweepy
import logging
import time
from src.dataProcessors.from_text_file import RWDataFromTextFile
from src.dataProcessors.from_google_spread_sheet import GoogleAPI
from random import randint, sample
from src.tweetBot.models.tweet import Tweet
from src.tweetBot.activities import Activities

logging.basicConfig(level=logging.INFO)

firework_image = ['firework1.jpg', 'firework2.jpg', 'firework3.jpg', 'firework4.jpg', 'firework5.jpg']
REQUIRED_STAMINA = 20
REQUIRED_BITE = 1

class TweetBot:
    def __init__(self):
        self.google_api = GoogleAPI()
        self.activities = Activities()
        self.bot_id = "@Serendity_Dice"
        self.image_path = "src/tweetBot/images/"

    def check_mentions(self, api, keywords, since_id, sheet_data):
        latest_id = since_id
        received_tweets = []
        for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
            if tweet.in_reply_to_status_id is not None:
                continue
            new_tweet = Tweet(id=tweet.id, user=tweet.user, text=tweet.text)
            received_tweets.append(new_tweet)

        for tweet in reversed(received_tweets):
            try:
                latest_id = tweet.id
                user_id = tweet.user.screen_name
                task_name = ""
                for keyword in keywords:
                    if keyword in tweet.text.lower():
                        task_name = keyword

                if task_name != "":
                    print(f"Answering to {tweet.user.name}")
                    print(tweet.id)
                    reply = self.generate_reply(sheet_data, task_name, tweet)

                    if reply["reply_image"] is not None:
                        api.update_status_with_media(
                            filename=self.image_path + reply["reply_image"],
                            status="@%s" % user_id + reply["reply_comment"],
                            in_reply_to_status_id=tweet.id,
                        )
                    else:
                        api.update_status(
                            status="@%s" % user_id + reply["reply_comment"],
                            in_reply_to_status_id=tweet.id,
                        )

            except tweepy.errors.TweepyException as err:
                print(err, "에러가 발생했습니다. 오류 메시지를 확인하세요.")
                RWDataFromTextFile().update_file(latest_id)

        RWDataFromTextFile().update_file(latest_id)
        return latest_id

    def generate_reply(self, sheet_data, task_name: str, tweet: Tweet):
        user_id = tweet.user.screen_name
        user_name = tweet.user.name
        reply_image = ""

        if task_name == "오늘의운세":
            reply_comment = "@%s" % user_id + " " + self.activities.todays_fortune()

        elif task_name == "[불꽃놀이]":
            value = randint(0, 4)
            text = tweet.text.replace(self.bot_id, "")
            text = text.replace("[불꽃놀이]", "")
            reply_image = self.image_path + firework_image[value]
            reply_comment = user_name + "(이)가 불꽃을 쏘아올립니다.\n\n<<" + text + " >>"

        elif task_name == "[로또뽑기]":
            randoms = sample(range(1, 46), 10)
            number_script = ', '.join(str(random) for random in randoms)
            reply_image = self.image_path + "lottery.jpeg"
            reply_comment = "@%s" % user_id + " " + number_script

        elif task_name == "[요리]":
            print("요리 시작")
            reply_comment = "@%s" % tweet.user.screen_name + self.activities.cooking(sheet_data["요리"], sheet_data["코멘트"]["요리 평가"])

        elif task_name == "[낚시]":
            print("낚시 시작")
            user_bites = sheet_data["플레이어"][user_name].떡밥
            fishing_comments = sheet_data["코멘트"]["낚시 멘트"]
            if user_bites >= REQUIRED_BITE:
                fishing_result = self.activities.activity_result(sheet_data["낚시"], fishing_comments)
                reply_image = fishing_result["image_name"]
                reply_comment = "@%s" % user_id + fishing_result["comment"]

                sheet_data["플레이어"][user_name].떡밥 = user_bites - REQUIRED_BITE
                self.google_api.update_user_data("플레이어", "test", sheet_data["플레이어"])
            else:
                reply_comment = "@%s" % user_id + "떡밥이 부족하거나 없는 유저명입니다. 상점에서 떡밥 구입하세요."
            time.sleep(2)

        elif task_name == "[사냥]":
            print("사냥 시작")
            user_stamina = sheet_data["플레이어"][user_name].스테미나
            hunting_comments = sheet_data["코멘트"]["사냥 멘트"]
            if user_stamina >= REQUIRED_STAMINA:
                hunt_result = self.activities.activity_result(sheet_data["사냥"], hunting_comments)
                reply_image = hunt_result["image_name"]
                reply_comment = "@%s" % user_id + hunt_result["comment"]

                sheet_data["플레이어"][user_name].스테미나 = user_stamina - REQUIRED_STAMINA
                self.google_api.update_user_data("플레이어", "test", sheet_data["플레이어"])
            else:
                reply_comment = "@%s" % user_id + "스테미나가 부족하거나 없는 유저명입니다. 상점에서 회복약을 구입하거나 스테미나가 회복될 때까지 기다려주세요."
            time.sleep(2)

        else:
            reply_comment = "@%s 오류입니다. 해당 트윗과 봇에 보낸 트윗을 캡쳐해서 총괄계 디엠으로 보내주세요." % user_id

        return {"reply_image": reply_image, "reply_comment": reply_comment}



