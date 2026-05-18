"""字典、日志、配置模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime, timezone
from models.base import Base


class DictType(Base):
    """字典类型"""
    __tablename__ = 'dict_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, comment='字典名称')
    code = Column(String(50), unique=True, nullable=False, comment='字典标识')
    status = Column(Boolean, default=True, comment='状态')
    remark = Column(String(500), default='', comment='备注')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DictData(Base):
    """字典数据"""
    __tablename__ = 'dict_data'

    id = Column(Integer, primary_key=True, index=True)
    dict_code = Column(String(50), nullable=False, comment='所属字典标识')
    label = Column(String(50), nullable=False, comment='字典标签')
    value = Column(String(50), nullable=False, comment='字典值')
    sort = Column(Integer, default=0, comment='排序')
    status = Column(Boolean, default=True, comment='状态')
    tag_type = Column(String(20), default='', comment='标签类型: primary/success/warning/danger/info')
    remark = Column(String(500), default='', comment='备注')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Config(Base):
    """系统配置"""
    __tablename__ = 'configs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, comment='配置名称')
    key = Column(String(50), unique=True, nullable=False, comment='配置键')
    value = Column(Text, default='', comment='配置值')
    remark = Column(String(500), default='', comment='备注')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class OperationLog(Base):
    """操作日志"""
    __tablename__ = 'operation_logs'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), default='', comment='操作人')
    module = Column(String(50), default='', comment='操作模块')
    action = Column(String(50), default='', comment='操作类型')
    method = Column(String(200), default='', comment='请求方法')
    url = Column(String(500), default='', comment='请求URL')
    ip = Column(String(50), default='', comment='操作IP')
    params = Column(Text, default='', comment='请求参数')
    result = Column(String(10), default='success', comment='结果: success/fail')
    cost_time = Column(Integer, default=0, comment='耗时(ms)')
    error_msg = Column(Text, default='', comment='错误信息')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class LoginLog(Base):
    """登录日志"""
    __tablename__ = 'login_logs'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), default='', comment='用户名')
    status = Column(String(10), default='success', comment='状态: success/fail')
    ip = Column(String(50), default='', comment='登录IP')
    message = Column(String(500), default='', comment='消息')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
