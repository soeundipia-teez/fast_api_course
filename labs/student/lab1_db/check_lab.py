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
state = {}


def t1():
    cols = {c.name for c in main.Memo.__table__.columns}
    assert {"id", "title", "content"} <= cols, f"memo 컬럼: {cols}"


def t2():
    main.MemoCreate(title="a", content="b")
    try:
        main.MemoCreate(title="a")
        raise AssertionError("content 가 없는데도 MemoCreate 가 통과했습니다")
    except Exception as e:  # noqa: BLE001
        if isinstance(e, AssertionError):
            raise
    assert main.MemoUpdate().title is None, "MemoUpdate 의 기본값은 None 이어야 합니다"


def t3():
    gen = main.get_db()
    db = next(gen)
    assert db is not None, "세션이 없습니다"
    gen.close()


def t4():
    r = client.post("/memos/", json={"title": "장보기", "content": "우유, 계란"})
    assert r.status_code == 200, f"상태 코드 {r.status_code} {r.text}"
    body = r.json()
    assert body["title"] == "장보기" and isinstance(body["id"], int), f"응답 {body}"
    state["id"] = body["id"]
    r = client.post("/memos/", json={"title": "제목만"})
    assert r.status_code == 422, "content 누락 요청은 422 여야 합니다"


def t5():
    client.post("/memos/", json={"title": "두번째", "content": "내용"})
    r = client.get("/memos/")
    assert r.status_code == 200, f"상태 코드 {r.status_code}"
    titles = [m["title"] for m in r.json()]
    assert titles == ["장보기", "두번째"], f"목록 {titles}"


def t6():
    r = client.put(f"/memos/{state['id']}", json={"content": "우유, 계란, 빵"})
    assert r.status_code == 200, f"상태 코드 {r.status_code}"
    assert r.json() == {"id": state["id"], "title": "장보기", "content": "우유, 계란, 빵"}, f"응답 {r.json()}"
    r = client.put("/memos/9999", json={"title": "x"})
    assert r.status_code == 404, f"없는 메모 수정은 404 여야 합니다 (현재 {r.status_code})"


def t7():
    r = client.delete(f"/memos/{state['id']}")
    assert r.status_code == 200, f"상태 코드 {r.status_code}"
    assert len(client.get("/memos/").json()) == 1, "삭제 후 목록 개수가 1 이 아닙니다"
    assert client.delete(f"/memos/{state['id']}").status_code == 404, "이미 지운 메모 삭제는 404"


check("STEP 1  Memo 모델 컬럼", t1)
check("STEP 2  Pydantic 스키마", t2)
check("STEP 3  get_db 세션", t3)
check("STEP 4  POST /memos/ 생성", t4)
check("STEP 5  GET /memos/ 목록", t5)
check("STEP 6  PUT /memos/{id} 수정", t6)
check("STEP 7  DELETE /memos/{id} 삭제", t7)
report()
