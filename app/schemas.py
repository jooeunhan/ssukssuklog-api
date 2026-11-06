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
