
import pytest
from tiny_bot import *


def test_basic_bot():
    pass

    # def some_action(bot, tracker, msg):
    #     ...

    # class MyAction(Action):
    #     def run(self, bot, tracker, msg):
    #         ...

    # store = RedisStore("test", "redis://localhost:6379/0")

    # class MyTracker(store.Tracker):
    #     __domain__ = "test"
    #     a = StringField(default="aaa")
    #     b = IntegerField(default=0)
    #     c = ListField()
    #     d = DictField()

    # class MyActionHub(ActionHub):
    #     a = some_action
    #     b = MyAction()
    #     c = "hello world!"  # utter template action

    # class MyPolicy(Policy):
    #     def predict(self, tracker, msg):
    #         ...

    # class MyNLU(NLU):
    #     def parse(self, tracker, msg):
    #         ...

    # class MyBot(Bot):
    #     __domain__ = "test"
    #     TRACKER = MyTracker
    #     ACTIONS = MyActionHub
    #     INTENTS = ['E', 'F', 'G']
    #     NLU = MyNLU
    #     POLICYS = [MyPolicy]

    # bot = MyBot()
    # app = create_flask_app(bot, endpoint="/api/handle_msg")
