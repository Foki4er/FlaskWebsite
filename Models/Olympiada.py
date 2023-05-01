from pydantic import BaseModel
from datetime import datetime


class BaseOlympiad(BaseModel):
    title: str
    introduction: str
    text: str


class GetOlympiad(BaseOlympiad):
    id: int
    date: datetime

    class Config:
        orm_mode = True


class PostOlympiad(BaseOlympiad):
    class Config:
        orm_mode = True
