from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.database import Base, engine
from app import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 정의된 테이블 생성
    Base.metadata.create_all(bind=engine)

    yield

app = FastAPI(
    title="쑥쑥로그 API",
    description="아동 개인 맞춤형 건강 관찰 서비스",
    version="1.0.0",
    lifespan=lifespan
)

# System
@app.get("/", tags=["System"], summary="api 작동 확인")
def home():
    return {
        "message": "쑥쑥로그 api 정상 작동 중!"
    }


# Test
@app.get("/db-test", tags=["Test"], summary="데이터베이스 테스트")
def db_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        value = result.scalar()

    return {
        "database": "SQLite",
        "status": "connected",
        "test_result": value
    }

@app.get("/table-test", tags=["Test"], summary="테이블 생성 테스트")
def table_test():
    with engine.connect() as connection:
        result = connection.execute(
            text(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name='children'"
            )
        )
        table_name = result.scalar()

    return {
        "table": table_name,
        "status": "created" if table_name else "not found"
    }