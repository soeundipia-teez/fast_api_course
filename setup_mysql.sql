-- =====================================================================
-- 마이 메모 앱 MySQL 준비 스크립트 (처음 한 번, root 계정으로 실행)
--   mysql -u root -p < setup_mysql.sql
--   또는 MySQL Workbench 에서 이 파일을 열어 전체 실행(⚡)
-- =====================================================================

-- 수업용 DB (uvicorn 으로 실행할 때 사용)
CREATE DATABASE IF NOT EXISTS my_memo_app
  DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 자동 점검(check_lab.py) 전용 DB  ※ 점검할 때마다 테이블을 지우고 다시 만듭니다
CREATE DATABASE IF NOT EXISTS my_memo_app_test
  DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 실습 계정: hyundai / hyundai
CREATE USER IF NOT EXISTS 'hyundai'@'localhost' IDENTIFIED BY 'hyundai';
GRANT ALL PRIVILEGES ON my_memo_app.*      TO 'hyundai'@'localhost';
GRANT ALL PRIVILEGES ON my_memo_app_test.* TO 'hyundai'@'localhost';
FLUSH PRIVILEGES;

-- 확인
SHOW DATABASES LIKE 'my_memo_app%';
