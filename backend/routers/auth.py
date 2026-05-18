"""认证路由: 登录/注册/用户信息"""
from fastapi import APIRouter, Depends, HTTPException, Request
from database import get_session
from models.user import User, Role, Menu, role_menu
from models.system import LoginLog
from schemas.user import LoginRequest, UserInfo
from security import verify_password, hash_password, create_access_token
from middleware.auth import get_current_user
from sqlalchemy import func
from datetime import datetime, timezone

router = APIRouter(prefix="/api/auth", tags=["认证管理"])


@router.post("/login")
def login(req: LoginRequest, request: Request):
    """用户登录"""
    session = get_session()
    try:
        user = session.query(User).filter(User.username == req.username).first()
        if not user or not verify_password(req.password, user.password):
            # 记录失败日志
            _log = LoginLog(username=req.username, status='fail', message='用户名或密码错误')
            session.add(_log)
            session.commit()
            raise HTTPException(status_code=400, detail="用户名或密码错误")

        if not user.status:
            raise HTTPException(status_code=400, detail="账户已禁用")

        # 更新最后登录时间
        user.last_login_at = datetime.now(timezone.utc)
        # 记录成功日志
        ip = request.client.host if request.client else ''
        _log = LoginLog(username=req.username, status='success', ip=ip, message='登录成功')
        session.add(_log)
        session.commit()

        token = create_access_token({"user_id": user.id, "username": user.username})
        return {
            "code": 200,
            "data": {
                "token": token,
                "user": _user_to_info(user, session)
            }
        }
    finally:
        session.close()


@router.get("/userinfo")
def get_userinfo(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    session = get_session()
    try:
        # 重新查询用户（避免 detached 错误）
        user = session.query(User).filter(User.id == current_user.id).first()
        return {"code": 200, "data": _user_to_info(user, session)}
    finally:
        session.close()


@router.get("/menus")
def get_user_menus(current_user: User = Depends(get_current_user)):
    """获取当前用户菜单树"""
    session = get_session()
    try:
        # 重新查询用户
        user = session.query(User).filter(User.id == current_user.id).first()
        if user.is_admin:
            menus = session.query(Menu).filter(
                Menu.status == True, Menu.hidden == False
            ).order_by(Menu.sort).all()
        else:
            menu_ids = session.query(role_menu.c.menu_id).join(
                Role, role_menu.c.role_id == Role.id
            ).join(
                User.roles
            ).filter(User.id == user.id).distinct()
            menus = session.query(Menu).filter(
                Menu.id.in_(menu_ids), Menu.status == True, Menu.hidden == False
            ).order_by(Menu.sort).all()

        tree = _build_menu_tree(menus)
        return {"code": 200, "data": tree}
    finally:
        session.close()


def _user_to_info(user: User, session) -> dict:
    """用户对象转信息"""
    roles = [r.code for r in user.roles]
    # 获取权限标识
    if user.is_admin:
        perms = ["*:*:*"]
    else:
        menu_ids = session.query(role_menu.c.menu_id).filter(
            role_menu.c.role_id.in_([r.id for r in user.roles])
        ).distinct()
        perms = [m.permission for m in session.query(Menu).filter(
            Menu.id.in_(menu_ids), Menu.permission != ''
        ).all()]

    return {
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "email": user.email,
        "phone": user.phone,
        "avatar": user.avatar,
        "status": user.status,
        "is_admin": user.is_admin,
        "roles": roles,
        "permissions": perms,
    }


def _build_menu_tree(menus, parent_id: int = 0) -> list:
    """构建菜单树"""
    tree = []
    for m in menus:
        if m.parent_id == parent_id:
            children = _build_menu_tree(menus, m.id)
            item = {
                "id": m.id,
                "parent_id": m.parent_id,
                "name": m.name,
                "path": m.path,
                "component": m.component,
                "permission": m.permission,
                "icon": m.icon,
                "type": m.type,
                "sort": m.sort,
                "hidden": m.hidden,
                "children": children,
            }
            tree.append(item)
    return sorted(tree, key=lambda x: x['sort'])
