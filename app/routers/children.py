from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas


router = APIRouter(
    prefix="/children",
    tags=["Children"]
)


@router.get(
    "/{child_id}",
    summary="아동 정보 조회",
    response_model=schemas.ChildResponse
)
def get_child(
    child_id: int,
    db: Session = Depends(get_db)
):
    child = db.get(models.Child, child_id)

    if child is None:
        raise HTTPException(
            status_code=404,
            detail="해당 아동을 찾을 수 없습니다."
        )

    return child