from sqlalchemy import Column, Integer, String, JSON
from app.database import Base

class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    class_name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    allergies = Column(JSON, nullable=False, default=list)