from app.database import Base
from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Float, Text,
    Date, DateTime, ForeignKey, JSON, UniqueConstraint
)
from sqlalchemy.orm import relationship

class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    class_name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    allergies = Column(JSON, nullable=False, default=list)
    health_records = relationship(
        "HealthRecord",
        back_populates="child"
    )

class HealthRecord(Base):
    __tablename__ = "health_records"

    __table_args__ = (
        UniqueConstraint(
            "child_id",
            "date",
            name="uq_child_health_date"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    child_id = Column(
        Integer,
        ForeignKey("children.id"),
        nullable=False,
        index=True
    )

    date = Column(
        Date,
        nullable=False
    )

    morning_temp = Column(Float, nullable=True)
    noon_temp = Column(Float, nullable=True)
    afternoon_temp = Column(Float, nullable=True)

    clinical_note = Column(
        Text,
        nullable=False,
        default=""
    )

    selected_symptoms = Column(
        JSON,
        nullable=False,
        default=list
    )

    analysis_status = Column(
        String(20),
        nullable=False,
        default="pending"
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    child = relationship(
        "Child",
        back_populates="health_records"
    )
