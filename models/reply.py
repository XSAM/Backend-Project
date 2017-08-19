from models import Mongo
from utils import (
    encode_with_utf8,
    decode_with_utf8,
)
import time


class Reply(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('user_id', int, -1),
        ('post_id', int, -1),
        ('content', str, ''),
    ]

    def ct(self):
        value = time.localtime(self.created_time)
        dt = '{}月{}日 {}:{}'.format(value.tm_mon, value.tm_mday, value.tm_hour, value.tm_min)
        return dt


if __name__ == '__main__':
    Reply().new({
        'user_id': 6,
        'post_id': 1,
        'content': '评论1',
    })
    print(Reply().find_all(post_id=1))