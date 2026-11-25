# FastAPI로 만드는 마이 메모 앱

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.162-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)
![LAB](https://img.shields.io/badge/LAB-6%20steps-1f5fbf)

![실행 과정 미리보기: MySQL 준비부터 완성 앱까지](docs/demo.gif)

MySQL 준비 → 자동 점검 → 테이블 재생성 → 서버 실행 → API 호출 → DB 확인 → 완성 화면 (각 단계 이미지는 바로 아래)

## 실행 결과 화면

이 프로젝트를 실제로 실행해서 얻은 결과입니다. 처음 셋팅부터 LAB 5 완성 앱까지 순서대로 진행했습니다.

### ① MySQL 준비 — `setup_mysql.sql`

수업용 `my_memo_app` 과 점검용 `my_memo_app_test` 가 만들어집니다.

![setup_mysql.sql 실행 결과](docs/screens/01_setup_mysql.png)

### ② 자동 점검 — 처음 받았을 때

학생용 파일을 받은 직후에는 모든 STEP 이 `FAIL` 이고, 무엇을 채워야 하는지(`미완성: STEP 3 ...`) 알려 줍니다.

![check_lab.py 처음 실행](docs/screens/02_check_start.png)

### ③ 자동 점검 — 완성했을 때

TODO 를 모두 채우면 STEP 별로 `PASS` 가 나옵니다. (LAB 1, LAB 5 예시)

![check_lab.py 완성 후](docs/screens/03_check_done.png)

### ④ LAB 3 테이블 재생성 — `reset_db.py`

LAB 1~2 의 `memo` 테이블을 지우고 `user_id` 가 있는 새 구조로 다시 만듭니다.

![reset_db.py 실행 결과](docs/screens/04_reset_db.png)

### ⑤ 서버 실행 — `uvicorn main:app --reload`

요청이 들어올 때마다 메서드, 경로, 상태 코드가 로그로 찍힙니다. 중복 가입 400, 로그인 실패 401, 비로그인 접근 303 이 그대로 보입니다.

![uvicorn 실행 로그](docs/screens/05_uvicorn.png)

### ⑥ API 직접 호출 — `curl`

회원가입 → 중복 가입(400) → 로그인 실패(401) → 로그인(세션 쿠키 저장) → 메모 생성 3건 → 수정 → 비로그인 접근(303) 순서입니다. 같은 요청을 `http://127.0.0.1:8000/docs` 에서도 해 볼 수 있습니다.

![curl 로 API 호출](docs/screens/06_api_curl.png)

### ⑦ DB 확인 — `mysql`

테이블 구조와 저장된 데이터입니다. 비밀번호는 `$2b$12$...` bcrypt 해시로만 저장되고, 메모마다 작성자 `user_id` 가 들어 있습니다.

![MySQL 에서 테이블과 데이터 확인](docs/screens/07_mysql.png)

### ⑧ 브라우저 — 홈 (로그인 · 회원가입)

![홈 화면](docs/screens/08_browser_home.png)

### ⑨ 브라우저 — 내 메모 (LAB 5 완성 화면)

로그인한 사용자 이름이 헤더에 표시되고, 위에서 만든 메모 3건이 카드로 나옵니다. 수정(연필)·삭제(휴지통) 버튼은 `fetch` 로 API 를 호출합니다.

![내 메모 화면](docs/screens/09_browser_memos.png)

---

## 소개

빈 FastAPI 서버에서 시작해 **DB 저장 → 회원가입·로그인 → 사용자별 메모 → 웹 화면 → 예외 처리**까지, 하나의 메모 앱을 LAB 6단계로 키워 가는 실습 프로젝트입니다. 각 LAB 폴더는 그 단계에서 실행되는 완전한 앱이고, 새로 배우는 부분만 `TODO` 로 비어 있습니다.

---

## 목차

1. [실행 결과 화면](#실행-결과-화면)
2. [프로젝트 구조](#프로젝트-구조)
3. [LAB 요약](#lab-요약)
4. [초기 셋팅](#초기-셋팅)
5. [데이터베이스 스키마](#데이터베이스-스키마)
6. [실행과 점검](#실행과-점검)
7. [최종 API 목록](#최종-api-목록)
8. [문제 해결](#문제-해결)

---

## 프로젝트 구조

```
fastapi_memo_course/
├─ README.md
├─ requirements.txt                  # 파이썬 패키지 (pip install -r)
├─ setup_mysql.sql                   # DB · 계정 생성 (처음 한 번)
├─ docs/                             # README 이미지 (스키마 도식)
├─ lesson_plan/
│  └─ fastapi_lesson_student.html    # 수업교안: 개념 · 도식 · 단계 · 확인 (브라우저로 열기)
└─ labs/student/
   ├─ lab0_start/                    # LAB 0  FastAPI 시작
   │  ├─ main.py
   │  ├─ templates/home.html
   │  ├─ LAB.md                      # 실습 시트
   │  └─ check_lab.py                # 자동 점검
   ├─ lab1_db/                       # LAB 1  DB 연결과 메모 CRUD
   │  ├─ main.py · templates/home.html
   │  └─ LAB.md · check_lab.py · reset_db.py
   ├─ lab2_login/                    # LAB 2  회원가입 · 로그인 · 세션
   │  ├─ main.py · templates/home.html
   │  └─ LAB.md · check_lab.py · reset_db.py
   ├─ lab3_memo/                     # LAB 3  내 메모만 보기
   │  ├─ main.py · templates/home.html · templates/memos.html
   │  └─ LAB.md · check_lab.py · reset_db.py
   ├─ lab4_ui/                       # LAB 4  화면 붙이기 (fetch)
   │  ├─ main.py · templates/home.html · templates/memos.html
   │  └─ LAB.md · check_lab.py · reset_db.py
   └─ lab5_final/                    # LAB 5  예외 처리와 마무리
      ├─ main.py · templates/home.html · templates/memos.html
      └─ LAB.md · check_lab.py · reset_db.py
```

| 파일               | 역할                                                                                                |
| ------------------ | --------------------------------------------------------------------------------------------------- |
| `main.py`          | FastAPI 앱. 각 함수 설명에 **STEP 번호 · 순서 · 힌트 코드**가 있고, `# ===== TODO` 아래를 채웁니다  |
| `templates/*.html` | Jinja2 화면. LAB 3~5 는 HTML·JavaScript 에도 TODO 가 있습니다 (`{# ===== TODO #}`, `// ===== TODO`) |
| `LAB.md`           | 그 LAB 의 목표 · 단계 · 실행 명령 · 확인 목록 · 자주 나는 오류 · 도전 과제                          |
| `check_lab.py`     | STEP 별 PASS / FAIL 자동 점검 (점검 전용 DB 사용)                                                   |
| `reset_db.py`      | 수업용 DB 의 테이블을 지우고 그 LAB 구조로 다시 생성                                                |

---

## LAB 요약

| LAB | 주제                     | 핵심 개념                                            | 새로 만드는 것                                     |
| :-: | ------------------------ | ---------------------------------------------------- | -------------------------------------------------- |
|  0  | FastAPI 시작             | 라우팅, JSON 응답, Jinja2 템플릿, 경로·쿼리 매개변수 | `GET /`, `/about`, `/hello/{name}`                 |
|  1  | DB 연결과 메모 CRUD      | SQLAlchemy 모델, Pydantic 스키마, `Depends(get_db)`  | `memo` 테이블, `/memos/` CRUD                      |
|  2  | 회원가입 · 로그인 · 세션 | bcrypt 해시, `SessionMiddleware`, 401                | `users` 테이블, `/signup` `/login` `/logout` `/me` |
|  3  | 내 메모만 보기           | ForeignKey, relationship, 인증 의존성, 소유자 필터   | `memo.user_id`, 내 메모 목록 페이지                |
|  4  | 화면 붙이기              | 서버 렌더링 + JavaScript `fetch`                     | 로그인·회원가입 폼, 메모 관리 화면                 |
|  5  | 예외 처리와 마무리       | 400 / rollback / 500, 303 Redirect, 상태 코드 분기   | 중복 가입 차단, 친절한 오류 메시지                 |

> LAB 1 ~ 5 에는 각각 **복습 과제 3개(기초 · 기본 · 심화)** 가 있습니다. 교안의 각 LAB 마지막 세부 메뉴 **과제** 와 LAB 폴더의 `LAB.md` 에서 볼 수 있습니다.

| LAB | 기초                     | 기본                 | 심화                            |
| :-: | ------------------------ | -------------------- | ------------------------------- |
|  1  | 메모 현황판 API          | 검색과 페이지 나누기 | 메모 일괄 등록 (전부 또는 전무) |
|  2  | 비밀번호 정책 검사       | 비밀번호 변경        | 로그인 실패 잠금                |
|  3  | 내 메모 요약             | 메모 고정(핀)        | 회원 탈퇴                       |
|  4  | 메모 개수와 빈 목록 안내 | 실시간 검색창        | 새로고침 없이 추가 · 삭제       |
|  5  | 이메일 형식 검증         | DB 장애 공통 처리    | 공통 요청 함수와 입력 길이 검증 |

### LAB 0 · FastAPI 시작

첫 웹 서버를 띄우고 URL 과 파이썬 함수를 연결합니다. dict 를 돌려주면 JSON 이, `TemplateResponse` 를 돌려주면 HTML 이 내려갑니다. `/hello/{name}?age=20` 으로 경로·쿼리 매개변수와 타입 검증(잘못된 값은 422)을 확인합니다.

| STEP | 할 일                                          |
| ---- | ---------------------------------------------- |
| 1    | `GET /about` → JSON 메시지                     |
| 2    | `GET /` → `home.html` 렌더링 (`app_name` 전달) |
| 3    | `GET /hello/{name}?age=` → 인사말 + 나이       |

### LAB 1 · DB 연결과 메모 CRUD

MySQL `my_memo_app` 에 접속해 `memo` 테이블을 만들고, 생성·조회·수정·삭제 API 를 만듭니다. **모델**(DB 테이블)과 **스키마**(HTTP JSON 모양)를 구분하고, 요청마다 DB 세션을 열고 닫는 `get_db` 의존성을 씁니다.

| STEP | 할 일                                                              |
| ---- | ------------------------------------------------------------------ |
| 1    | `Memo` 모델 (id, title, content)                                   |
| 2    | `MemoCreate` · `MemoUpdate` 스키마                                 |
| 3    | `get_db()` 세션 의존성                                             |
| 4~7  | `POST` 생성 · `GET` 목록 · `PUT` 수정 · `DELETE` 삭제 (없으면 404) |

### LAB 2 · 회원가입 · 로그인 · 세션

비밀번호는 bcrypt **해시**로만 저장하고, 로그인에 성공하면 `request.session` 에 사용자 이름을 기록합니다. 브라우저는 서명된 세션 쿠키를 받아 다음 요청부터 자동으로 보냅니다.

| STEP | 할 일                                               |
| ---- | --------------------------------------------------- |
| 1    | `SessionMiddleware` 등록                            |
| 2    | `get_password_hash` · `verify_password`             |
| 3    | `User` 모델, `UserCreate` · `UserLogin` 스키마      |
| 4~7  | `/signup` · `/login` (실패 401) · `/logout` · `/me` |

### LAB 3 · 내 메모만 보기

`memo` 에 `user_id` 외래 키를 추가해 작성자를 저장합니다. 로그인 확인을 `get_current_user` 의존성 하나로 묶고, 조회·수정·삭제는 항상 `user_id == 나` 조건을 겁니다. 남의 메모는 404 입니다. 목록은 `memos.html` 로 그립니다.

> 테이블 구조가 바뀌므로 이 LAB 폴더에서 **`python reset_db.py` 를 먼저 한 번** 실행합니다.

| STEP | 할 일                                             |
| ---- | ------------------------------------------------- |
| 1    | `Memo.user_id` ForeignKey, NOT NULL, relationship |
| 2    | `get_current_user()` (401 / 404)                  |
| 3    | 생성 시 `user_id` 저장                            |
| 4    | 내 메모만 조회 → `memos.html` (Jinja2 for 문)     |
| 5    | 수정·삭제에 소유자 조건                           |

### LAB 4 · 화면 붙이기

처음 화면은 서버가 Jinja2 로 그리고, 추가·수정·삭제·로그인은 JavaScript `fetch` 로 LAB 1~3 의 JSON API 를 호출합니다. 헤더에 로그인한 사용자 이름을 표시합니다.

| STEP | 할 일                                              |
| ---- | -------------------------------------------------- |
| 1    | `memos.html` 에 `username` 전달 (main.py)          |
| 2~3  | `home.html` 로그인 · 회원가입 `fetch`              |
| 4~7  | `memos.html` 추가 · 수정 · 삭제 · 로그아웃 `fetch` |

### LAB 5 · 예외 처리와 마무리

실패도 정해진 모양(`{"detail": "..."}` + 상태 코드)으로 알리고, 화면은 `response.status` 로 성공·실패를 나눠 처리합니다.

| STEP | 할 일                                               |
| ---- | --------------------------------------------------- |
| 1    | 중복 username → 400                                 |
| 2    | `commit` 실패 시 `rollback` + 500                   |
| 3    | 로그인 실패 메시지 "로그인을 실패했습니다."         |
| 4    | 비로그인 `GET /memos/` → 303 홈으로 이동            |
| 5~6  | 로그인 · 회원가입 응답 상태 코드 분기, 성공 시 이동 |

---

## 초기 셋팅

![초기 셋팅: setup_mysql.sql 이 만드는 것](docs/db_setup.png)

### 1. MySQL 준비 (처음 한 번)

MySQL 8 서버를 설치하고 실행한 뒤 (Windows: 서비스 `MySQL80`, macOS: `brew services start mysql`), root 계정으로 `setup_mysql.sql` 을 실행합니다.

```bash
mysql -u root -p < setup_mysql.sql
# 또는 MySQL Workbench 에서 setup_mysql.sql 을 열고 전체 실행
```

| 만들어지는 것                             | 용도                                                                   |
| ----------------------------------------- | ---------------------------------------------------------------------- |
| DB `my_memo_app`                          | 수업용. `uvicorn` 으로 앱을 실행할 때 사용                             |
| DB `my_memo_app_test`                     | `check_lab.py` 자동 점검 전용. 점검할 때마다 테이블을 지우고 다시 만듦 |
| 계정 `hyundai` / `hyundai` (`@localhost`) | 두 DB 에 모든 권한                                                     |

두 DB 모두 `utf8mb4` / `utf8mb4_unicode_ci` 로 만들어 한글과 이모지를 저장할 수 있습니다.

### 2. 파이썬 환경

```bash
cd fastapi_memo_course
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows PowerShell
# source .venv/bin/activate          # macOS / Linux
pip install -r requirements.txt
```

### 3. 접속 정보

앱은 아래 URL 로 접속합니다. 다른 계정이나 DB 를 쓰려면 환경 변수로 바꿉니다.

```
mysql+pymysql://hyundai:hyundai@localhost:3306/my_memo_app?charset=utf8mb4
```

```powershell
# PowerShell 예시
$env:DATABASE_URL       = "mysql+pymysql://아이디:비번@localhost:3306/my_memo_app?charset=utf8mb4"
$env:CHECK_DATABASE_URL = "mysql+pymysql://아이디:비번@localhost:3306/my_memo_app_test?charset=utf8mb4"
```

> 테이블은 직접 만들지 않습니다. 앱이 시작될 때 SQLAlchemy 의 `Base.metadata.create_all()` 이 `main.py` 의 모델대로 생성합니다.

---

## 데이터베이스 스키마

### 최종 스키마 (LAB 3 ~ 5)

![my_memo_app 최종 스키마](docs/db_erd.png)

`users` 와 `memo` 는 **1 : N** 관계입니다. 한 사용자가 여러 메모를 가지며, `memo.user_id` 가 `users.id` 를 가리킵니다.

### `users` 테이블 (LAB 2 부터)

| 컬럼              | 타입           | 제약                             | 설명                                                                |
| ----------------- | -------------- | -------------------------------- | ------------------------------------------------------------------- |
| `id`              | `INT`          | **PK**, `AUTO_INCREMENT`, 인덱스 | 사용자 번호                                                         |
| `username`        | `VARCHAR(100)` | **UNIQUE**, 인덱스               | 로그인 아이디. 같은 이름으로 두 번 가입할 수 없음                   |
| `email`           | `VARCHAR(200)` |                                  | 이메일                                                              |
| `hashed_password` | `VARCHAR(512)` |                                  | bcrypt 해시 (`$2b$12$...`, 60자). **평문 비밀번호는 저장하지 않음** |

### `memo` 테이블 (LAB 1 부터)

| 컬럼      | 타입            | 제약                             | 설명                                                         | 추가 시점 |
| --------- | --------------- | -------------------------------- | ------------------------------------------------------------ | --------- |
| `id`      | `INT`           | **PK**, `AUTO_INCREMENT`, 인덱스 | 메모 번호                                                    | LAB 1     |
| `user_id` | `INT`           | **FK** → `users.id`, 인덱스      | 작성자. 조회·수정·삭제 때 `user_id == 로그인 사용자` 로 거름 | LAB 3     |
| `title`   | `VARCHAR(100)`  | `NOT NULL` (LAB 3~)              | 메모 제목                                                    | LAB 1     |
| `content` | `VARCHAR(1000)` | `NOT NULL` (LAB 3~)              | 메모 내용                                                    | LAB 1     |

### 실제 생성되는 DDL

`create_all()` 이 MySQL 에 만드는 테이블입니다. (MySQL 8 의 `SHOW CREATE TABLE my_memo_app.users;` 형식)

```sql
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `hashed_password` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_username` (`username`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `memo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `title` varchar(100) NOT NULL,
  `content` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_memo_id` (`id`),
  CONSTRAINT `memo_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 같은 구조의 SQLAlchemy 모델

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(200))
    hashed_password = Column(String(512))

class Memo(Base):
    __tablename__ = "memo"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)
    user = relationship("User")      # memo.user 로 작성자 객체 접근
```

### LAB 별 스키마 변화

![LAB 별 스키마 변화](docs/db_schema_by_lab.png)

| LAB   | 테이블          | 변화                                               | 필요한 작업              |
| ----- | --------------- | -------------------------------------------------- | ------------------------ |
| 0     | 없음            | DB 를 쓰지 않음                                    | -                        |
| 1     | `memo`          | `id`, `title`, `content` 생성                      | 없음 (자동 생성)         |
| 2     | `memo`, `users` | `users` 추가                                       | 없음 (자동 생성)         |
| 3 ~ 5 | `memo`, `users` | `memo.user_id` FK 추가, `title`·`content` NOT NULL | **`python reset_db.py`** |

`create_all()` 은 **없는 테이블만 만들고 이미 있는 테이블은 바꾸지 않습니다.** 그래서 LAB 3 에서 컬럼이 추가될 때는 `reset_db.py` 로 테이블을 지우고 다시 만듭니다. (실무에서는 데이터를 지우지 않고 Alembic 같은 마이그레이션 도구로 `ALTER TABLE` 합니다.)

```bash
cd labs/student/lab3_memo
python reset_db.py        # 모든 테이블과 데이터를 지웁니다. 계속할까요? (y/N) → y
```

---

## 실행과 점검

항상 **해당 LAB 폴더 안에서** 실행합니다. (`templates/` 가 실행 위치 기준)

```bash
cd labs/student/lab1_db
uvicorn main:app --reload      # http://127.0.0.1:8000   ·   API 문서 http://127.0.0.1:8000/docs
python check_lab.py            # STEP 별 PASS / FAIL
```

```
PASS  STEP 1  Memo 모델 컬럼
FAIL  STEP 4  POST /memos/ 생성
      → 미완성: STEP 4: 메모 생성
...
결과: 3 / 7 통과
```

---

## 최종 API 목록

| 메서드 | 경로                 | 설명                                         | 인증 |  LAB  |
| ------ | -------------------- | -------------------------------------------- | :--: | :---: |
| GET    | `/`                  | 홈 (로그인 · 회원가입 화면)                  |      |   0   |
| GET    | `/about`             | 앱 소개 JSON                                 |      |   0   |
| GET    | `/hello/{name}?age=` | 매개변수 연습                                |      |   0   |
| POST   | `/signup`            | 회원가입 `{username, email, password}`       |      |   2   |
| POST   | `/login`             | 로그인 `{username, password}` → 세션 쿠키    |      |   2   |
| POST   | `/logout`            | 로그아웃                                     |      |   2   |
| GET    | `/me`                | 로그인 사용자 확인                           |  ✔   |   2   |
| POST   | `/memos/`            | 메모 생성 `{title, content}`                 |  ✔   | 1 → 3 |
| GET    | `/memos/`            | 내 메모 목록 페이지 (비로그인 시 `/` 로 303) |  ✔   | 1 → 3 |
| PUT    | `/memos/{id}`        | 메모 수정 (내 메모만)                        |  ✔   | 1 → 3 |
| DELETE | `/memos/{id}`        | 메모 삭제 (내 메모만)                        |  ✔   | 1 → 3 |

| 상태 코드 | 의미             | 이 프로젝트에서                        |
| :-------: | ---------------- | -------------------------------------- |
|    200    | 성공             | 정상 응답                              |
|    303    | 다른 곳으로 이동 | 비로그인으로 `/memos/` 접근            |
|    400    | 잘못된 요청      | 중복 가입                              |
|    401    | 인증 필요        | 로그인 실패, 비로그인 API 호출         |
|    404    | 없음             | 없는 메모, 남의 메모                   |
|    422    | 검증 실패        | 필수 값 누락, 타입 오류 (FastAPI 자동) |
|    500    | 서버 오류        | 저장 실패 후 rollback                  |

---

## 문제 해결

| 증상                                                                  | 해결                                                                                             |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `Can't connect to MySQL server on 'localhost'`                        | MySQL 서버가 실행 중인지 확인                                                                    |
| `Access denied for user 'hyundai'` / `Unknown database 'my_memo_app'` | root 로 `setup_mysql.sql` 실행                                                                   |
| `cryptography package is required ...`                                | `pip install cryptography` (MySQL 8 기본 인증)                                                   |
| `Unknown column 'user_id'`                                            | LAB 3 폴더에서 `python reset_db.py`                                                              |
| `[점검 불가] 점검용 MySQL DB 에 접속하지 못했습니다`                  | `my_memo_app_test` 생성 여부 확인 (`setup_mysql.sql`)                                            |
| `uvicorn` 명령을 찾을 수 없음                                         | 가상환경 활성화 후 `pip install -r requirements.txt`, 또는 `python -m uvicorn main:app --reload` |
| `TemplateNotFound`                                                    | LAB 폴더 안에서 실행했는지 확인                                                                  |
| 코드를 고쳤는데 반영이 안 됨                                          | `--reload` 옵션 확인, 다른 폴더의 서버가 떠 있지 않은지 확인                                     |
| PowerShell 에서 가상환경 활성화가 막힘                                | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` 한 번 실행                                 |
