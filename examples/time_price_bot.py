from tiny_bot import *

store = RedisStore("test", "redis://localhost:6379/0")


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
    # utter template action , will trandom choose a reply
    utter_bye = ['再见', 'bye', '滚蛋']
    utter_greeting = ['你好', '小垃圾,咋了？']
    utter_ask__from = "从哪邮寄？"
    utter_ask_to = ['要邮寄到哪？']
    utter_ask_weight = "多重？"
    utter_ask_time = "什么时候邮寄？"


class MyPolicy(Policy):
    def predict(self, bot, tracker, msg):
        if msg.intent == "bye":
            return ['utter_bye'], 0
        elif msg.intent == "greeting":
            return ['utter_greeting'], None
        elif msg.intent in ("query", "inform"):
            for slot in ['_from', 'to', 'weight', 'time']:
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
    INTENTS = ["query", "inform", "greeting", "bye"]
    NLU = MyNLU
    POLICIES = [MyPolicy]


if __name__ == '__main__':
    bot = MyBot()

    class Error1(Exception):
        pass

    class Error2(Exception):
        pass

    class Error3(Exception):
        pass

    @bot.catch(Error1)
    def catch1(tracker, req):
        return Response("catch1")

    @bot.catch((Error1, Error2))
    def catch1(tracker, req):
        return Response("catch2")

    @bot.before_request
    def before_request(tracker, req):
        print("before_request", req)
        return req

    @bot.after_request
    def after_request(tracker, res):
        print("after_request", res)
        return res

    @bot.before_action
    def before_acton(act, tracker, req):
        print("before_acton", act)

    @bot.after_action
    def after_action(act, tracker, req):
        print("after_action", act)

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
        Request(body="", intent="inform", entities=weight), "1111")
    assert len(res) == 1 and res[0].body == "什么时候邮寄？"
    res = bot.handle_msg(
        Request(body="", intent="inform", entities=time), "1111")
    assert len(res) == 2 and res[1].body in ['再见', 'bye', '滚蛋']
    assert res[0].body == "从<北京>邮寄到<上海>,重量:<12.0>,时间:<今天> 不要钱,哈哈！"
