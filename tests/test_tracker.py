#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tiny_bot` package."""


import pytest
from tiny_bot import *


def test_basic_tracker():

    class MyTracker(Tracker):
        __domain__ = "test"
        a = StringField(default="aaa")
        b = IntegerField(default=0)
        c = ListField()
        d = DictField()
        e = IntegerField()

    x = MyTracker()
    assert x.a == "aaa"
    assert x.b == 0
    assert x.c == []
    assert x.d == {}
    assert x.e == None
    x.e = 10
    assert x.e == 10

    assert x['a'] == "aaa"
    x['a'] = "bbb"
    assert x['a'] == "bbb"

    x.c.append(1)
    assert x.c == [1]

    x.a = "bbb"
    assert x.a == "bbb"

    with pytest.raises(KeyError):
        x.f = 123

    with pytest.raises(KeyError):
        print(x.sss)

    with pytest.raises(TypeError):
        x.b = "ssdfdsf"

    assert "a" in x
    assert "f" not in x

    assert x.__domain__ == "test"


def test_redis_tracker():
    store = RedisStore("test", "redis://localhost:6379/0")

    class MyTracker(store.Tracker):
        __domain__ = "test"
        a = StringField(default="aaa")
        b = IntegerField(default=0)
        c = ListField()
        d = DictField()

    assert MyTracker.gen_key("abc") == "test:abc"

    x = MyTracker(sender_id="111")
    x.b = 10
    x.c.append("xxx")
    x.d['a'] = "a"
    x.a = 'a'
    x.save()

    y = MyTracker.get("111")
    assert x.a == y.a
    assert x.b == y.b
    assert x.c == y.c
    assert x.d == y.d
