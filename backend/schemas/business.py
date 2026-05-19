"""业务管理 Pydantic 模型"""
from pydantic import BaseModel, Field
from typing import Optional, List


class PageParams(BaseModel):
    page: int = 1
    size: int = 20


class PageResponse(BaseModel):
    total: int
    list: list


# ---- 设备类型 ----
class EquipmentTypeCreate(BaseModel):
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=50)
    category: str = ''
    description: str = ''
    status: bool = True
    sort: int = 0


class EquipmentTypeUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None
    sort: Optional[int] = None


# ---- 设备台账 ----
class EquipmentLedgerCreate(BaseModel):
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=50)
    type_id: int = 0
    type_name: str = ''
    turbine_id: int = 0
    turbine_name: str = ''
    model: str = ''
    manufacturer: str = ''
    install_date: str = ''
    warranty_expire: str = ''
    status: str = 'normal'
    description: str = ''


class EquipmentLedgerUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    type_id: Optional[int] = None
    type_name: Optional[str] = None
    turbine_id: Optional[int] = None
    turbine_name: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    install_date: Optional[str] = None
    warranty_expire: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None


# ---- 维修记录 ----
class MaintenanceCreate(BaseModel):
    equipment_id: int = 0
    equipment_name: str = ''
    turbine_id: int = 0
    turbine_name: str = ''
    fault_description: str = ''
    fault_type: str = ''
    priority: str = 'medium'
    repair_content: str = ''
    repair_person: str = ''
    repair_cost: float = 0.0
    start_time: str = ''
    end_time: str = ''
    status: str = 'pending'


class MaintenanceUpdate(BaseModel):
    equipment_id: Optional[int] = None
    fault_description: Optional[str] = None
    fault_type: Optional[str] = None
    priority: Optional[str] = None
    repair_content: Optional[str] = None
    repair_person: Optional[str] = None
    repair_cost: Optional[float] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    status: Optional[str] = None


# ---- 通用 CRUD Schema 工厂 ----
# 以下使用同一套 Create/Update schema 简化实现

class DictItem(BaseModel):
    name: str = Field(..., max_length=200)
    code: Optional[str] = None
    status: bool = True
    sort: int = 0
    remark: str = ''


class GenericCreate(BaseModel):
    name: str = Field(..., max_length=200)
    code: Optional[str] = None
    status: bool = True
    sort: int = 0
    remark: str = ''
    # 扩展字段
    extra: Optional[dict] = None


class GenericUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    status: Optional[bool] = None
    sort: Optional[int] = None
    remark: Optional[str] = None
    extra: Optional[dict] = None
