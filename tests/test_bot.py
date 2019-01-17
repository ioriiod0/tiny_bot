
import pytest
from tiny_bot import *


class Error1(Exception):
    pass


class Error2(Exception):
    pass


class Error3(Exception):
    pass


store = RedisStore("test", "redis://localhost:6379/0")


@pytest.fixture
def bot():

    def raisefunc1(bot, tracker, msg):
        raise Error1("error1")

    def raisefunc2(bot, tracker, msg):
        raise Error2("error2")

    def raisefunc3(bot, tracker, msg):
        raise Error3("error3")

    class QueryAction(Action):
        def run(self, bot, tracker, msg):
            result = "从<%s>邮寄到<%s>,重量:<%s>,时间:<%s> 不要钱,哈哈！" % (
                tracker._from, tracker.to, tracker.weight, tracker.time)
            return Response(result)

    class MyTracker(store.Tracker):
        __domain__ = "price_time_bot"
        _from = StringField()
        to = StringField()
        weight = FloatField()
        time = StringField()

    class MyActionHub(ActionHub):
        query = QueryAction()
        utter_bye = ['再见', 'bye', '滚蛋']  # utter template action
        utter_greeting = ['你好', '小垃圾,咋了？']
        utter_ask__from = "从哪邮寄？"
        utter_ask_to = ['要邮寄到哪？']
        utter_ask_weight = "多重？"
        utter_ask_time = "什么时候邮寄？"

        raise1 = raisefunc1
        raise2 = raisefunc2
        raise3 = raisefunc3

    class MyPolicy(Policy):
        def predict(self, bot, tracker, msg):
            if msg.intent == "bye":
                return ['utter_bye'], 0
            elif msg.intent == "greeting":
                return ['utter_greeting'], None

            elif msg.intent == "raise1":
                raise Error1('error1')

            elif msg.intent == "raise2":
                return ['raise2'], 100

            elif msg.intent == "raise3":
                return ['raise3'], 100

            elif msg.intent in ("query", "inform"):
                for slot in ['_from', 'to', 'weight', 'time']:
                    print("slot:", slot, tracker[slot])
                    if tracker[slot] is None:
                        return ['utter_ask_%s' % slot], 100
                return ['query', 'utter_bye'], 1
            else:
                raise Exception("should never happened!")

    class MyNLU(NLU):
        def parse(self, bot, tracker, msg):
            return msg

    class MyBot(Bot):
        __domain__ = "test"
        TRACKER = MyTracker
        ACTIONS = MyActionHub
        INTENTS = ["query", "inform", Intent("greeting", auto_fill=False),
                   "bye", "raise1", "raise2", "raise3"]
        NLU = MyNLU
        POLICIES = [MyPolicy]

    bot = MyBot()
    return bot


def test_greeting(bot):
    res = bot.handle_msg(Request(body="", intent="greeting"), "1111")
    assert len(res) == 1 and res[0].body in ['你好', '小垃圾,咋了？']
    assert store._redis.get("price_time_bot:1111") is not None


def test_bye(bot):
    res = bot.handle_msg(Request(body="", intent="bye"), "1111")
    assert len(res) == 1 and res[0].body in ['再见', 'bye', '滚蛋']
    assert store._redis.get("price_time_bot:1111") is None


def test_query_autofill(bot):
    import time
    entities = [
        {'entity': '_from', 'value': '北京'},
        {'entity': 'to', 'value': '上海'},
        {'entity': 'weight', 'value': 12.0},
        {'entity': 'time', 'value': "今天"}
    ]

    res = bot.handle_msg(
        Request(body="", intent="query", entities=entities), "1111")
    assert res[0].body == "从<北京>邮寄到<上海>,重量:<12.0>,时间:<今天> 不要钱,哈哈！"
    print(res)
    assert len(res) == 2 and res[1].body in ['再见', 'bye', '滚蛋']
    assert store._redis.get("price_time_bot:1111") is not None
    time.sleep(1.1)
    assert store._redis.get("price_time_bot:1111") is None


