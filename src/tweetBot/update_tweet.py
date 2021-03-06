import tweepy
import logging
import time
from src.dataProcessors.from_text_file import RWDataFromTextFile
from src.dataProcessors.from_google_spread_sheet import GoogleAPI
from random import sample
from src.tweetBot.models.tweet import Tweet
from src.tweetBot.activities import Activities

logging.basicConfig(level=logging.INFO)

REQUIRED_STAMINA = 20
REQUIRED_BITE = 1
REQUIRED_CRYSTAL = 3000

class TweetBot:
    def __init__(self):
        self.google_api = GoogleAPI()
        self.activities = Activities()
        self.image_path = "src/tweetBot/images/"

    def check_mentions(self, api, keywords, since_id, sheet_data):
        latest_id = since_id
        received_tweets = []
        for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
            if tweet.in_reply_to_status_id is not None:
                continue
            new_tweet = Tweet(id=tweet.id, user=tweet.user, text=tweet.text)
            received_tweets.append(new_tweet)

        self.google_api.update_user_sheet_data_from_google(sheet_data)
        for tweet in reversed(received_tweets):
            try:
                latest_id = tweet.id
                user_id = tweet.user.screen_name
                user_list = sheet_data["플레이어"].keys()
                task_name = ""
                for keyword in keywords:
                    if keyword in tweet.text.lower():
                        task_name = keyword

                if user_id not in user_list:
                    api.update_status(
                        status="@%s " % user_id + "존재하지 않는 플레이어입니다. 시트 정보를 다시 확인해주세요.",
                        in_reply_to_status_id=tweet.id,
                    )
                    continue

                if task_name == "":
                    api.update_status(
                        status="@%s" % user_id + "존재하지 않는 명령어 입니다. 명령어를 확인해주세요.",
                        in_reply_to_status_id=tweet.id,
                    )
                    continue

                print(f"Answering to {tweet.user.name}")
                print(tweet.id)
                if task_name == "[장비뽑기]":
                    replies = self.generate_gotcha_comment(sheet_data, tweet)
                else:
                    replies = self.generate_reply(sheet_data, task_name, tweet)

                for reply in replies:
                    if reply["reply_image"]:
                        api.update_status_with_media(
                            filename=self.image_path + reply["reply_image"],
                            status=reply["reply_comment"],
                            in_reply_to_status_id=tweet.id,
                        )
                    else:
                        api.update_status(
                            status=reply["reply_comment"],
                            in_reply_to_status_id=tweet.id,
                        )
                time.sleep(3)

            except tweepy.errors.TweepyException as err:
                api.update_status(
                    status="@%s" % tweet.user.screen_name + "봇 오류입니다. 캡쳐와 함께 총괄계에 문의 부탁드립니다.",
                    in_reply_to_status_id=tweet.id,
                )
                print(err, "에러가 발생했습니다. 오류 메시지를 확인하세요.")
                RWDataFromTextFile().update_file(latest_id)

            # save updated data
            RWDataFromTextFile().update_file(latest_id)

        self.google_api.update_user_data(sheet_data["플레이어"])
        return latest_id

    def generate_reply(self, sheet_data, task_name: str, tweet: Tweet):
        user_id = tweet.user.screen_name
        reply_image = ""

        if task_name == "오늘의운세":
            reply_comment = "@%s" % user_id + " " + self.activities.todays_fortune()

        elif task_name == "[로또뽑기]":
            randoms = sample(range(1, 46), 10)
            number_script = ', '.join(str(random) for random in randoms)
            reply_image = "lottery.png"
            reply_comment = "@%s" % user_id + " " + number_script

        elif task_name == "[요리]":
            print("요리 시작")
            reply_comment = "@%s" % user_id + self.activities.cooking(sheet_data["요리"], sheet_data["코멘트"]["요리_평가"])

        elif task_name == "[낚시]":
            print("낚시 시작")
            user_bites = sheet_data["플레이어"][user_id]["떡밥"]
            fishing_comments = sheet_data["코멘트"]["낚시_멘트"]
            if user_bites >= REQUIRED_BITE:
                fishing_result = self.activities.activity_result(sheet_data["낚시"], fishing_comments)
                reply_image = fishing_result["image_name"]
                reply_comment = "@%s" % user_id + fishing_result["comment"]

                # update user data
                sheet_data["플레이어"][user_id]["떡밥"] -= REQUIRED_BITE
            else:
                reply_comment = "@%s" % user_id + "떡밥이 부족하거나 없는 유저명입니다. 상점에서 떡밥 구입하세요."

        elif task_name == "[사냥]":
            print("사냥 시작")
            user_stamina = sheet_data["플레이어"][user_id]["스테미나"]
            hunting_comments = sheet_data["코멘트"]["사냥_멘트"]
            if user_stamina >= REQUIRED_STAMINA:
                hunt_result = self.activities.activity_result(sheet_data["사냥"], hunting_comments)
                reply_image = hunt_result["image_name"]
                reply_comment = "@%s" % user_id + hunt_result["comment"]

                # update user data
                sheet_data["플레이어"][user_id]["스테미나"] -= REQUIRED_STAMINA
            else:
                reply_comment = "@%s" % user_id + "스테미나가 부족하거나 없는 유저명입니다. 상점에서 회복약을 구입하거나 스테미나가 회복될 때까지 기다려주세요."

        elif task_name == "[일괄판매]":
            print("일괄판매 시작")
            num_c_equip = sheet_data["플레이어"][user_id]["C급장비개수"]
            num_b_equip = sheet_data["플레이어"][user_id]["B급장비개수"]
            if int(num_b_equip) + int(num_c_equip) == 0:
                reply_comment = "장비가 없습니다. 인벤토리를 확인해주세요."
            else:
                sell_total = 5000 * int(num_b_equip) + 1000 * int(num_c_equip)
                reply_comment = "@%s" % user_id + f"[장비판매]\nB급장비개수: {num_b_equip}\nC급장비개수: {num_c_equip}\n총가격: {str(sell_total)}"

                # update user data
                sheet_data["플레이어"][user_id]["골드"] += sell_total
                sheet_data["플레이어"][user_id]["C급장비개수"] = 0
                sheet_data["플레이어"][user_id]["B급장비개수"] = 0
                
                
        ##### 새로운 기능을 추가하길 바랄 경우 여기에 elif 구문으로 코드를 추가하세요 #####

        else:
            reply_comment = "@%s" % user_id + "봇 오류입니다. 캡쳐와 함께 총괄계에 문의 부탁드립니다."

        return [{"reply_image": reply_image, "reply_comment": reply_comment}]

    def generate_gotcha_comment(self, sheet_data, tweet: Tweet):
        gotcha_result = self.activities.gotcha_result(sheet_data["장비"])
        user_id = tweet.user.screen_name

        print("가챠 시작")
        user_crystal = sheet_data["플레이어"][user_id]["크리스탈"]
        if user_crystal >= REQUIRED_CRYSTAL:
            replies = [{"reply_image": gotcha_result["image_name"], "reply_comment": "@%s" % user_id}]

            normal_equips = ""
            for c_equip in gotcha_result["equip_list"]["C급"]:
                normal_equips += f'[{c_equip["등급"]}]{c_equip["장비명"]}: {c_equip["설명"]}\n'
            for b_equip in gotcha_result["equip_list"]["B급"]:
                normal_equips += f'[{b_equip["등급"]}]{b_equip["장비명"]}: {b_equip["설명"]}\n'
            for a_equip in gotcha_result["equip_list"]["A급"]:
                normal_equips += f'[{a_equip["등급"]}]{a_equip["장비명"]}: {a_equip["설명"]}\n'

            chunks = [normal_equips[i:i + 140].lstrip() for i in range(0, len(normal_equips), 140)]
            for chunk in chunks:
                replies.append({"reply_image": "", "reply_comment": "@%s " % user_id + chunk})

            for s_equip in gotcha_result["equip_list"]["S급"]:
                replies.append(
                    {
                        "reply_image": s_equip["이미지"],
                        "reply_comment": "@%s" % user_id + f'[{s_equip["등급"]}]{s_equip["장비명"]}: {s_equip["설명"]}\n'
                    }
                )

            num_c_equip = len(gotcha_result["equip_list"]["C급"])
            num_b_equip = len(gotcha_result["equip_list"]["B급"])

            # update user data
            sheet_data["플레이어"][user_id]["크리스탈"] -= REQUIRED_CRYSTAL
            sheet_data["플레이어"][user_id]["C급장비개수"] += num_c_equip
            sheet_data["플레이어"][user_id]["B급장비개수"] += num_b_equip

        else:
            reply_comment = "@%s" % user_id + "크리스탈 부족하거나 없는 유저명입니다. 상점에서 크리스탈을 구매해주세요."
            replies = [{"reply_image": "", "reply_comment": reply_comment}]

        return replies

