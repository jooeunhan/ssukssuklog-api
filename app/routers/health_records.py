
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db


router = APIRouter(
    prefix="/children/{child_id}/records",
    tags=["Health Records"]
)


def get_child_or_404(db: Session, child_id: int):
    child = db.get(models.Child, child_id)

    if child is None:
        raise HTTPException(
            status_code=404,
            detail="해당 아동을 찾을 수 없습니다."
        )

    return child


def get_record_or_404(
    db: Session,
    child_id: int,
    record_id: int
):
    record = db.query(models.HealthRecord).filter(
        models.HealthRecord.id == record_id,
        models.HealthRecord.child_id == child_id
    ).first()

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="해당 건강 기록을 찾을 수 없습니다."
        )

    return record


# 건강 기록 등록
@router.post(
    "",
    summary="건강 기록 등록",
    response_model=schemas.HealthRecordResponse,
    status_code=status.HTTP_201_CREATED
)
def create_health_record(
    child_id: int,
    record_data: schemas.HealthRecordCreate,
    db: Session = Depends(get_db)
):
    get_child_or_404(db, child_id)

    existing_record = db.query(models.HealthRecord).filter(
        models.HealthRecord.child_id == child_id,
        models.HealthRecord.date == record_data.date
    ).first()

    if existing_record:
        raise HTTPException(
            status_code=409,
            detail="해당 날짜의 건강 기록이 이미 존재합니다."
        )

    new_record = models.HealthRecord(
        child_id=child_id,
        **record_data.model_dump(),
        analysis_status="pending"
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


# 건강 기록 전체 조회
@router.get(
    "",
    summary="건강 기록 전체 조회",
    response_model=list[schemas.HealthRecordResponse]
)
def get_health_records(
    child_id: int,
    db: Session = Depends(get_db)
):
    get_child_or_404(db, child_id)

    records = db.query(models.HealthRecord).filter(
        models.HealthRecord.child_id == child_id
    ).order_by(
        models.HealthRecord.date.desc()
    ).all()

    return records


# 특정 건강 기록 조회
@router.get(
    "/{record_id}",
    summary="특정 건강 기록 조회",
    response_model=schemas.HealthRecordResponse
)
def get_health_record(
    child_id: int,
    record_id: int,
    db: Session = Depends(get_db)
):
    get_child_or_404(db, child_id)

    return get_record_or_404(
        db,
        child_id,
        record_id
    )


# 건강 기록 수정
@router.patch(
    "/{record_id}",
    summary="건강 기록 수정",
    response_model=schemas.HealthRecordResponse
)
def update_health_record(
    child_id: int,
    record_id: int,
    record_data: schemas.HealthRecordUpdate,
    db: Session = Depends(get_db)
):
    get_child_or_404(db, child_id)

    record = get_record_or_404(
        db,
        child_id,
        record_id
    )

    updated_data = record_data.model_dump(
        exclude_unset=True
    )

    for key, value in updated_data.items():
        setattr(record, key, value)

    if updated_data:
        # 입력 정보가 변경되면 기존 분석 상태 초기화
        record.analysis_status = "pending"

    db.commit()
    db.refresh(record)

    return record
