import time
from pymongo import MongoClient
client = MongoClient()


def timestamp():
    return int(time.time())


def next_id(name):
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1,
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    # 存储数据的 id
    doc = client.todo['data_id']
    # find_and_modify 是一个原子操作函数
    new_id = doc.find_and_modify(**kwargs).get('seq')
    return new_id


class Mongo(object):
    __fields__ = [
        '_id',
        ('id', int, -1),
        ('type', str, ''),
        ('deleted', bool, False),
        ('created_time', int, 0),
        ('updated_time', int, 0),
    ]

    @classmethod
    def has(cls, **kwargs):
        return cls.find_one(**kwargs) is not None

    @classmethod
    def new(cls, form=None, **kwargs):
        name = cls.__name__
        m = cls()
        fields = cls.__fields__.copy()
        fields.remove('_id')
        if form is None:
            form = {}

        for f in fields:
            k, t, v = f
            if k in form:
                # format value by type
                setattr(m, k, t(form[k]))
            else:
                # set default value
                setattr(m, k, v)
        # handle additional kwargs
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        # write in db
        m.id = next_id(name)
        current_time = timestamp()
        m.created_time = current_time
        m.updated_time = current_time
        m.type = name
        m.save()
        return m

    @classmethod
    def all(cls):
        return cls._find()

    @classmethod
    def _find(cls, **kwargs):
        name = cls.__name__

        # 过滤被删除的数据
        deleted = kwargs.get('deleted', False)
        if deleted is True:
            kwargs.pop('deleted')
        else:
            kwargs['deleted'] = False

        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        ds = client.todo[name].find(kwargs)
        if sort is not None:
            ds = ds.sort(sort)
        l = [cls._new_with_bson(d) for d in ds]
        return l

    @classmethod
    def _new_with_bson(cls, bson):
        """
        这是给内部 all 这种函数使用的函数
        从 mongo 数据中恢复一个 model
        """
        m = cls()
        fields = cls.__fields__.copy()
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                # 设置默认值
                setattr(m, k, v)
        # 这一句必不可少，否则 bson 生成一个新的_id
        setattr(m, '_id', bson['_id'])
        return m

    @classmethod
    def find_one(cls, **kwargs):
        l = cls._find(**kwargs)
        if len(l) > 0:
            return l[0]
        else:
            return None

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def get(cls, id):
        return cls.find_one(id=id)

    def update(self, form, force=False):
        for k, v in form.items():
            if force or hasattr(self, k):
                setattr(self, k, v)
        self.updated_time = timestamp()
        self.save()

    def save(self):
        name = self.__class__.__name__
        print('** save:', self.__dict__)
        # deprecated, but easy to use
        client.todo[name].save(self.__dict__)

    def delete(self):
        print('deleted')
        name = self.__class__.__name__
        query = {
            'id': self.id,
        }
        values = {
            '$set': {
                'deleted': True,
            }
        }
        client.todo[name].update_one(query, values)

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    def ct(self):
        format = '%H:%M:%S'
        value = time.localtime(self.created_time)
        dt = time.strftime(format, value)
        return dt

    def ut(self):
        format = '%H:%M:%S'
        value = time.localtime(self.updated_time)
        dt = time.strftime(format, value)
        return dt

if __name__ == '__main__':
    # model = Mongo().new()

    print(Mongo()._find(**{
        'deleted': True
    }))