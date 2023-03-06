from datetime import datetime
from pydantic import BaseModel, UUID4, UUID1
from typing import Union


class UserBase(BaseModel):
    login: str
    password: str


class UserCreate(UserBase):
    email: str


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class History(BaseModel):
    user_agent: str
    ip_address: str
    auth_datetime: datetime


class RoleBase(BaseModel):
    name: str


class RoleUser(BaseModel):
    user_id: Union[UUID4, UUID1]
    role_id: Union[UUID4, UUID1]
