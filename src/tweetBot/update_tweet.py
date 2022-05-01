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
MINIMUM_STAMINA = 20

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
                user_name = tweet.user.name
                task_name = ""

                for keyword in keywords:
                    if keyword in tweet.text.lower():
                        task_name = keyword

                if task_name != "":
                    print(f"Answering to {tweet.user.name}")
                    print(tweet.id)
                    # save replied tweet's id

                    if task_name == "오늘의운세":
                        api.update_status(
                            status="@%s " % user_id + self.activities.todays_fortune(),
                            in_reply_to_status_id=tweet.id,
                        )

                    elif task_name == "[불꽃놀이]":
                        value = randint(0, 4)
                        text = tweet.text.replace(self.bot_id, "")
                        text = text.replace("[불꽃놀이]", "")
                        api.update_with_media(
                            firework_image[self.image_path + value],
                            status=user_name + "(이)가 불꽃을 쏘아올립니다.\n\n<<" + text + " >>",
                        )

                    elif task_name == "[로또뽑기]":
                        randoms = sample(range(1, 46), 10)
                        number_script = ', '.join(str(random) for random in randoms)
                        api.update_with_media(
                            "images/lottery.jpeg",
                            status="@%s" % user_id + " " + number_script,
                            in_reply_to_status_id=tweet.id,
                        )

                    elif task_name == "[사냥]":
                        print("사냥 시작")
                        user_stamina = sheet_data["플레이어"][user_name].스테미나
                        hunting_comments = sheet_data["코멘트"]["사냥 멘트"]

                        if user_stamina >= MINIMUM_STAMINA:
                            hunt_result = self.activities.activity_result(sheet_data["사냥"], hunting_comments)
                            if hunt_result["image_name"]:
                                api.update_status_with_media(
                                    filename=self.image_path + hunt_result["image_name"],
                                    status="@%s" % tweet.user.screen_name + hunt_result["comment"],
                                    in_reply_to_status_id=tweet.id,
                                )
                            else:
                                api.update_status(
                                    status="@%s" % tweet.user.screen_name + hunt_result["comment"],
                                    in_reply_to_status_id=tweet.id,
                                )
                            sheet_data["플레이어"][user_name].스테미나 = user_stamina-20
                            self.google_api.update_user_data("플레이어", "test", sheet_data["플레이어"])
                        else:
                            api.update_status(
                                status="@%s" % tweet.user.screen_name
                                       + "스테미나가 부족하거나 없는 유저명입니다. 상점에서 회복약을 구입하거나 스테미나가 회복될 때까지 기다려주세요.",
                                in_reply_to_status_id=tweet.id,
                            )
                        time.sleep(2)

                    else:
                        api.update_status(
                            status="@%s 오류입니다. 해당 트윗과 봇에 보낸 트윗을 캡쳐해서 총괄계 디엠으로 보내주세요." % tweet.user.screen_name,
                            in_reply_to_status_id=tweet.id,
                        )

            except tweepy.errors.TweepyException as err:
                print(err, "에러가 발생했습니다. 오류 메시지를 확인하세요.")
                RWDataFromTextFile().update_file(latest_id)

        RWDataFromTextFile().update_file(latest_id)
        return latest_id
