"""系统管理路由: 用户/角色/菜单/字典/日志/监控"""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from database import get_session
from models.user import User, Role, Menu
from models.system import DictType, DictData, Config, LoginLog, OperationLog
from schemas.user import UserCreate, UserUpdate, RoleCreate, MenuCreate, MenuOut
from security import hash_password
from middleware.auth import get_current_user
from middleware.log import log_operation
from sqlalchemy import func
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/api/system", tags=["系统管理"])


# ===================== 用户管理 =====================

@router.get("/users")
def list_users(page: int = 1, size: int = 20, keyword: str = '', current_user: User = Depends(get_current_user)):
    session = get_session()
    try:
        q = session.query(User)
        if keyword:
            q = q.filter(User.username.like(f'%{keyword}%') | User.nickname.like(f'%{keyword}%'))
        total = q.count()
        users = q.order_by(User.id).offset((page - 1) * size).limit(size).all()
        return {
            "code": 200,
            "data": {
                "total": total,
                "list": [{
                    "id": u.id, "username": u.username, "nickname": u.nickname,
                    "email": u.email, "phone": u.phone, "status": u.status,
                    "is_admin": u.is_admin, "remark": u.remark,
                    "created_at": u.created_at.isoformat() if u.created_at else '',
                    "roles": [r.code for r in u.roles],
                } for u in users]
            }
        }
    finally:
        session.close()


@router.post("/users")
def create_user(data: UserCreate, request: Request, current_user: User = Depends(get_current_user)):
    session = get_session()
    try:
        if session.query(User).filter(User.username == data.username).first():
            raise HTTPException(400, detail="用户名已存在")
        user = User(
            username=data.username,
            password=hash_password(data.password),
            nickname=data.nickname or data.username,
            email=data.email, phone=data.phone, status=data.status,
        )
        session.add(user)
        session.flush()
        # 关联角色
        if data.role_ids:
            roles = session.query(Role).filter(Role.id.in_(data.role_ids)).all()
            user.roles = roles
        session.commit()
        return {"code": 200, "message": "创建成功", "data": {"id": user.id}}
    finally:
        session.close()


@router.put("/users/{user_id}")
def update_user(user_id: int, data: UserUpdate, current_user: User = Depends(get_current_user)):
    session = get_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(404, detail="用户不存在")
        for k, v in data.model_dump(exclude_none=True).items():
            if k == 'role_ids' and v is not None:
                user.roles = session.query(Role).filter(Role.id.in_(v)).all()
            elif k != 'role_ids':
                setattr(user, k, v)
        session.commit()
        return {"code": 200, "message": "更新成功"}
    finally:
        session.close()


@router.delete("/users/{user_id}")
def delete_user(user_id: int, current_user: User = Depends(get_current_user)):
    session = get_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(404, detail="用户不存在")
        if user.is_admin:
            raise HTTPException(400, detail="不能删除超管用户")
        session.delete(user)
        session.commit()
        return {"code": 200, "message": "删除成功"}
    finally:
        session.close()


# ===================== 角色管理 =====================

@router.get("/roles")
def list_roles(page: int = 1, size: int = 20, current_user: User = Depends(get_current_user)):
    session = get_session()
    try:
        total = session.query(func.count(Role.id)).scalar() or 0
        roles = session.query(Role).order_by(Role.sort).offset((page - 1) * size).limit(size).all()
        return {
            "code": 200,
            "data": {
                "total": total,
                "list": [{"id": r.id, "name": r.name, "code": r.code,
                          "status": r.status, "sort": r.sort, "remark": r.remark,
                          "created_at": r.created_at.isoformat() if r.created_at else ''}
                         for r in roles]
            }
        }
    finally:
        session.close()


@router.post("/roles")
def create_role(data: RoleCreate, current_user: User = Depends(get_current_user)):
    session = get_session()
    try:
        if session.query(Role).filter(Role.code == data.code).first():
            raise HTTPException(400, detail="角色标识已存在")
        role = Role(name=data.name, code=data.code, status=data.status, sort=data.sort, remark=data.remark)
        session.add(role)
        session.flush()
        if data.menu_ids:
            menus = session.query(Menu).filter(Menu.id.in_(data.menu_ids)).all()
            role.menus = menus
        session.commit()
        return {"code": 200, "message": "创建成功"}
    finally:
        session.close()


# ===================== 菜单管理 =====================

@router.get("/menus")
def list_menus(current_user: User = Depends(get_current_user)):
    session = get_session()
    try:
        menus = session.query(Menu).order_by(Menu.sort).all()
        tree = _build_tree(menus)
        return {"code": 200, "data": tree}
    finally:
        session.close()


@router.post("/menus")
def create_menu(data: MenuCreate, current_user: User = Depends(get_current_user)):
    session = get_session()
    try:
        menu = Menu(**data.model_dump())
        session.add(menu)
        session.commit()
        return {"code": 200, "message": "创建成功", "data": {"id": menu.id}}
    finally:
        session.close()


