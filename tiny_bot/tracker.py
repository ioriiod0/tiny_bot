# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tracker.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ioriiod0 <ioriiod0@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/01/07 16:43:18 by ioriiod0          #+#    #+#              #
#    Updated: 2019/01/11 20:02:19 by ioriiod0         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


from typing import Any, Type, Optional
import copy
import redis
from .fields import *

try:
    import cPickle as pickle
except:
    import pickle


class TrackerMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name in ('Tracker',):
            return type.__new__(cls, name, bases, attrs)

        mappings = {}

        assert "latest_action_name" not in attrs
        assert "latest_message" not in attrs
        assert "latest_replies" not in attrs
        assert "__domain__" in attrs

        # add default slots
        attrs['latest_action_name'] = StringField()
        attrs['latest_message'] = DictField()
        attrs['latest_replies'] = ListField()
        attrs['sender_id'] = StringField()

        for k, v in attrs.items():
            if isinstance(v, Field):
                v.name = k
                mappings[k] = v

        for k in mappings.keys():
            attrs.pop(k)

        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        ret = type.__new__(cls, name, bases, attrs)
        return ret


class Tracker(object, metaclass=TrackerMetaclass):
    def __init__(self, **kwargs):
        super(Tracker, self).__init__()

        tracker_slots = {}
        for k, v in self.__mappings__.items():
            if v.factory:
                tracker_slots[k] = v.factory()
            else:
                tracker_slots[k] = copy.deepcopy(v.default)

        object.__setattr__(self, "__tracker_slots__", tracker_slots)
        for k, v in kwargs.items():
            self[k] = v

    def __getitem__(self, key: str) -> Any:
        return self.__tracker_slots__[key]

    def __setitem__(self, key: str, value: Any):
        field = self.__mappings__.get(key)
        if not field:
            raise KeyError(
                r"'Tracker' object has no slot '%s'" % key)

        if not isinstance(value, field.type) and value is not None:
            raise TypeError('%s required,but got %s' %
                            (field.type, type(value)))

        if field.validator and not field.validator(value):
            raise ValidateError(
                'validate error with vaule:%s, field:%s' % (value, field))

        self.__tracker_slots__[key] = value

    def __getattr__(self, k: str) -> Any:
        return self[k]

    def __setattr__(self, k: str, value: Any):
        self[k] = value

    def __contains__(self, k: str):
        return k in self.__tracker_slots__

    def __str__(self):
        return str(self.__tracker_slots__)

    def _as_dict(self):
        return self.__tracker_slots__


class RedisStore(object):
    def __init__(self, domain, redis_uri, db=None, **kwargs):
        super(RedisStore, self).__init__()
        _redis = redis.Redis.from_url(
            redis_uri, db=db, **kwargs)
        self._redis = _redis

        class _Tracker(Tracker):
            __domain__ = domain

            def serialize(self) -> bytes:
                return pickle.dumps(self.__tracker_slots__)

            @classmethod
            def deserialize(cls, value: bytes) -> Type[Tracker]:
                return cls(**pickle.loads(value))

            @classmethod
            def get(cls, sender_id: str) -> Type[Tracker]:
                key = cls.gen_key(sender_id)
                body = _redis.get(key)
                if body is None:
                    ret = cls(sender_id=sender_id)
                    return ret
                return cls.deserialize(body)

            @classmethod
            def gen_key(cls, key: str):
                return "%s:%s" % (cls.__domain__, key)

            def save(self, expire: Optional[int] = None):
                body = self.serialize()
                key = self.__class__.gen_key(self.sender_id)
                _redis.set(key, body)
                if expire is not None:
                    _redis.expire(key, expire)

            @classmethod
            def delete(cls, sender_id: str):
                key = cls.gen_key(sender_id)
                _redis.delete(key)

        self.Tracker = _Tracker
