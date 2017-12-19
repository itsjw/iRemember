from flask import session, g, url_for, redirect
from  config import DevConfig
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if DevConfig.CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))

    return wrapper
