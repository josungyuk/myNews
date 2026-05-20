MyNews

MyNews는 여러 뉴스 사이트의 기사를 크롤링하고 기사 내용을 분석하여 키워드 기반 점수를 계산하는 뉴스 백엔드 프로젝트입니다.
수집된 뉴스는 경제/국제 관련 키워드를 기준으로 점수화되며 향후 LLM을 활용한 뉴스 요약 기능까지 확장할 수 있도록 구성되어 있습니다.

주요 기능

1. 뉴스 기사 크롤링
   - Selenium과 requests를 사용하여 뉴스 페이지를 수집합니다.
   - 기사 제목, 본문, 작성일, URL 등의 정보를 추출합니다.

2. 뉴스 데이터 파싱
   - BeautifulSoup을 이용해 HTML에서 기사 정보를 파싱합니다.
   - 언론사별 태그 설정을 기반으로 필요한 콘텐츠만 추출합니다.

3. 키워드 기반 점수 계산
   - 경제, 국제 뉴스 관련 키워드를 기준으로 기사 점수를 계산합니다.
   - 제목에 포함된 키워드는 본문보다 더 높은 가중치를 가집니다.

4. 데이터베이스 저장
   - SQLAlchemy를 사용하여 뉴스 데이터를 DB에 저장합니다.
   - 중복된 뉴스는 저장하지 않도록 처리합니다.

5. API 제공
   - FastAPI 기반으로 백엔드 서버를 구성했습니다.
   - /news 엔드포인트를 통해 최신 뉴스 크롤링 결과를 확인할 수 있습니다.

기술 스택

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Selenium
- BeautifulSoup
- requests
- Alembic

프로젝트 구조

myNews/
├── app/
│   ├── common/        # 공통 설정, DB 연결, 환경 설정
│   ├── controller/    # API 라우터
│   ├── crawler/       # 크롤링 및 파싱 로직
│   ├── domain/        # 뉴스 엔티티 및 ORM 모델
│   ├── repository/    # DB 저장소 로직
│   ├── service/       # 비즈니스 로직
│   └── main.py        # FastAPI 앱 실행 파일
├── alembic/           # DB 마이그레이션 설정
├── requirements.txt   # Python 패키지 목록
└── alembic.ini

실행 방법

1. 저장소 클론

git clone https://github.com/josungyuk/myNews.git
cd myNews

2. 가상환경 생성 및 실행

python -m venv venv

Windows:
venv\Scripts\activate

macOS/Linux:
source venv/bin/activate

3. 패키지 설치

pip install -r requirements.txt

4. 환경 변수 설정

프로젝트 루트에 .env 파일을 생성하고 아래 값을 설정합니다.

DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name

5. 서버 실행

uvicorn app.main:app --reload

6. API 확인

브라우저 또는 API 테스트 도구에서 아래 주소로 접속합니다.

http://localhost:8000/news

개발 목적

이 프로젝트는 뉴스 기사 데이터를 자동으로 수집하고, 키워드 기반으로 중요도를 분석하는 백엔드 시스템을 구현하기 위해 만들어졌습니다.
추후 뉴스 요약, 추천, 분류 기능 등을 추가하여 개인 맞춤형 뉴스 서비스로 확장할 수 있습니다.
