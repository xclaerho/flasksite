from flask import session, redirect, url_for, flash
from functools import wraps

def login_required(f):
    """ Decorator for routes that need a user to be logged in """
    @wraps(f)
    def decorated_fuction(*args, **kwargs):
        if not session.get('username', None):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_fuction

def requires_one_of_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
                if not session.get('roles', None):
                    # user not logged in
                    return redirect(url_for('login'))
                for role in roles:
                    if role in session.get('roles'):
                        return f(*args, **kwargs)
                flash('Niet toegestaan.', category="primary")
                return redirect(url_for('home'))
        return wrapped
    return wrapper