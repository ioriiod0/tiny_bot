# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    bot.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ioriiod0 <ioriiod0@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/01/08 19:17:06 by ioriiod0          #+#    #+#              #
#    Updated: 2019/01/10 20:35:51 by ioriiod0         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from typing import Type, Dict, List, Union, Any, Optional, Callable, Tuple
from functools import wraps
from .tracker import Tracker
from .policy import Policy
from .nlu import NLU
from .action import Action, ActionHub
from .types import Request, Response


class IententNotFound(Exception):
    pass


class Intent(object):
    def __init__(self, name, auto_fill=True, **kwargs):
        self.name = name
        self.auto_fill = auto_fill
        self.__dict__.update(kwargs)

    def __str__(self):
        return '<intent:%s>' % self.name


def create_action(_actions):
    if isinstance(_actions, ActionHub):
        return _actions
    elif callable(_actions):
        return _actions()
    else:
        raise Exception("unkown action type,%s" % type(_actions))


def create_intents(_intents):
    intents = {}
    for x in _intents:
        if isinstance(x, str):
            x = Intent(x)
        elif isinstance(x, dict):
            x = Intent(**x)
        elif isinstance(x, Intent):
            pass
        else:
            raise Exception("unkown intent type,%s" % type(x))
        intents[x.name] = x
    return intents


def create_tracker(_tracker):
    assert isinstance(_tracker, type)
    return _tracker


def create_policies(_policies):
    policies = []
    for p in _policies:
        if isinstance(p, Policy):
            pass
        elif callable(p):
            p = p()
        else:
            raise Exception("unkown policy type,%s" % type(p))
        policies.append(p)
    return p


def create_nul(_nlu):
    if isinstance(_nlu, NLU):
        return _nlu
    elif callable(_nlu):
        return _nlu()
    else:
        raise Exception("unkown nlu type,%s" % type(_nlu))


class BotMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Bot':
            return type.__new__(cls, name, bases, attrs)
        assert "__domain__" in attrs

        attrs["intents"] = create_intents(attrs['INTENT'])
        attrs["nlu"] = create_nlu(attrs['NLU'])
        attrs["tracker"] = create_tracker(attrs['TRACKER'])
        attrs["policies"] = create_policies(attrs['POLICIES'])
        attrs["actions"] = create_actions(attrs['ACTIONS'])

        for com in ["NLU", "ACTIONS", "INTENTS", "TRACKER", "POLICIES"]:
            attrs.pop(com)

        return type.__new__(cls, name, bases, attrs)


def auto_fill(entities: List[Dict], traker: Type[Tracker]):
    for entity in entities:
        name = entity['entity']
        if name in tracker:
            tracker[name] = e['value']


class Bot(object, metaclass=BotMetaclass):
    def __init__(self):
        super(Bot, self).__init__()
        self._before_request = None
        self._after_request = None
        self._before_action = None
        self._after_action = None
        self._exception_handlers = {}

    def before_request(self, f: Callable[[Type[Tracker], Type[Request]], Type[Request]]):
        self._before_request = f
        return f

    def before_request(self, f: Callable[[Type[Tracker], Type[Request]], Type[Request]]):
        self._after_request = f
        return f

    def before_action(self, f: Callable[[Type[Action], Type[Tracker], Type[Request]], None]):
        self._before_action = f
        return f

    def after_action(self, f: Callable[[Type[Action], Type[Tracker], Type[Request]], None]):
        self._after_action = f
        return f

    def catch(self, exception: Type[Exception]):
        def _(f: Callable[[Type[Tracker], Type[Request]], Type[Response]]):
            self._exception_handlers[exception] = f
            return f
        return _

    def __str__(self):
        return "<bot: %s>" % self.__domain__

    def handle_msg(self, msg: Union[str, Request], sender_id: str) -> List[Response]:
        if isinstance(msg, str):
            msg = Request(body=msg)
        tracker = self.tracker.get(sender_id)
        try:
            return self._handle_msg(tracker, msg)
        except Exception as e:
            t = type(e)
            h = self._exception_handlers.get(t)
            if h:
                return [h(tracker, msg)]
            else:
                raise e

    def _handle_msg(self, tracker: Type[Tracker], msg: Union[str, Request]) -> List[Response]:
        if not msg.intent:
            msg = self.nlu(self, tracker, msg)

        if self._before_request:
            msg = self._before_request(self, tracker, msg)

        intent_attrs = self.intents.get(msg.intent['name'])
        if not intent_attrs:
            raise IententNotFound("intent not found for %s" % msg.intent)

        if intent_attrs.auto_fill:
            auto_fill(msg.entities, tracker)

        acts, timeout = [], None
        for policy in self.policies:
            acts, timeout = policy(self, tracker, msg)
            if acts:
                break
        else:
            raise Exception('msg can not be handled!', msg)

        resps = self._run_actions(tracker, acts, msg)
        # update leatest_msg & leatest_resps
        tracker.latest_message = msg
        tracker.latest_replies = resps
        # only log action generated by policy..
        tracker.latest_action_name = acts[-1]

        if self._after_request:
            resps = self._after_request(self, tracker, resps)

        tracker.save(timeout)

        return resps

    def _run_actions(self, tracker: Union[Type[Tracker], str], acts: List[str], msg: Type[Request]) -> List[Response]:
        if isinstance(tracker, str):
            tracker = self.tracker.get(tracker)
        l = []
        for act in acts:
            ret = self.execute_action(act, tracker, msg)
            if ret is None:
                continue
            l.append(ret)
        return ret

    def execute_action(self, act: str, tracker: Union[Type[Tracker], str], msg: Type[Request]) -> Optional[Response]:
        action = self.actions[act]
        if isinstance(sender, str):
            tracker = self.tracker.get(tracker)
        return action(self, tracker, msg)