def test_inform(bot):
    _from = [
        {'entity': '_from', 'value': '北京'},
    ]
    to = [
        {'entity': 'to', 'value': '上海'},
    ]
    weight = [
        {'entity': 'weight', 'value': 12.0},
    ]
    time = [
        {'entity': 'time', 'value': "今天"},
    ]

    res = bot.handle_msg(
        Request(body="", intent="query", entities=_from+to), "1111")
    assert len(res) == 1 and res[0].body == "多重？"
    res = bot.handle_msg(
        Request(body="", intent="query", entities=weight), "1111")
    assert len(res) == 1 and res[0].body == "什么时候邮寄？"
    res = bot.handle_msg(
        Request(body="", intent="query", entities=time), "1111")
    assert len(res) == 2 and res[1].body in ['再见', 'bye', '滚蛋']
    assert res[0].body == "从<北京>邮寄到<上海>,重量:<12.0>,时间:<今天> 不要钱,哈哈！"


def test_exception_hook(bot):

    @bot.catch(Error1)
    def catch1(tracker, req):
        return Response("catch1")

    @bot.catch((Error1, Error2))
    def catch1(tracker, req):
        return Response("catch2")

    res = bot.handle_msg(Request(body="", intent="raise1"), "1111")
    assert res[0].body == "catch1"

    res = bot.handle_msg(Request(body="", intent="raise2"), "1111")
    assert res[0].body == "catch2"

    with pytest.raises(Error3):
        res = bot.handle_msg(Request(body="", intent="raise3"), "1111")


def test_exception_hook(bot):

    @bot.catch(Error1)
    def catch1(tracker, req):
        return Response("catch1")

    @bot.catch((Error1, Error2))
    def catch1(tracker, req):
        return Response("catch2")

    res = bot.handle_msg(Request(body="", intent="raise1"), "1111")
    assert res[0].body == "catch1"

    res = bot.handle_msg(Request(body="", intent="raise2"), "1111")
    assert res[0].body == "catch2"

    res = bot.handle_msg(Request(body="", intent="raise3"), "1111")
    assert res[0].body == "an error occurred..."


def test_hook(bot):

    flags = []

    @bot.before_request
    def before_request(tracker, req):
        assert req.body == "你好"
        flags.append("a")
        return req

    @bot.after_request
    def after_request(tracker, res):
        assert res[0].body in ['你好', '小垃圾,咋了？']
        flags.append("b")
        return res

    @bot.before_action
    def before_acton(act, tracker, req):
        assert req.body == "你好"
        assert act.name == "utter_greeting"
        flags.append("c")

    @bot.after_action
    def after_action(act, tracker, req):
        assert req.body == "你好"
        assert act.name == "utter_greeting"
        flags.append("d")

    res = bot.handle_msg(Request(body="你好", intent="greeting"), "1111")
    assert len(res) == 1 and res[0].body in ['你好', '小垃圾,咋了？']
    assert flags == ['a', 'c', 'd', 'b']


def test_plugin(bot):

    class Logger(object):
        def __init__(self, bot):

            @bot.before_request
            def before_request(tracker, req):
                print(req)
                return req

            @bot.after_request
            def after_request(tracker, res):
                print(res)
                return res

    class UnAuthed(Exception):
        pass

    class Auth(object):
        def __init__(self, bot):

            @bot.before_request
            def before_request(tracker, req):
                if req.apikey != "aaabbbccc":
                    raise UnAuthed("api key required!")
                return req

            @bot.catch(UnAuthed)
            def catch(tracker, req):
                return Response("please login first")

    logger = Logger(bot)
    auth = Auth(bot)

    res = bot.handle_msg(
        Request(body="你好", intent="greeting", apikey="111111"), "1111")
    assert len(res) == 1 and res[0].body == "please login first"
