import os
from dotenv import load_dotenv, find_dotenv
from notion_client import Client
from helper import async_getitem
import asyncio

_ = load_dotenv(find_dotenv())

notion = Client(auth=os.environ["NOTION_TOKEN"]) # 토근이 없으면 에러 발생

def get_streaks(memberId):
    """
    해당 멤버스페이스 id를 가지는 streak 페이지를 
    {{스트릭1 이름}: {스트릭1 id}...} 형태의 딕셔너리로 만들어 반환합니다.

    Args:
        memberId (string): 멤버스페이스 id

    Returns:
        dict: key: 페이지 이름, value: 페이지 id
    """
    streaks = notion.databases.query(
            **{
                "database_id": '40fcfbea5f514a6583db737bc7821536',
                "filter": {
                    "property": "[Season 3] 유저 멤버 스페이스",
                    "relation": {
                        "contains": memberId
                    }
        
                }
            }
        )
    streaks_list = asyncio.run(async_getitem(streaks, "results"))
    preprocessed_streaks = dict()
    for streak in streaks_list:
        preprocessed_streaks[streak["properties"]["Name"]["title"][0]["plain_text"].strip()] = streak["id"]

    return preprocessed_streaks


if __name__ == '__main__':
    get_streaks("3db94169-8c89-4def-be86-f00a29ee7443")