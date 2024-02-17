import re


def extract_name(title):
    # 정규 표현식을 사용하여 'X의' 형태를 찾습니다. X는 임의의 문자열이 될 수 있습니다.
    match = re.match(r"(.+?)의", title)
    if match:
        # 매칭된 부분의 첫 번째 그룹(.+?)을 반환합니다.
        return match.group(1)
    else:
        # 매칭되는 부분이 없을 경우 None을 반환합니다.
        return "아무개"


if __name__ == "__main__":
    # 테스트 코드
    titles = ["이혁의 1D1S", "박준서의 일기", "김민지의 여행", "조수미의 노래"]

    for title in titles:
        print(extract_name(title))
