from flask import (
    session,
    url_for,
)

from models.user import User


class Valid(object):
    def __init__(self):
        self.is_user = False
        self.is_valid = False
        self.code = -1
        self.u = None
        self.page_header = None


class Head(object):
    def __init__(self, title, url):
        self.title = title
        self.url = url

csrf_token = dict()


def current_user():
    uid = session.get('user_id', -1)
    u = User.find_one(id=int(uid))
    return u


def validate_login_and_token(request):
    u = current_user()
    if u is None:
        return 403, u
    token = request.form.get('token', None)
    if token in csrf_token and csrf_token[token] == u.id:
        # FIXME csrf
        # csrf_token.pop(token)
        return 200, u
    else:
        return 403, u


def get_valid(request):
    code, u = validate_login_and_token(request)
    valid = Valid()
    valid.code = code
    if code == 200:
        valid.is_valid = True
    if u is not None:
        valid.is_user = True
        valid.page_header = (
            Head(u.username, url_for('index.index')),
            Head('登出', url_for('index.logout')),
        )
    else:
        valid.page_header = (
            Head('登录', url_for('index.login')),
            Head('注册', url_for('index.register')),
        )
    return valid
