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

    def generate_comment(self, activity_comment: str, grade: str, monster: Monster):
        result_comment = activity_comment + "\n . \n . \n . \n" + grade + monster.name + "\n" + \
        monster.description + "\n\n추천 레시피: " + monster.recipe

        return result_comment

    def activity_result(self, activity_data, comment_list):
        image_name = ""
        activity_comment = comment_list[randint(0, len(comment_list) - 1)]

        # 전설 1% 초희귀 10% 희귀 30% 평범 40% 꽝 20%
        value = randint(1, 101)
        if value < 20:
            monster_list = activity_data["꽝"]
            result_monster = monster_list[randint(0, len(monster_list) - 1)]
            comment = self.generate_comment(activity_comment, "꽝", result_monster)

        elif value < 60:
            monster_list = activity_data["평범"]
            result_monster = monster_list[randint(0, len(monster_list) - 1)]
            comment = self.generate_comment(activity_comment, "평범", result_monster)

        elif value < 90:
            monster_list = activity_data["희귀"]
            result_monster = monster_list[randint(0, len(monster_list) - 1)]
            comment = self.generate_comment(activity_comment, "희귀", result_monster)

        elif value < 99:
            monster_list = activity_data["초희귀"]
            result_monster = monster_list[randint(0, len(monster_list) - 1)]
            comment = self.generate_comment(activity_comment, "초희귀", result_monster)

        else:
            monster_list = activity_data["전설"]
            result_monster = monster_list[randint(0, len(monster_list) - 1)]
            comment = self.generate_comment(activity_comment, "희귀", result_monster)
            image_name = result_monster.image

        return {"image_name": image_name, "comment": comment}

