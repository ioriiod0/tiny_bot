# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    types.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ioriiod0 <ioriiod0@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/01/10 14:46:03 by ioriiod0          #+#    #+#              #
#    Updated: 2019/01/11 20:06:26 by ioriiod0         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


from typing import Type, Mapping, Sequence, Union, Any, Optional, Callable, Tuple


class Request(dict):
    """
        intent: {"name":"ooxx","confidence":0.999}
        entities: [ {
            "entity": "ooxx",
            "value": 12313,
        }]
    """

    def __init__(self, body: Any, content_type: str = "text", intent: Optional[str] = None, entities: Optional[Sequence[Mapping]] = None, **kwargs):
        super(Request, self).__init__()
        self.body = body
        self.content_type = content_type
        self.intent = intent
        self.entities = [] if entities is None else entities
        self.__dict__.update(kwargs)

    def __getattr__(self, k: str):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)

    def __setattr__(self, k: str, v: Any):
        self[k] = v


class Response(dict):
    def __init__(self, body: Any, content_type: str = "text", **kwargs):
        super(Response, self).__init__()
        self.body = body
        self.content_type = content_type

    def __getattr__(self, k: str):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)

    def __setattr__(self, k: str, v: Any):
        self[k] = v
