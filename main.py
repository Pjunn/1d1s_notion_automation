import os
from dotenv import load_dotenv, find_dotenv
import logging
from get_diary import get_diary
from create_habit import create_habit, update_diary


def main():
    """
    확인이 필요한 모든 일기를 불러오고
    일기를 순회하며 Habit Tracker 데이터베이스에 페이지를 추가합니다.
    해당 일기의 모든 목표가 추가되었다면 '운영진 확인용' 체크박스에 체크합니다.
    """
    _ = load_dotenv(find_dotenv())

    # 로그 세팅
    logging.basicConfig(filename="1d1s_automation.log", level=logging.INFO)

    # 일기 불러오기
    diarys = get_diary(os.environ["DIARY_DATABASE"])
    logging.info(f"확인이 필요한 일기: {len(diarys)}개")

    # 일기를 순회하며 목표 수행 업데이트
    for diary in diarys:
        _, success = create_habit(os.environ["HABIT_DATABASE"], diary)
        if success:
            logging.info("목표 수행 업데이트 완료!")
            _ = update_diary(diary)
        else:
            logging.warning("등록되지 않은 목표가 있습니다. 확인해주세요.")


if __name__ == "__main__":
    main()
