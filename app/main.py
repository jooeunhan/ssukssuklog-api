from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine

app = FastAPI(
    title="쑥쑥로그 API",
    description="아동 개인 맞춤형 건강 관찰 서비스",
    version="1.0.0"
)


@app.get("/", tags=["System"], summary="api 작동 확인")
def home():
    return {
        "message": "쑥쑥로그 api 정상 작동 중!"
    }


@app.get("/db-test", tags=["System"], summary="데이터베이스 테스트")
def db_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        value = result.scalar()

    return {
        "database": "SQLite",
        "status": "connected",
        "test_result": value
    }