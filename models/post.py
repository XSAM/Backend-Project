from models import Mongo
from utils import (
    encode_with_utf8,
    decode_with_utf8,
)
import time
from models.user import User


class Post(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('user_id', int, -1),
        ('content', str, ''),
        ('refer_post_id', int, -1),
    ]

    def ct(self):
        value = time.localtime(self.created_time)
        dt = '{}月{}日 {}:{}'.format(value.tm_mon, value.tm_mday, value.tm_hour, value.tm_min)
        return dt

    def set_attr_by_refer_post(self):
        if self.refer_post_id != -1:
            tmp_post = Post().find_one(id=self.refer_post_id)
            if tmp_post is not None:
                self.refer_post = tmp_post
                self.refer_user = User().find_one(id=tmp_post.user_id)
            else:
                self.refer_post_id = -1

    def user(self):
        u = User.find_one(id=self.user_id)
        return u


if __name__ == '__main__':
    # Post().new({
    #     'user_id': 6,
    #     'content': '测试',
    # })
    # Post().new({
    #     'user_id': 6,
    #     'content': '测试2',
    #     'refer_post_id': 1,
    # })
    # print(Post().find_all(user_id=6))
    post = Post.find_one(id=1)
    print(post.ct())