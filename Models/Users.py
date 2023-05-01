from pydantic import BaseModel
from datetime import datetime


class Profiles(BaseModel):
    id: int = 0
    name: str
    old: int
    city: str


class BaseUser(BaseModel):
    email: str
    pr: Profiles = None


class UserGet(BaseUser):
    id: int
    is_active: bool
    date: datetime

    class Config:
        orm_mode = True


class UserPost(BaseUser):
    psw: str
