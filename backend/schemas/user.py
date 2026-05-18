"""用户相关 Pydantic 模型"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user: "UserInfo"


class UserInfo(BaseModel):
    id: int
    username: str
    nickname: str
    email: str
    phone: str
    avatar: str
    status: bool
    is_admin: bool
    roles: List[str] = []
    permissions: List[str] = []

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=4, max_length=128)
    nickname: str = Field(default='', max_length=50)
    email: str = Field(default='', max_length=100)
    phone: str = Field(default='', max_length=20)
    status: bool = True
    role_ids: List[int] = []


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[bool] = None
    role_ids: Optional[List[int]] = None


class UserOut(BaseModel):
    id: int
    username: str
    nickname: str
    email: str
    phone: str
    status: bool
    is_admin: bool
    remark: str
    created_at: datetime
    roles: List[str] = []

    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    code: str = Field(..., min_length=1, max_length=50)
    status: bool = True
    sort: int = 0
    remark: str = ''
    menu_ids: List[int] = []


class RoleOut(BaseModel):
    id: int
    name: str
    code: str
    status: bool
    sort: int
    remark: str
    created_at: datetime

    class Config:
        from_attributes = True


class MenuCreate(BaseModel):
    parent_id: int = 0
    name: str = Field(..., max_length=50)
    path: str = ''
    component: str = ''
    permission: str = ''
    icon: str = ''
    type: str = 'menu'
    sort: int = 0
    status: bool = True
    hidden: bool = False


class MenuOut(BaseModel):
    id: int
    parent_id: int
    name: str
    path: str
    component: str
    permission: str
    icon: str
    type: str
    sort: int
    status: bool
    hidden: bool
    children: List["MenuOut"] = []

    class Config:
        from_attributes = True
