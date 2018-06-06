"""User authorization decorators"""

from functools import wraps

from flask import flash, redirect
from flask_login import current_user


def anonymous_required(url='/'):
    """
    Redirect a user to a specified location if they are already signed in.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated:
                return redirect(url)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def roles_required(*roles):
    """
    Require that the user's role match one or more roles to access a page
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                flash('Page not authorized.', 'error')
                return redirect('/')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
