from datetime import datetime
from pydantic import BaseModel, UUID4


class UserBase(BaseModel):
    login: str
    password: str


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class History(BaseModel):
    user_agent: str
    ip_address: str
    auth_datetime: datetime
