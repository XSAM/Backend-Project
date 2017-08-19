from models import Mongo
from utils import (
    encode_with_utf8,
    decode_with_utf8,
)


class User(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('user_image', str, 'default.png'),
    ]

    def __init__(self):
        self.user_image = 'default.png'

    @staticmethod
    def salt_password(password, salt='#!@<>Hi'):
        import hashlib

        def sha256(ascii_str):
            return hashlib.sha256(encode_with_utf8(ascii_str)).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) >= 5 and User.has(username=name) is False:
            pwd = User.salt_password(pwd)
            # form 是不可变对象，所以为了减少 save 次数，使用copy
            form = form.copy()
            form['password'] = pwd
            u = User.new(form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        u = User()
        u.username = form.get('username', '')
        u.password = form.get('password', '')
        user = User.find_one(username=u.username)
        if user is not None and user.password == User.salt_password(u.password):
            return user
        else:
            return None

if __name__ == '__main__':
    User().register({
        'username': 'test123',
        'password': 'sdfdf',
    })
    user = User().validate_login({
        'username': 'test123',
        'password': 'sdfdf',
    })
    print('user', user)
    user.update({
        'username': 'test456',
    })
    print('user', user)