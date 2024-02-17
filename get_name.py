import os
from dotenv import load_dotenv, find_dotenv
from notion_client import Client
import asyncio
from helper import async_getitem
from extract_name import extract_name

_ = load_dotenv(find_dotenv())

notion = Client(auth=os.environ["NOTION_TOKEN"]) # 토근이 없으면 에러 발생

def get_name(memberId):
    """
    해당 멤버스페이스 id를 가지는 멤버의 이름을 반환합니다.

    Args:
        memberId (string): 멤버스페이스 id

    Returns:
        string: 멤버 이름
    """
    page = notion.pages.retrieve(
        **{
            "page_id": memberId
        }
    )
    page_properties = asyncio.run(async_getitem(page, "properties"))

    title = page_properties["이름"]["title"][0]["plain_text"]
    name = extract_name(title)
    return name

if __name__ == '__main__':
    name = get_name('4704411a-c7c6-463a-b693-a7576a53302e')
    print(name)


