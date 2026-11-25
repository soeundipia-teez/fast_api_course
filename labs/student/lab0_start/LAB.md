# LAB 0 · FastAPI 시작하기 (40분)

첫 웹 서버를 띄우고, URL 과 파이썬 함수를 연결하는 '라우팅'을 익힙니다.

## 학습 목표
- `uvicorn main:app --reload` 로 서버를 실행한다
- JSON 을 돌려주는 API 와 HTML 을 돌려주는 페이지를 구분한다
- 경로 매개변수·쿼리 매개변수를 타입 힌트로 받는다

## 실습 단계
| STEP | 파일 | 할 일 |
|---|---|---|
| STEP 1 | main.py | `GET /about` → `{"message": "이것은 마이 메모 앱의 소개 페이지입니다."}` |
| STEP 2 | main.py | `GET /` → `TemplateResponse(request, "home.html", {"app_name": "마이 메모 앱"})` |
| STEP 3 | main.py | `GET /hello/{name}?age=20` → `{"greeting": "안녕하세요, 네트님!", "age": 20}` |

## 실행
```bash
cd labs/student/lab0_start
uvicorn main:app --reload
# 브라우저: http://127.0.0.1:8000/  /about  /hello/네트?age=20  /docs
python check_lab.py
```

## 확인
- [ ] 브라우저에서 `/` 에 제목이 보인다
- [ ] `/docs` 에 경로 3개가 자동으로 정리되어 있다
- [ ] `/hello/네트?age=abc` 가 422 로 거절된다
- [ ] `python check_lab.py` 3 / 3 통과

## 자주 나는 오류
| 증상 | 원인 · 해결 |
|---|---|
| `uvicorn` 명령을 찾을 수 없음 | 가상환경이 활성화되지 않았거나 설치 전입니다. `pip install -r requirements.txt` 또는 `python -m uvicorn main:app --reload` |
| `Error loading ASGI app. Could not import module "main"` | main.py 가 있는 폴더에서 실행해야 합니다. `cd labs/student/lab0_start` |
| `TemplateNotFound: home.html` | `templates` 폴더 위치 확인. 실행 위치 기준 상대 경로입니다 |
| 포트 8000 사용 중 | 다른 서버가 떠 있습니다. Ctrl+C 로 끄거나 `--port 8001` |

## 도전 과제
- `GET /health` → `{"status": "ok"}` 추가
- home.html 에 오늘 날짜를 파이썬에서 넘겨 표시하기
- `netstat -an | findstr 8000` 으로 uvicorn 의 LISTENING 확인 (앞 과정 복습)

> 개념 설명과 도식은 `lesson_plan/` 의 HTML 교안을 함께 보세요.
