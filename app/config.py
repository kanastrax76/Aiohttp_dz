import os

PG_USER = os.getenv("PG_USER", "some_user")
PG_PASSWORD = os.getenv("PG_PASSWORD", "secret")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", 5433))
PG_DB = os.getenv("PG_DB", "aiohttp_db")
PG_DSN = os.getenv("PG_DSN", f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}")
SECRET_KEY = os.getenv("SECRET_KEY", "fjk3ghg1hr3ke@kfl3j3afk23485968456bj3vbj5460mv")


API_URL = os.getenv("API_URL", "http://127.0.0.1:8080")
DLT_USER = "user_test1@gg.com"
DLT_PSW = "Soe1fa34532!ddDd23"

ROOT_USER_EMAIL = "root@toor.te"
ROOT_USER_PASSWORD = "Root!ddd3raarDEWSAwqe2"