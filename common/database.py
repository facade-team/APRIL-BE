import os

from dotenv import load_dotenv

load_dotenv()

# DB 관련 secrets 값 불러오기
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("PASSWORD")
db_host = os.environ.get("HOST")
db_port = os.environ.get("PORT")
db_database = os.environ.get("DATABASE")


DB_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}?charset=utf8"
