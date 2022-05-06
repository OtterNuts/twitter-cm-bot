# twitter-cm-bot

## installation

본 프로젝트는 poetry 로 라이브러리 의존성 관리를 하고 있습니다. 다음의 command를 입력 후 사용해주시기 바랍니다.

```
> curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
> poetry install
```

## authentification

트위터와 구글 스프레드 시트 api를 사용하고 있습니다.

### 트위터 인증
src/auth/twitter.py

```
self.consumer_key = "여기에"
self.consumer_secret = "키와 시크릿,"
self.access_token = "토큰과 시크릿을"
self.access_token_secret = "입력하세요"

```

### 구글 인증
auth 폴더에 구글드라이브의 인증 json 파일을 넣은 후 아래 코드에 경로를 입력하세요.
src/auth/google_drive.py

```
self.keyfile = "src/auth" + "json 파일명"
```

## 키워드 등록 및 새로운 기능 추가
src/main
```
activity_list = ["오늘의운세", "[사냥]", "[요리]", "[낚시]", "[장비뽑기]", "[로또뽑기]", "[일괄판매]"]

```
에 새로운 키워드를 추가한 후 src/tweetBot/generate_reply 함수의 아래 부분에 elif 구문으로 기능을 추가해서 사용하세요

```
        elif task_name == "[일괄판매]":
            print("일괄판매 시작")
            num_c_equip = sheet_data["플레이어"][user_id].C급장비개수
            num_b_equip = sheet_data["플레이어"][user_id].B급장비개수
            if int(num_b_equip) + int(num_c_equip) == 0:
                reply_comment = "장비가 없습니다. 인벤토리를 확인해주세요."
            else:
                sell_total = 5000 * int(num_b_equip) + 1000 * int(num_c_equip)
                sheet_data["플레이어"][user_id].골드 += sell_total
                sheet_data["플레이어"][user_id].C급장비개수 = 0
                sheet_data["플레이어"][user_id].B급장비개수 = 0
                self.google_api.update_user_data("플레이어", "test", sheet_data["플레이어"])
                reply_comment = "@%s" % user_id + f"[장비판매]\nB급장비개수: {num_b_equip}\nC급장비개수: {num_c_equip}\n총가격: {str(sell_total)}"

        ##### 새로운 기능을 추가하길 바랄 경우 여기에 elif 구문으로 코드를 추가하세요 #####

        else:
            reply_comment = "@%s" % user_id + "봇 오류입니다. 캡쳐와 함께 총괄계에 문의 부탁드립니다."

        return [{"reply_image": reply_image, "reply_comment": reply_comment}]
```

결과값은 reply_comment에 할당하고, 이미지를 추가하고 싶을 경우 reply_image에 이미지파일명을 확장자와 함께 기입하세요.

```
reply_comment = "@%s" % user_id + "봇이 명령어를 읽었습니다."
reply_image = "photo.png"
```

## 구글 스프레드 시트 관리
예시용 구글 스프레드 시트: https://docs.google.com/spreadsheets/d/15HMKanZCVymE3XsnkhjgYZ_ddQTmfZRTrclwD3S9Cts/edit#gid=1956526250

사용할 시트에 구글 api 계정을 추가한 후 src/dataProcessors/from_google_spread_sheet.py 최상단 상수 SHEET_NAME에 sheet이름을 추가하세요
예시)

```
SHEET_NAME = "bot-data-example"

```

새로운 데이터 시트를 추가 후 불러올 경우 src/dataProcessors/from_google_spread_sheet.py/DataProcessingService 에 아래의 형식을 지켜 새로운 데이터 시트를 추가하세요.

```
example_raw_data = google_api.get_all_data_from_sheet(SHEET_NAME, "시트이름")
```
시트 데이터에 맞춰 src/dataProcessors/models/items에 dataclass를 추가하고 데이터를 가공할 함수를 생성하세요.
raw_data를 가공하여 sheet_data에 넘기세요.


## 외부 참고 링크
https://velog.io/@otternut
