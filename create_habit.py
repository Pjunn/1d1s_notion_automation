import os
from dotenv import load_dotenv, find_dotenv
from notion_client import Client
from pprint import pprint
import logging
from get_streaks import get_streaks
from get_name import get_name
_ = load_dotenv(find_dotenv())

notion = Client(auth=os.environ["NOTION_TOKEN"]) # 토근이 없으면 에러 발생

def create_habit(databaseId, diary):
    """Habit Tracker 데이터베이스에 페이지를 추가합니다.

    Args:
        databaseId (string): Habit Tracker 데이터베이스 id
        diary (dict): 일기

    Returns:
        list: 추가된 habit 페이지 리스트
        boolean: 해당 일기에서 완료된 모든 목표가 Habit Tracker에 추가되었을때 True, 아니라면 False
    """
    streaks = get_streaks(diary["memberId"])

    name = get_name(diary["memberId"])
    logging.info(f"{name}의 해결 목표 개수: {len(diary['finishedGoals'])} ")

    success = False

    habits = list()
    diary_icon = get_icon(diary)

    for goal in diary["finishedGoals"]:
        try:
            streakId = streaks[goal]
        except KeyError:
            logging.info(f"목표: {goal} is not registerd")
            continue

        habit = notion.pages.create(
            **{
                "icon": diary_icon,
                "parent": {
                "type": "database_id",
                "database_id": databaseId
                }, 
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": goal + ' - ' + name
                                }
                            }
                        ]
                    },
                    "Date": {
                        "date": diary["date"]["date"]
                    },
                    "[Season 3] 유저 멤버 스페이스": {
                        "relation": [
                            {
                                "id": diary["memberId"]
                            }
                        ]
                    },
                    "[Season 3] Streaks": {
                        "relation": [
                            {
                                "id": streakId
                            }
                        ]
                    },
                    "완료": {
                        "checkbox": True
                    }

                }
            }
        )
        habits.append(habit)
        logging.info(f"목표: {goal} is successfully posted")
    
    if len(habits) == len(diary["finishedGoals"]):
        success = True

    return habits, success

def get_icon(diary):
    """일기의 아이콘을 반환합니다.\n
    현재 노션 api에서 file 타입을 icon에 사용하는 것이 지원되지 않고 
    external로 url만 넣어주면 아예 하얗게 깨져서 나옵니다.\n
    icon을 이미지로 설정한 경우 '🔥'을 기본 icon으로 사용했습니다.\n
    Args:
        diary (dict): 일기

    Returns:
        dict: icon
    """
    if diary["icon"]["type"] == 'emoji':
        icon = {"type": diary["icon"]["type"], "emoji": diary["icon"]["emoji"]}
    elif diary["icon"]["type"] == 'file':
        # icon = {"type": diary["icon"]["type"], "file": {"url": diary["icon"]["file"]["url"], "expiry_time": diary["icon"]["file"]["expiry_time"]}}
        icon = {"type": "emoji", "emoji":'🔥'}
    elif diary["icon"]["type"] == "external":
        icon = {"type": diary["icon"]["type"], "external": {"url": diary["icon"]["external"]["url"]}}
    
    return icon

def update_diary(diary):
    """운영진 확인용 체크박스에 체크합니다.

    Args:
        diary (dict): 일기

    Returns:
        dict: 업데이트된 일기
    """
    update = notion.pages.update(
        **{
            "page_id": diary["id"],
            "properties": {
                "운영진 확인용": {
                    "checkbox": True
                }
            }
        }
    )
    return update


if __name__ == '__main__':
    diary = {'date': {'date': {'end': None, 'start': '2024-02-16', 'time_zone': None},
            'id': 'ZC%5Cv',
            'type': 'date'},
    'finishedGoals': ['1일 1BOJ', '1일 1 코드 카피', '프로젝트 개발'],
    'icon': {'file': {'expiry_time': '2024-02-17T07:58:07.259Z',
                        'url': 'https://prod-files-secure.s3.us-west-2.amazonaws.com/ad32e87f-391b-4ce3-ba36-b0877643695d/ba7330f7-9b17-442e-b04b-75d23bca5330/rabbit_profile.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45HZZMZUHI%2F20240217%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20240217T065807Z&X-Amz-Expires=3600&X-Amz-Signature=4286496df6b5229ef03ef1ca0691fc166ed1fd9e1412f6f39d30565bc0ac8994&X-Amz-SignedHeaders=host&x-id=GetObject'},
            'type': 'file'},
    'id': '1cf7c65f-555c-4868-9f06-7b7d3b65923b',
    'memberId': '4704411a-c7c6-463a-b693-a7576a53302e'}

    habits = create_habit("5fa151cdd7bd4572ae0e9d9315037b94", diary)
    _ = update_diary(diary)
    pprint(habits)