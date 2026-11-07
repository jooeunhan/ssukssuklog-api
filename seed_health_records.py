import json
from datetime import date
from pathlib import Path

from sqlalchemy.orm import Session

from app.database import engine
from app.models import Child, HealthRecord

BASE_DIR = Path(__file__).resolve().parent
SEED_PATH = BASE_DIR / "data" / "health_records_seed.json"
CHILD_ID = 1

def seed_health_records():
    with SEED_PATH.open("r", encoding="utf-8") as f:
        records = json.load(f)

    if not isinstance(records, list):
        raise ValueError("JSON 최상위 구조는 배열")

    with Session(engine) as db:
        child = db.get(Child, CHILD_ID)

        if child is None:
            print("아동 정보 없음. 서버 먼저 실행해주세요")
            return

        added = 0
        skipped = 0

        for item in records:
            record_date = date.fromisoformat(item["date"])

            existing = (
                db.query(HealthRecord)
                .filter(
                    HealthRecord.child_id == CHILD_ID,
                    HealthRecord.date == record_date
                )
                .first()
            )

            if existing:
                skipped += 1
                continue

            record = HealthRecord(
                child_id=CHILD_ID,
                date=record_date,
                morning_temp=item.get("morning_temp"),
                noon_temp=item.get("noon_temp"),
                afternoon_temp=item.get("afternoon_temp"),
                clinical_note=item.get("clinical_note"),
                selected_symptoms=item.get("selected_symptoms", []),
                analysis_status="pending"
            )

            db.add(record)
            added += 1

        db.commit()

        print(f"등록: {added}")
        print(f"중복 건너뜀: {skipped}")

if __name__ == "__main__":
    seed_health_records()