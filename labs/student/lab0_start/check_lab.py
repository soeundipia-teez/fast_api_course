"""LAB 자동 점검 (완성본 · 수정하지 않음)   실행: 이 폴더에서  python check_lab.py
점검은 '점검 전용' MySQL DB(my_memo_app_test)에서 테이블을 새로 만들어 진행하므로
수업용 DB(my_memo_app)의 데이터에는 영향이 없습니다. (setup_mysql.sql 로 미리 생성)"""
import os
import sys
import warnings

warnings.filterwarnings("ignore")
os.environ["DATABASE_URL"] = os.getenv(
    "CHECK_DATABASE_URL",
    "mysql+pymysql://hyundai:hyundai@localhost:3306/my_memo_app_test?charset=utf8mb4",
)

try:
    from fastapi.testclient import TestClient  # noqa: E402

    import main  # noqa: E402  (import 할 때 create_all 로 테이블 생성)
except Exception as e:  # noqa: BLE001
    if "OperationalError" in type(e).__name__ or "Can't connect" in str(e) or "Access denied" in str(e) or "Unknown database" in str(e):
        print("[점검 불가] 점검용 MySQL DB 에 접속하지 못했습니다.")
        print(f"  {type(e).__name__}: {str(e).splitlines()[0][:160]}")
        print("  ① MySQL 서버 실행 여부  ② setup_mysql.sql 로 my_memo_app_test 와 hyundai 계정 생성 여부를 확인하세요.")
        sys.exit(1)
    raise

if hasattr(main, "engine"):
    # 점검 DB 를 깨끗하게: 모든 테이블을 지우고(외래 키 순서 고려) 이 LAB 구조로 다시 생성
    from sqlalchemy import MetaData

    _old = MetaData()
    _old.reflect(bind=main.engine)
    _old.drop_all(bind=main.engine)
    main.Base.metadata.create_all(bind=main.engine)

results = []


def check(name, fn):
    try:
        fn()
        results.append((name, True, ""))
    except NotImplementedError as e:
        results.append((name, False, f"미완성: {e}"))
    except AssertionError as e:
        results.append((name, False, str(e)))
    except Exception as e:  # noqa: BLE001
        results.append((name, False, f"{type(e).__name__}: {str(e).splitlines()[0][:200] if str(e) else ''}"))


def report():
    for name, ok, msg in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f"\n      → {msg}"))
    print(f"\n결과: {sum(ok for _, ok, _ in results)} / {len(results)} 통과")
    if hasattr(main, "engine"):
        main.engine.dispose()

# ----------------------------------------------------------------------

client = TestClient(main.app)


def t1():
    r = client.get("/about")
    assert r.status_code == 200, f"상태 코드 {r.status_code}"
    assert r.json() == {"message": "이것은 마이 메모 앱의 소개 페이지입니다."}, f"응답 {r.json()}"


def t2():
    r = client.get("/")
    assert r.status_code == 200, f"상태 코드 {r.status_code}"
    assert "text/html" in r.headers["content-type"], "HTML 이 아닙니다"
    assert "마이 메모 앱에 오신 것을 환영합니다!" in r.text, "app_name 이 템플릿에 들어가지 않았습니다"


def t3():
    r = client.get("/hello/네트")
    assert r.json() == {"greeting": "안녕하세요, 네트님!", "age": None}, f"응답 {r.json()}"
    r = client.get("/hello/네트", params={"age": 20})
    assert r.json()["age"] == 20, "age 가 int 로 오지 않았습니다"
    r = client.get("/hello/네트", params={"age": "abc"})
    assert r.status_code == 422, "잘못된 age 는 422 여야 합니다"


check("STEP 1  GET /about JSON", t1)
check("STEP 2  GET / 템플릿 렌더링", t2)
check("STEP 3  경로·쿼리 매개변수", t3)

report()
