# 1d1s_notion_automation

## 실행 방법

```
git clone https://github.com/Pjunn/1d1s_notion_automation.git
cd 1d1s_notion_automation
echo "NOTION_TOKEN='{your-notion-token}'
DIARY_DATABASE='2ff941a72ab040d4a0604bcf4193589c'
HABIT_DATABASE='5fa151cdd7bd4572ae0e9d9315037b94'" >> .env
```

미니콘다 설치 해주세요. 설치 한 다음 아래 명령어로 콘다 가상환경을 생성, 실행해주세요.
```
conda env create -f auto_py310.yaml
conda activate auto_py310
```

아래의 명령어로 프로그램을 실행합니다.
```
python main.py
```