from functools import wraps
from flask_login import current_user
from flask import abort, render_template

def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if current_user.role not in roles:
                abort(403)

            return f(*args, **kwargs)

        return decorator

    return wrapper