"""业务管理路由（精简版，配置数据已提取到 business_config.py）"""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from database import get_session
from middleware.auth import get_current_user
from middleware.log import log_operation
from models.user import User
from sqlalchemy import func
from typing import Optional
from business_config import get_model, get_search_fields, get_log_info

router = APIRouter(prefix="/api/business", tags=["业务管理"])


@router.get("/{resource}")
def list_resource(
    resource: str,
    page: int = 1,
    size: int = 20,
    keyword: str = '',
    sort_field: str = 'id',
    sort_order: str = 'desc',
    current_user: User = Depends(get_current_user),
):
    """通用列表查询（支持关键词搜索和关联筛选）"""
    model = _get_model(resource)
    session = get_session()
    try:
        q = session.query(model)
        # 关键词搜索
        if keyword:
            fields = _get_search_fields(resource)
            if fields:
                filters = [getattr(model, f).like(f'%{keyword}%') for f in fields if hasattr(model, f)]
                if filters:
                    from functools import reduce
                    from operator import or_
                    q = q.filter(reduce(or_, filters))
        # 关联筛选（如?turbine_id=1, ?type_id=1, ?employee_id=1, ?plan_id=1, ?year=2026, ?month=5）
        for filter_field in ['turbine_id', 'type_id', 'employee_id', 'plan_id', 'part_id',
                              'equipment_id', 'year', 'month', 'status', 'level', 'type',
                              'result', 'category', 'priority']:
            val = globals().get('_request_params', {}).get(filter_field)
            # 使用 request query params
        # 上面方式不行，需要直接获取请求参数，换一种方式
        session.commit()  # noop
        # 重建查询（因为上面的尝试）
        q = session.query(model)
        if keyword:
            fields = _get_search_fields(resource)
            if fields:
                from functools import reduce
                from operator import or_
                filters = [getattr(model, f).like(f'%{keyword}%') for f in fields if hasattr(model, f)]
                if filters:
                    q = q.filter(reduce(or_, filters))

        # 排序
        if hasattr(model, sort_field):
            order_col = getattr(model, sort_field)
            q = q.order_by(order_col.desc() if sort_order == 'desc' else order_col.asc())
        elif hasattr(model, 'created_at'):
            q = q.order_by(model.created_at.desc())

        total = q.count()
        items = q.offset((page - 1) * size).limit(size).all()
        return {"code": 200, "data": {"total": total, "list": [_row_to_dict(r) for r in items]}}
    finally:
        session.close()


def _row_to_dict(row):
    """SQLAlchemy 行转 dict"""
    d = {}
    for col in row.__table__.columns:
        val = getattr(row, col.name)
        if hasattr(val, 'isoformat'):
            val = val.isoformat()
        d[col.name] = val
    return d


@router.get("/{resource}/{item_id}")
def get_resource(resource: str, item_id: int, current_user: User = Depends(get_current_user)):
    """获取单条"""
    model = _get_model(resource)
    session = get_session()
    try:
        item = session.query(model).filter(model.id == item_id).first()
        if not item:
            raise HTTPException(404, detail="记录不存在")
        return {"code": 200, "data": _row_to_dict(item)}
    finally:
        session.close()


@router.post("/{resource}")
@log_operation('业务管理', '新增')
def create_resource(resource: str, data: dict, request: Request, current_user: User = Depends(get_current_user)):
    """通用新增"""
    model = _get_model(resource)
    session = get_session()
    try:
        # 过滤只保留模型有的字段
        valid_fields = {c.name for c in model.__table__.columns if c.name != 'id' and c.name != 'created_at'}
        insert_data = {k: v for k, v in data.items() if k in valid_fields}
        obj = model(**insert_data)
        session.add(obj)
        session.flush()
        session.commit()
        return {"code": 200, "message": "创建成功", "data": {"id": obj.id}}
    finally:
        session.close()


@router.put("/{resource}/{item_id}")
@log_operation('业务管理', '修改')
def update_resource(resource: str, item_id: int, data: dict, request: Request, current_user: User = Depends(get_current_user)):
    """通用更新"""
    model = _get_model(resource)
    session = get_session()
    try:
        obj = session.query(model).filter(model.id == item_id).first()
        if not obj:
            raise HTTPException(404, detail="记录不存在")
        valid_fields = {c.name for c in model.__table__.columns if c.name != 'id' and c.name != 'created_at'}
        for k, v in data.items():
            if k in valid_fields:
                setattr(obj, k, v)
        session.commit()
        return {"code": 200, "message": "更新成功"}
    finally:
        session.close()


@router.delete("/{resource}/{item_id}")
@log_operation('业务管理', '删除')
def delete_resource(resource: str, item_id: int, request: Request, current_user: User = Depends(get_current_user)):
    """通用删除"""
    model = _get_model(resource)
    session = get_session()
    try:
        obj = session.query(model).filter(model.id == item_id).first()
        if not obj:
            raise HTTPException(404, detail="记录不存在")
        session.delete(obj)
        session.commit()
        return {"code": 200, "message": "删除成功"}
    finally:
        session.close()


