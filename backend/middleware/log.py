"""操作日志装饰器"""
import time
import traceback
from functools import wraps
from database import get_session
from models.system import OperationLog


def log_operation(module: str, action: str):
    """操作日志装饰器

    用法:
        @router.post('/users')
        @log_operation('用户管理', '新增')
        def create_user(...):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.time()
            request = kwargs.get('request')
            try:
                result = await func(*args, **kwargs)
                cost = int((time.time() - start) * 1000)
                _save_log(request, module, action, 'success', cost)
                return result
            except Exception as e:
                cost = int((time.time() - start) * 1000)
                _save_log(request, module, action, 'fail', cost, str(e))
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.time()
            request = kwargs.get('request')
            try:
                result = func(*args, **kwargs)
                cost = int((time.time() - start) * 1000)
                _save_log(request, module, action, 'success', cost)
                return result
            except Exception as e:
                cost = int((time.time() - start) * 1000)
                _save_log(request, module, action, 'fail', cost, str(e))
                raise

        if hasattr(func, '__await__'):
            return async_wrapper
        return sync_wrapper
    return decorator


def _save_log(request, module, action, result, cost, error_msg=''):
    """异步保存操作日志"""
    try:
        session = get_session()
        log = OperationLog(
            username=getattr(request.state, 'username', '') if hasattr(request, 'state') else '',
            module=module,
            action=action,
            method=request.method if request else '',
            url=str(request.url) if request else '',
            ip=request.client.host if request and request.client else '',
            params=str(dict(request.query_params)) if request else '',
            result=result,
            cost_time=cost,
            error_msg=error_msg,
        )
        session.add(log)
        session.commit()
        session.close()
    except Exception:
        pass
