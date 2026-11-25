"""
수업용 DB 초기화 도구 (완성본 · 수정하지 않음)
=====================================================================
my_memo_app 의 테이블을 '모두' 지우고, 이 LAB 의 main.py 모델 구조로 다시 만듭니다.
  - LAB 3 에서 memo 테이블에 user_id 가 추가될 때 꼭 한 번 실행합니다.
  - 데이터가 꼬였을 때 처음부터 다시 하고 싶을 때 사용합니다.
실행:  python reset_db.py        (이 폴더에서)
=====================================================================
"""
import warnings

from sqlalchemy import MetaData

warnings.filterwarnings("ignore")
import main  # noqa: E402

url = main.engine.url
print(f"대상 DB : {url.database}  ({url.username}@{url.host}:{url.port})")
if input("모든 테이블과 데이터를 지웁니다. 계속할까요? (y/N) ").strip().lower() != "y":
    print("취소했습니다.")
    raise SystemExit

old = MetaData()
old.reflect(bind=main.engine)
print("삭제 :", ", ".join(old.tables) or "(없음)")
old.drop_all(bind=main.engine)
main.Base.metadata.create_all(bind=main.engine)
print("생성 :", ", ".join(main.Base.metadata.tables))
main.engine.dispose()
