from models import Mongo
from utils import (
    encode_with_utf8,
    decode_with_utf8,
    log,
)
import json
from models.RedisCache import RedisCache
from collections import defaultdict

def bool_true():
    return True


class Todo(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('user_id', int, -1),
        ('title', str, ''),
        ('completed', bool, False),
    ]
    should_update_all = True
    should_update_user_id = defaultdict(bool_true)
    cache_client = RedisCache()

    def to_json(self):
        d = dict()
        for k in Todo.__fields__:
            key = k[0]
            if not key.startswith('_'):
                d[key] = getattr(self, key)
        return json.dumps(d)

    @classmethod
    def from_json(cls, j):
        d = json.loads(j)

        instance = cls()
        for k, v in d.items():
            setattr(instance, k, v)
        return instance

    @classmethod
    def complete(cls, id, completed=True):
        """
        用法很方便
        Todo.complete(1)
        Todo.complete(2, False)
        """
        t = cls.find_one(id=id)
        t.completed = completed
        t.save()
        return t

    @classmethod
    def cache_all(cls):
        if Todo.should_update_all:
            log('*cache updated: todo all')
            Todo.cache_client.set('todo_all', json.dumps(
                [i.to_json() for i in cls.all()]
            ))
            Todo.should_update_all = False
        j = json.loads(Todo.cache_client.get('todo_all'))
        j = [Todo.from_json(i) for i in j]
        return j

    @classmethod
    def cache_by_user_id(cls, id):
        if Todo.should_update_user_id[id]:
            log('*cache updated: todo user_id')
            Todo.cache_client.set('todo_'+str(id), json.dumps(
                [i.to_json() for i in cls.find_all(user_id=id)]
            ))
            Todo.should_update_user_id[id] = False
        j = json.loads(Todo.cache_client.get('todo_'+str(id)))
        j = [Todo.from_json(i) for i in j]
        return j


if __name__ == '__main__':
    # todo = Todo().new({
    #     'user_id': 5,
    #     'title': '不该出现',
    # })
    # Todo.complete(todo.id)
    print(Todo.cache_by_user_id(4))
    print(Todo.cache_all())
    print(Todo.cache_all())