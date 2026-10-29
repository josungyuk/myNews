# myNews

뉴스 기사를 수집하고, 분야별 요약과 수집한 기사에 근거한 질문·답변을 제공하는 FastAPI 프로젝트입니다. 기사를 저장할 때 본문을 청크로 나누고 Gemini 임베딩을 생성합니다. RAG 질문에서는 PostgreSQL의 pgvector로 관련 청크를 검색한 뒤, Gemini가 검색 결과를 바탕으로 답변과 기사 출처를 반환합니다.

## 현재 구현된 기능

- 연합뉴스, YTN, BBC, The Guardian, NPR의 경제·국제 뉴스 수집 및 본문 파싱
- 키워드 기반 경제·국제 점수 계산, 기사 중복 저장 방지
- 기사 본문 청킹(기본 1,500자, 200자 중첩) 및 임베딩 저장
- 경제·국제·전체 기사 요약과 pgvector 유사도 검색 기반 RAG 질문·답변
- 기존 기사에 대한 청크·임베딩 백필 스크립트

## 기술 스택과 구조

Python, FastAPI, Selenium, BeautifulSoup, SQLAlchemy, Alembic, PostgreSQL/pgvector, Google Gemini API를 사용합니다. Neon은 PostgreSQL 호스팅 선택지이며 로컬 PostgreSQL도 사용할 수 있습니다.

```text
app/
  crawler/     뉴스 페이지 수집·파싱
  news/        기사 저장 및 점수 계산
  summary/     분야별 요약 API
  rag/         청킹·벡터 검색·질문 응답 API
  ai/embedding/ Gemini 임베딩 클라이언트
  llm/         Gemini 텍스트 생성 클라이언트
  common/      설정·DB 연결·의존성
alembic/       DB 마이그레이션
scripts/       기존 데이터 백필
tests/         unittest 기반 테스트
```

## 로컬 실행

Python 환경, Chrome 브라우저(Selenium 수집 시), `vector` 확장을 사용할 수 있는 PostgreSQL 데이터베이스, Gemini API 키가 필요합니다. 수집 및 RAG 요청은 외부 서비스 사용량이 발생할 수 있습니다.

1. 가상환경을 만들고 의존성을 설치합니다.

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

2. 프로젝트 루트에 `.env`를 만들고 실제 값을 입력합니다. 아래 값은 예시이며, 비밀번호와 API 키를 Git에 올리지 마세요.

   ```dotenv
   DATABASE_URL=postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require
   llm_api_key=YOUR_GEMINI_API_KEY
   llm_model=YOUR_GEMINI_GENERATION_MODEL
   ```

   Neon을 사용한다면 `DATABASE_URL`에 Neon 콘솔의 연결 문자열을 넣습니다. 로컬 DB를 사용한다면 `DATABASE_URL` 대신 `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`을 모두 설정할 수 있습니다. `embedding_model`은 기본값 `gemini-embedding-001`, `embedding_dimension`은 기본값 `768`입니다. 차원을 바꾸려면 DB의 `news_chunks.embedding` 벡터 차원도 일치시켜야 합니다. `llm_fallback_model`은 선택 사항으로, RAG 답변 생성 중 기본 모델이 429/503 오류를 반환할 때 사용됩니다.

3. **새 데이터베이스**에 스키마를 적용하고 서버를 실행합니다.

   ```powershell
   python -m alembic upgrade head
   python -m uvicorn app.main:app --reload
   ```

   기존 데이터베이스를 사용 중이라면 먼저 현재 Alembic 버전과 스키마를 확인하세요. 백업 없이 기존 DB의 마이그레이션 이력을 재설정하거나 새 DB용 명령을 그대로 적용하지 마세요.

4. 브라우저에서 `http://127.0.0.1:8000/docs`를 열어 API를 호출합니다. `/news`는 **POST** 요청이므로 주소창에서 GET으로 열면 405가 반환됩니다.

## API

| 메서드 | 경로 | 역할 |
| --- | --- | --- |
| POST | `/news` | 뉴스 수집, 점수 계산, 저장, 청킹 및 임베딩 |
| POST | `/summaries/economy` | 경제 뉴스 요약 |
| POST | `/summaries/world` | 국제 뉴스 요약 |
| POST | `/summaries/total` | 전체 뉴스 요약 |
| POST | `/rag/ask` | 질문과 관련된 기사 검색 후 출처가 포함된 답변 생성 |

RAG 요청 예시:

```json
{
  "question": "최근 경제 뉴스의 주요 이슈는 무엇인가요?",
  "limit": 3
}
```

`limit`은 1~5이며, 응답에는 `answer`와 기사별 `news_id`, `title`, `source`, `url`을 담은 `sources`가 포함됩니다. 검색 가능한 임베딩이 없으면 빈 `sources`와 자료를 찾지 못했다는 답변을 반환합니다. 요약 API는 저장된 기사에서 데이터를 읽어 LLM 결과를 반환하며, 현재 요약 결과 자체를 DB에 저장하지는 않습니다.

## 기존 데이터 백필

이미 저장된 기사에 청크 또는 임베딩이 없는 경우에만 아래 명령을 순서대로 실행합니다. 실제 DB를 읽고 쓰며, 임베딩 단계는 Gemini API를 호출합니다.

```powershell
python -m scripts.backfill_news_chunks
python -m scripts.backfill_news_embeddings
```

## 테스트

외부 사이트, Selenium, DB, Gemini를 호출하지 않는 단위 테스트:

```powershell
python -m unittest discover -s tests -v
```

실제 Gemini 연결 테스트는 기본적으로 건너뜁니다. API 키와 호출 비용을 확인한 뒤 실행하려면 `RUN_GEMINI_INTEGRATION=1`을 설정하세요. 단위 테스트 통과가 실제 크롤링→DB 저장→벡터 검색→답변의 종단 간 동작을 보증하지는 않습니다.

## 현재 제한 사항

- `/news`는 요청 안에서 Selenium 수집과 임베딩을 수행하므로 응답 시간이 길 수 있습니다. 현재 설정은 언론사·분야별 링크를 1개씩 처리합니다.
- 기사 페이지 구조가 바뀌거나 외부 API에 장애·할당량 제한이 생기면 일부 처리가 실패할 수 있습니다. 임베딩 생성이 실패한 청크는 벡터 없이 저장될 수 있으며, 이 경우 RAG 검색 대상에서 제외됩니다.
- 프런트엔드, 배포 자동화, 실제 인프라를 포함한 종단 간 테스트는 아직 이 저장소에 없습니다.
