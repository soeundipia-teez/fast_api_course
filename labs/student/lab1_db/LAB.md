# LAB 1 · DB 연결과 메모 CRUD (50분)

SQLAlchemy 로 메모를 DB 에 저장하고, 생성·조회·수정·삭제 API 를 만듭니다.

## 학습 목표
- 모델(테이블)과 스키마(요청/응답 모양)를 구분해서 정의한다
- `Depends(get_db)` 로 요청마다 DB 세션을 열고 닫는다
- CRUD 를 HTTP 메서드(POST/GET/PUT/DELETE)에 대응시킨다

## 실습 단계
| STEP | 파일 | 할 일 |
|---|---|---|
| STEP 1 | main.py | `Memo` 모델에 title·content 컬럼 |
| STEP 2 | main.py | `MemoCreate`·`MemoUpdate` 스키마 |
| STEP 3 | main.py | `get_db()` 세션 의존성 |
| STEP 4 | main.py | `POST /memos/` 생성 |
| STEP 5 | main.py | `GET /memos/` 목록 |
| STEP 6 | main.py | `PUT /memos/{id}` 수정 (없으면 404) |
| STEP 7 | main.py | `DELETE /memos/{id}` 삭제 (없으면 404) |

## 실행
```bash
cd labs/student/lab1_db
uvicorn main:app --reload
# /docs 에서 POST → GET → PUT → DELETE 순서로 Try it out
python check_lab.py
```

## 확인
- [ ] MySQL 에서 `USE my_memo_app; SHOW TABLES;` 에 memo 테이블이 보인다
- [ ] `/docs` 에서 만든 메모가 GET 목록에 나온다
- [ ] 없는 id 를 수정·삭제하면 404
- [ ] `python check_lab.py` 7 / 7 통과

## 자주 나는 오류
| 증상 | 원인 · 해결 |
|---|---|
| `Can't connect to MySQL server on 'localhost'` | MySQL 서버가 꺼져 있습니다. Windows: 서비스(services.msc)에서 MySQL80 시작 |
| `cryptography package is required for sha256_password or caching_sha2_password` | MySQL 8 기본 인증 방식 때문입니다. `pip install cryptography` (requirements 에 포함) |
| POST 가 422 | 요청 본문에 title·content 둘 다 있어야 합니다. 응답 detail 에 빠진 필드가 나옵니다 |
| `ResponseValidationError` | `MemoOut` 의 필드와 모델 컬럼 이름이 다르거나 `from_attributes=True` 가 없습니다 |
| `Access denied for user 'hyundai'` / `Unknown database 'my_memo_app'` | `setup_mysql.sql` 을 root 로 먼저 실행해 DB 와 계정을 만듭니다 |

## 도전 과제
- `GET /memos/{id}` 단건 조회 추가 (없으면 404)
- `GET /memos/?q=회의` 제목 검색 (`Memo.title.contains(q)`)
- MySQL Workbench 나 `mysql` 클라이언트에서 `SELECT * FROM memo;` 로 실제 행 확인

> DB 는 MySQL `my_memo_app` (계정 hyundai). 처음이면 프로젝트 루트의 `setup_mysql.sql` 을 먼저 실행하세요. 테이블을 처음부터 다시 만들려면 `python reset_db.py`.

> 개념 설명과 도식은 `lesson_plan/` 의 HTML 교안을 함께 보세요.

## 복습 과제 (기초 · 기본 · 심화)

이 LAB 을 마친 프로젝트에 이어서 작성합니다. 자세한 설명과 힌트는 교안의 **과제** 메뉴를 보세요.

### 1. [기초] 메모 현황판 API

> 운영팀이 '지금 메모가 몇 개 있고, 가장 최근에 뭐가 들어왔는지' 대시보드에 띄우고 싶어 합니다.

- `GET /memos/summary`
- 응답: `{"count": 전체 개수, "latest": 가장 최근 메모 | null}`
- 메모가 하나도 없으면 `latest` 는 `null`

```bash
curl http://127.0.0.1:8000/memos/summary
# {"count":2,"latest":{"id":2,"title":"회의","content":"3시 B동"}}
```

### 2. [기본] 검색과 페이지 나누기

> 메모가 수백 개가 되자 목록이 너무 길어졌습니다. 키워드로 찾고, 10개씩 나눠 보는 기능이 필요합니다.

- `GET /memos/search?q=키워드&page=1&size=10`
- 제목 **또는** 내용에 q 가 들어간 메모, 최신순
- 응답: `{"total", "page", "size", "items": [...]}`
- page ≥ 1, 1 ≤ size ≤ 50 (벗어나면 422)

```bash
curl "http://127.0.0.1:8000/memos/search?q=회의&page=1&size=5"
curl "http://127.0.0.1:8000/memos/search?size=100"   # 422
```

### 3. [심화] 메모 일괄 등록 (전부 또는 전무)

> 다른 시스템에서 옮겨 온 메모를 한 번에 등록해야 합니다. 중간에 하나라도 잘못되면 **하나도 저장되면 안 됩니다**.

- `POST /memos/bulk`, body 는 `[{title, content}, ...]` 배열
- 1~20개만 허용, 아니면 400
- 제목이 공백뿐인 항목이 하나라도 있으면 400 + 아무것도 저장하지 않음
- 성공 시 생성된 메모 목록(id 포함) 반환

```bash
curl -X POST http://127.0.0.1:8000/memos/bulk -H "Content-Type: application/json" \
     -d '[{"title":"a","content":"1"},{"title":"  ","content":"2"}]'
# 400 {"detail":"제목이 비어 있는 항목 번호: [1]"}  → GET /memos/ 개수 변화 없음
```
