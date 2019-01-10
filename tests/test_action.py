import pytest
from tiny_bot import *


def test_basic_action():
    def func(bot, tracker, msg):
        return Response("world")

    class MyAction(Action):
        def run(self, bot, tracker, msg):
            return Response("hello")

    class MyActionHub(ActionHub):
        f = func
        g = MyAction()
        h = "hello world!"

    hub = MyActionHub()
    assert isinstance(hub['f'], Action)
    assert isinstance(hub['g'], Action)
    assert isinstance(hub['h'], Action)

    class FakeBot(object):
        def __init__(self):
            self._before_action = None
            self._after_action = None

    bot = FakeBot()

    assert hub['f'](bot, {}, {}).body == "world"
    assert hub['g'](bot, {}, {}).body == "hello"
    assert hub['h'](bot, {}, {}).body == "hello world!"
