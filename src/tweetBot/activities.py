from random import randint
from collections import defaultdict

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

    def cooking(self, cooking_data, comment_list):
        value = randint(0, len(cooking_data) - 1)
        dish = cooking_data[value]
        result_comment = comment_list[randint(0, len(comment_list) - 1)]
        return f'[{dish["음식명"]}]\n들어간 재료: {dish["들어간_재료"]}\n{dish["음식_설명"]}\n\n한줄평: {result_comment}'

    def generate_comment(self, activity_comment: str, monster):
        result_comment = f'{activity_comment}\n . \n . \n . \n [{monster["등급"]}]{monster["이름"]}\n{monster["아이템_설명"]}\n\n'
        if monster["추천_레시피"]:
            result_comment += f'추천 레시피: {monster["추천_레시피"]}'

        return result_comment

    def activity_result(self, activity_data, comment_list):
        activity_comment = comment_list[randint(0, len(comment_list) - 1)]

        # 전설 1% 초희귀 10% 희귀 30% 평범 40% 꽝 20%
        value = randint(1, 101)
        if value < 20:
            monster_list = activity_data["꽝"]
        elif value < 60:
            monster_list = activity_data["평범"]
        elif value < 90:
            monster_list = activity_data["희귀"]
        elif value < 99:
            monster_list = activity_data["초희귀"]
        else:
            monster_list = activity_data["전설"]

        result_monster = monster_list[randint(0, len(monster_list) - 1)]
        comment = self.generate_comment(activity_comment, result_monster)
        image_name = result_monster["이미지"]

        return {"image_name": image_name, "comment": comment}

    def gotcha_result(self, equipment_data):
        image_name = "normal.png"
        result = defaultdict(list)

        for i in range(0, 10):
            value = randint(1, 100)
            if value == 100:
                equip_grade = "S급"
                equipment_list = equipment_data[equip_grade]
                image_name = "special.png"
            elif value > 89:
                equip_grade = "A급"
                equipment_list = equipment_data[equip_grade]
                image_name = "special.png"
            elif value > 53:
                equip_grade = "B급"
                equipment_list = equipment_data[equip_grade]
            else:
                equip_grade = "C급"
                equipment_list = equipment_data[equip_grade]

            equipment = equipment_list[randint(0, len(equipment_list) - 1)]
            result[equip_grade].append(equipment)

        return {"image_name": image_name, "equip_list": result}

