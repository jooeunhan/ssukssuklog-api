from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db


router = APIRouter(
    prefix="/children/{child_id}/dashboard",
    tags=["Dashboard"]
)


@router.get("", summary="건강 대시보드 조회")
def get_dashboard(
    child_id: int,
    db: Session = Depends(get_db)
):
    # 1. 아동 조회
    child = db.get(models.Child, child_id)

    if child is None:
        raise HTTPException(
            status_code=404,
            detail="해당 아동을 찾을 수 없습니다."
        )

    # 2. 건강 기록 조회 (최근 날짜순)
    records = (
        db.query(models.HealthRecord)
        .filter(models.HealthRecord.child_id == child_id)
        .order_by(
            models.HealthRecord.date.desc(),
            models.HealthRecord.id.desc()
        )
        .all()
    )

    # 3. 최신 건강 기록
    latest_record = records[0] if records else None

    # 4. 체온 그래프용 데이터 (오래된 날짜순)
    temperature_history = [
        {
            "date": record.date,
            "morning_temp": record.morning_temp,
            "noon_temp": record.noon_temp,
            "afternoon_temp": record.afternoon_temp
        }
        for record in reversed(records)
    ]

    # 5. 응답 반환
    return {
        "child": schemas.ChildResponse.model_validate(
            child
        ).model_dump(mode="json"),

        "latest_record": (
            schemas.HealthRecordResponse.model_validate(
                latest_record
            ).model_dump(mode="json")
            if latest_record else None
        ),

        "temperature_history": temperature_history,

        "analysis_status": (
            latest_record.analysis_status
            if latest_record else "pending"
        )
    }
