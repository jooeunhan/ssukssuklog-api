from pydantic import BaseModel, ConfigDict, Field
from datetime import date,datetime
from pydantic import BaseModel, ConfigDict, Field


class ChildBase(BaseModel):
    name: str
    class_name: str
    age: int = Field(ge=0)
    gender: str
    allergies: list[str] = Field(default_factory=list)


class ChildCreate(ChildBase):
    pass


class ChildUpdate(BaseModel):
    name: str | None = None
    class_name: str | None = None
    age: int | None = Field(default=None, ge=0)
    gender: str | None = None
    allergies: list[str] | None = None


class ChildResponse(ChildBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# 건강 기록 공통 스키마
class HealthRecordBase(BaseModel):
    date: date

    morning_temp: float | None = Field(
        default=None,
        ge=30.0,
        le=43.0
    )

    noon_temp: float | None = Field(
        default=None,
        ge=30.0,
        le=43.0
    )

    afternoon_temp: float | None = Field(
        default=None,
        ge=30.0,
        le=43.0
    )

    clinical_note: str = ""

    selected_symptoms: list[str] = Field(
        default_factory=list
    )


# 건강 기록 생성
class HealthRecordCreate(HealthRecordBase):
    pass


# 건강 기록 수정
class HealthRecordUpdate(BaseModel):
    morning_temp: float | None = Field(
        default=None,
        ge=30.0,
        le=43.0
    )

    noon_temp: float | None = Field(
        default=None,
        ge=30.0,
        le=43.0
    )

    afternoon_temp: float | None = Field(
        default=None,
        ge=30.0,
        le=43.0
    )

    clinical_note: str | None = None

    selected_symptoms: list[str] | None = None


# 건강 기록 응답
class HealthRecordResponse(HealthRecordBase):
    id: int
    child_id: int

    analysis_status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
