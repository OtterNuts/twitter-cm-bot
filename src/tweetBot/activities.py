from random import randint
from src.dataProcessors.models.items import Monster

class Activities:
    def todays_fortune(self):
        value = randint(0, 1000)

        if value == 1:
            return "축하합니다!!! 0.01%의 확률을 뚫은 불운!!!"
        elif value < 50:
            return "[대흉] 대흉과 대길은 확률이 같습니다. 힘내세요 ㅠ^ㅠ"
        elif value < 200:
            return "[중흉] 오늘은 조금 주의해야겠어요."
        elif value < 500:
            return "[흉] 이 정도면 나쁘지 않은 운이네요"
        elif value < 800:
            return "[길] 상쾌한 하루가 되겠네요!"
        elif value < 950:
            return "[중길] 0.5% 확률을 뚫은 행운아!"
        else:
            return "[대길] 축하합니다!! 로또보단 낮지만 어쨌든 엄청난 확률을 손에 쥐셨습니다!"

    def activity_result(self, activity_data, comment_list):
        image_name = ""

        # 전설 1% 초희귀 10% 희귀 30% 평범 40% 꽝 20%
        value = randint(1, 101)

        if value < 20:
            result_list = activity_data["꽝"]
            result = result_list[randint(0, len(result_list) - 1)]
            comment = comment_list[randint(0, len(comment_list) - 1)] + "\n . \n . \n . \n" + result.description + "\n[꽝]"

        elif value < 60:
            result_list = activity_data["평범"]
            result = result_list[randint(0, len(result_list) - 1)]
            comment = comment_list[randint(0, len(comment_list) - 1)] + "\n . \n . \n . \n[평범]" + result.name + "\n" + \
                        result.description + "\n\n추천 레시피: " + result.recipe

        elif value < 90:
            result_list = activity_data["희귀"]
            result = result_list[randint(0, len(result_list) - 1)]
            comment = comment_list[randint(0, len(comment_list) - 1)] + "\n . \n . \n . \n[희귀]" + result.name + "\n" + \
                        result.description + "\n\n추천 레시피: " + result.recipe

        elif value < 99:
            result_list = activity_data["초희귀"]
            result = result_list[randint(0, len(result_list) - 1)]
            comment = comment_list[randint(0, len(comment_list) - 1)] + "\n . \n . \n . \n[초희귀]" + result.name + "\n" + \
                      result.description + "\n\n추천 레시피: " + result.recipe

        else:
            result_list = activity_data["전설"]
            result = result_list[randint(0, len(result_list) - 1)]
            comment = comment_list[randint(0, len(comment_list) - 1)] + "\n . \n . \n . \n[전설]" + result.name + "\n" + \
                      result.description + "\n\n추천 레시피: " + result.recipe
            image_name = result.image

        return {"image_name": image_name, "comment": comment}