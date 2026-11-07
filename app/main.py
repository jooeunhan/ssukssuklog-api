import json
from pathlib import Path

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import Base, engine
from app import models
from app.routers import children, health_records, dashboard

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    data_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "demo_child.json"
    )

    if data_path.exists():
        with data_path.open("r", encoding="utf-8") as file:
            child_data = json.load(file)

        with Session(engine) as db:
            child = db.get(models.Child, child_data["id"])

            if child is None:
                db.add(models.Child(**child_data))
                db.commit()

    yield

app = FastAPI(
    title="쑥쑥로그 API",
    description="아동 개인 맞춤형 건강 관찰 서비스",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

app.include_router(children.router)
app.include_router(health_records.router)
app.include_router(dashboard.router)