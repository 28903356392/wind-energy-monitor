"""用户、角色、菜单模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.base import Base

# ---------- 关联表 ----------
user_role = Table(
    'user_role', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
)

role_menu = Table(
    'role_menu', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('menu_id', Integer, ForeignKey('menus.id', ondelete='CASCADE'), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, comment='用户名')
    password = Column(String(128), nullable=False, comment='密码(加密后)')
    nickname = Column(String(50), default='', comment='昵称')
    email = Column(String(100), default='', comment='邮箱')
    phone = Column(String(20), default='', comment='手机号')
    avatar = Column(String(200), default='', comment='头像')
    status = Column(Boolean, default=True, comment='状态: True启用 False停用')
    is_admin = Column(Boolean, default=False, comment='是否超管')
    remark = Column(String(500), default='', comment='备注')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_login_at = Column(DateTime, nullable=True, comment='最后登录时间')

    roles = relationship('Role', secondary=user_role, back_populates='users')


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, comment='角色名称')
    code = Column(String(50), unique=True, nullable=False, comment='角色标识')
    status = Column(Boolean, default=True, comment='状态')
    sort = Column(Integer, default=0, comment='排序')
    remark = Column(String(500), default='', comment='备注')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    users = relationship('User', secondary=user_role, back_populates='roles')
    menus = relationship('Menu', secondary=role_menu, back_populates='roles')


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, default=0, comment='父菜单ID')
    name = Column(String(50), nullable=False, comment='菜单名称')
    path = Column(String(200), default='', comment='路由地址')
    component = Column(String(200), default='', comment='组件路径')
    permission = Column(String(100), default='', comment='权限标识')
    icon = Column(String(50), default='', comment='图标')
    type = Column(String(20), default='menu', comment='类型: directory/menu/button')
    sort = Column(Integer, default=0, comment='排序')
    status = Column(Boolean, default=True, comment='状态')
    hidden = Column(Boolean, default=False, comment='是否隐藏')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    roles = relationship('Role', secondary=role_menu, back_populates='menus')
