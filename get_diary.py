import os
from dotenv import load_dotenv, find_dotenv
from notion_client import Client
from pprint import pprint
import asyncio
from helper import async_getitem
from get_goals import get_goals

_ = load_dotenv(find_dotenv())

notion = Client(auth=os.environ["NOTION_TOKEN"]) # 토근이 없으면 에러 발생

def get_diary(databaseId):
    """모두의 일기 데이터베이스에서 작성완료되고 아직 목표가 등록되지 않은 일기를 반환합니다.

    Args:
        databaseId (string): 모두의 일기 데이터베이스 id

    Returns:
        list: 일기 딕셔너리를 담은 리스트
    """
    diary_database = notion.databases.query(
    **{
            "database_id": databaseId,
            "filter": {
                "and": [
                    {
                        "property": "작성 완료",
                        "checkbox": {
                            "equals": True
                        }
                    },
                    {
                        "property": "운영진 확인용",
                        "checkbox": {
                            "equals": False
                        }
                    }
                ]
            }

        }
    )
    unprocessed_diarys = asyncio.run(async_getitem(diary_database, "results"))

    preprocessed_diarys = list()
    for diary in unprocessed_diarys:
        preprocess = dict()
        preprocess['id'] = diary['id']
        preprocess['memberId'] = diary['properties']['[Season 3] 유저 멤버 스페이스']['relation'][0]['id']
        preprocess['date'] = diary['properties']['날짜']
        preprocess['finishedGoals'] = get_goals(diary['id'])
        preprocess['icon'] = diary['icon']
        preprocessed_diarys.append(preprocess)

    return preprocessed_diarys

if __name__ == '__main__':
    diarys = get_diary("2ff941a72ab040d4a0604bcf4193589c")
    print(len(diarys))
    pprint(diarys)