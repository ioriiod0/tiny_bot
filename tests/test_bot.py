
import pytest
from tiny_bot import *


def test_basic_bot():

    store = RedisStore("test", "redis://localhost:6379/0")

    class MyTracker(store.Tracker):
        __domain__ = "test"
        a = StringField(default="aaa")
        b = IntegerField(default=0)
        c = ListField()
        d = DictField()

    def func(bot, tracker, msg):
        return Response("world")

    class MyAction(Action):
        def run(self, bot, tracker, msg):
            return Response("hello")

    class MyActionHub(ActionHub):
        f = func
        g = MyAction("g")
        h = "hello world!"

    class MyBot(Bot):
        __domain__ = "test"
        TRACKER = MyTracker
        ACTIONS = MyActionHub
        INTENTS = ['A', 'B', 'C']
        NLU = xx
        POLICYS = [XXX, XX]

    bot = Bot()
