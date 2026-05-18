"""JWT 认证中间件"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from security import decode_access_token
from database import get_session
from models.user import User

security_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> User:
    """获取当前登录用户"""
    if credentials is None:
        raise HTTPException(status_code=401, detail="未登录")

    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token无效或已过期")

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token无效")

    session = get_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user is None or not user.status:
            raise HTTPException(status_code=401, detail="用户不存在或已禁用")
        return user
    finally:
        session.close()
