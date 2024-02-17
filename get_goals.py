import os
from dotenv import load_dotenv, find_dotenv
from notion_client import Client
import asyncio
from helper import async_getitem

_ = load_dotenv(find_dotenv())

notion = Client(auth=os.environ["NOTION_TOKEN"]) # 토근이 없으면 에러 발생

def get_goals(blockId):
    """일기 페이지에서 체크박스에 체크한 목표의 이름을 담은 리스트를 반환합니다.

    Args:
        blockId (string): 일기 페이지 id

    Returns:
        list: 완수한 목표의 이름 리스트
    """
    diary_blocks = notion.blocks.children.list(
        **{
            "block_id": blockId,
            "page_size": 20,
        }
    )
    blocks = asyncio.run(async_getitem(diary_blocks, "results"))

    column_list_check = 0
    finished_goals = list()
    for block in blocks:
        if column_list_check == 2:
            break
        if block['type'] == 'column_list':
            column_list_check += 1
        elif block['type'] == 'to_do' and block['to_do']['checked'] == True:
            finished_goals.append(block['to_do']['rich_text'][0]['plain_text'].strip())

    return finished_goals

if __name__ == '__main__':
    goals = get_goals("2ccc700332974a05a3572bbab0d20d1a")
    print(goals)