@router.put("/menus/{menu_id}")
def update_menu(menu_id: int, data: MenuCreate, current_user: User = Depends(get_current_user)):
    session = get_session()
    try:
        menu = session.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(404, detail="菜单不存在")
        for k, v in data.model_dump().items():
            setattr(menu, k, v)
        session.commit()
        return {"code": 200, "message": "更新成功"}
    finally:
        session.close()


@router.delete("/menus/{menu_id}")
def delete_menu(menu_id: int, current_user: User = Depends(get_current_user)):
    session = get_session()
    try:
        # 检查是否有子菜单
        if session.query(Menu).filter(Menu.parent_id == menu_id).first():
            raise HTTPException(400, detail="存在子菜单，不能删除")
        menu = session.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(404, detail="菜单不存在")
        session.delete(menu)
        session.commit()
        return {"code": 200, "message": "删除成功"}
    finally:
        session.close()


# ===================== 字典管理 =====================

@router.get("/dict/types")
def list_dict_types(page: int = 1, size: int = 20, current_user: User = Depends(get_current_user)):
    session = get_session()
    try:
        total = session.query(func.count(DictType.id)).scalar() or 0
        items = session.query(DictType).offset((page - 1) * size).limit(size).all()
        return {"code": 200, "data": {
            "total": total,
            "list": [{"id": d.id, "name": d.name, "code": d.code, "status": d.status, "remark": d.remark,
                      "created_at": d.created_at.isoformat() if d.created_at else ''} for d in items]
        }}
    finally:
        session.close()


@router.get("/dict/data/{dict_code}")
def list_dict_data(dict_code: str, current_user: User = Depends(get_current_user)):
    session = get_session()
    try:
        items = session.query(DictData).filter(
            DictData.dict_code == dict_code, DictData.status == True
        ).order_by(DictData.sort).all()
        return {"code": 200, "data": [{
            "id": d.id, "label": d.label, "value": d.value,
            "tag_type": d.tag_type, "sort": d.sort
        } for d in items]}
    finally:
        session.close()


# ===================== 日志管理 =====================

@router.get("/logs/login")
def list_login_logs(page: int = 1, size: int = 20, current_user: User = Depends(get_current_user)):
    session = get_session()
    try:
        total = session.query(func.count(LoginLog.id)).scalar() or 0
        items = session.query(LoginLog).order_by(LoginLog.id.desc()).offset((page - 1) * size).limit(size).all()
        return {"code": 200, "data": {
            "total": total,
            "list": [{"id": l.id, "username": l.username, "status": l.status, "ip": l.ip,
                      "message": l.message, "created_at": l.created_at.isoformat() if l.created_at else ''}
                     for l in items]
        }}
    finally:
        session.close()


@router.get("/logs/operation")
def list_operation_logs(page: int = 1, size: int = 20, current_user: User = Depends(get_current_user)):
    session = get_session()
    try:
        total = session.query(func.count(OperationLog.id)).scalar() or 0
        items = session.query(OperationLog).order_by(OperationLog.id.desc()).offset((page - 1) * size).limit(size).all()
        return {"code": 200, "data": {
            "total": total,
            "list": [{"id": l.id, "username": l.username, "module": l.module, "action": l.action,
                      "method": l.method, "url": l.url, "ip": l.ip,
                      "result": l.result, "cost_time": l.cost_time,
                      "created_at": l.created_at.isoformat() if l.created_at else ''}
                     for l in items]
        }}
    finally:
        session.close()


# ===================== 系统监控 =====================

@router.get("/monitor")
def system_monitor(current_user: User = Depends(get_current_user)):
    """系统监控信息"""
    import psutil, platform
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        boot_time = datetime.fromtimestamp(psutil.boot_time())

        return {"code": 200, "data": {
            "os": platform.system() + " " + platform.release(),
            "hostname": platform.node(),
            "cpu": {
                "cores": psutil.cpu_count(logical=True),
                "physical_cores": psutil.cpu_count(logical=False),
                "percent": cpu_percent,
            },
            "memory": {
                "total": memory.total,
                "used": memory.used,
                "percent": memory.percent,
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "percent": disk.percent,
            },
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
            "python_version": platform.python_version(),
        }}
    except ImportError:
        return {"code": 200, "data": {"message": "请安装 psutil: pip install psutil"}}


# ===================== 工具函数 =====================

def _build_tree(items, parent_id=0):
    """构建菜单树"""
    tree = []
    for item in items:
        if item.parent_id == parent_id:
            children = _build_tree(items, item.id)
            tree.append({
                "id": item.id, "parent_id": item.parent_id,
                "name": item.name, "path": item.path,
                "component": item.component, "permission": item.permission,
                "icon": item.icon, "type": item.type, "sort": item.sort,
                "status": item.status, "hidden": item.hidden,
                "children": children,
            })
    return sorted(tree, key=lambda x: x['sort'])
