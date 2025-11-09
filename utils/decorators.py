from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("You need to log in to access this page.", "warning")
                return redirect(url_for('routes.login_page'))
            if current_user.role != role:
                flash("You do not have the required permissions to access this page.", "danger")
                return redirect(url_for('routes.home_page'))
            return func(*args, **kwargs)
        return wrapped
    return decorator