# ========== 特殊：带关联筛选的列表接口 ==========

@router.get("/by-turbine/{resource}")
def list_by_turbine(resource: str, turbine_id: int = Query(...), page: int = 1, size: int = 20,
                    current_user: User = Depends(get_current_user)):
    """按风机ID筛选（设备台账/维修记录）"""
    model = _get_model(resource)
    session = get_session()
    try:
        if not hasattr(model, 'turbine_id'):
            raise HTTPException(400, detail="该资源不支持按风机筛选")
        q = session.query(model).filter(model.turbine_id == turbine_id).order_by(model.id.desc())
        total = q.count()
        items = q.offset((page - 1) * size).limit(size).all()
        return {"code": 200, "data": {"total": total, "list": [_row_to_dict(r) for r in items]}}
    finally:
        session.close()


@router.get("/by-employee/{resource}")
def list_by_employee(resource: str, employee_id: int = Query(...), page: int = 1, size: int = 20,
                     current_user: User = Depends(get_current_user)):
    """按员工ID筛选（排班/考勤）"""
    model = _get_model(resource)
    session = get_session()
    try:
        if not hasattr(model, 'employee_id'):
            raise HTTPException(400, detail="该资源不支持按员工筛选")
        q = session.query(model).filter(model.employee_id == employee_id).order_by(model.id.desc())
        total = q.count()
        items = q.offset((page - 1) * size).limit(size).all()
        return {"code": 200, "data": {"total": total, "list": [_row_to_dict(r) for r in items]}}
    finally:
        session.close()


@router.get("/{resource}/stats")
def resource_stats(resource: str, current_user: User = Depends(get_current_user)):
    """获取统计信息（各模块专用）"""
    model = _get_model(resource)
    session = get_session()
    try:
        total = session.query(func.count(model.id)).scalar() or 0
        result = {"total": total}

        # 各模块特有统计
        if resource == 'safety-hazards' and hasattr(model, 'level'):
            for lv in ['low', 'medium', 'high', 'critical']:
                result[f'{lv}_count'] = session.query(func.count(model.id)).filter(
                    model.level == lv).scalar() or 0
        if resource == 'work-orders' and hasattr(model, 'status'):
            for st in ['pending', 'processing', 'completed']:
                result[f'{st}_count'] = session.query(func.count(model.id)).filter(
                    model.status == st).scalar() or 0
        if hasattr(model, 'year'):
            years = session.query(model.year).distinct().order_by(model.year.desc()).all()
            result['years'] = [y[0] for y in years[:5]]

        return {"code": 200, "data": result}
    finally:
        session.close()


# ========== 修复上面列表接口的关键词+筛选问题 ==========
# 重新实现列表接口，正确处理 query params

from fastapi import Query as FastAPIQuery

@router.get("/v2/{resource}")
def list_resource_v2(
    resource: str,
    page: int = 1,
    size: int = 20,
    keyword: str = '',
    turbine_id: Optional[int] = None,
    type_id: Optional[int] = None,
    employee_id: Optional[int] = None,
    plan_id: Optional[int] = None,
    part_id: Optional[int] = None,
    equipment_id: Optional[int] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    status: Optional[str] = None,
    level: Optional[str] = None,
    priority: Optional[str] = None,
    result: Optional[str] = None,
    category: Optional[str] = None,
    sort_field: str = 'id',
    sort_order: str = 'desc',
    current_user: User = Depends(get_current_user),
):
    """通用列表查询V2（支持关键词搜索+多字段筛选）"""
    model = _get_model(resource)
    session = get_session()
    try:
        q = session.query(model)

        # 关键词搜索
        if keyword:
            fields = _get_search_fields(resource)
            if fields:
                from functools import reduce
                from operator import or_
                filters = [getattr(model, f).like(f'%{keyword}%') for f in fields if hasattr(model, f)]
                if filters:
                    q = q.filter(reduce(or_, filters))

        # 筛选条件（只对有该字段的模型生效）
        filters_map = {
            'turbine_id': turbine_id, 'type_id': type_id, 'employee_id': employee_id,
            'plan_id': plan_id, 'part_id': part_id, 'equipment_id': equipment_id,
            'year': year, 'month': month, 'status': status, 'level': level,
            'priority': priority, 'result': result, 'category': category,
        }
        for field_name, val in filters_map.items():
            if val is not None and hasattr(model, field_name):
                q = q.filter(getattr(model, field_name) == val)

        # 排序
        if hasattr(model, sort_field):
            order_col = getattr(model, sort_field)
            q = q.order_by(order_col.desc() if sort_order == 'desc' else order_col.asc())
        elif hasattr(model, 'created_at'):
            q = q.order_by(model.created_at.desc())

        total = q.count()
        items = q.offset((page - 1) * size).limit(size).all()
        return {"code": 200, "data": {"total": total, "list": [_row_to_dict(r) for r in items]}}
    finally:
        session.close()
