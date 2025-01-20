from functools import wraps
from flask import abort
from flask_login import current_user


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.role != "admin":
            abort(403)
        return func(*args, **kwargs)

    return decorated_function
