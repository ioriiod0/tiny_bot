# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    types.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ioriiod0 <ioriiod0@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/01/10 14:46:03 by ioriiod0          #+#    #+#              #
#    Updated: 2019/01/10 14:46:20 by ioriiod0         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


from typing import Type, Dict, List, Union, Any, Optional, Callable, Tuple


class Request(object):
    """
        intent: {"name":"ooxx","confidence":0.999}
        entities: [ {
            "entity": "ooxx",
            "value": 12313,
        }]
    """

    def __init__(self, body: Any, content_type: str = "text", intent: Optional[dict] = None, entities: Optional[List[Dict]] = None, **kwargs):
        super(Request, self).__init__()
        self.body = body
        self.content_type = content_type
        self.intent = intent
        self.entities = [] if entities is None else entities
        self.__dict__.update(kwargs)

    def __getitem__(self, k: str):
        return getattr(self, k)

    def __setitem__(self, k: str, v: Any):
        setattr(self, k, v)

    def as_dict(self):
        return self.__dict__


class Response(object):
    def __init__(self, body, content_type="text", **kwargs):
        super(Response, self).__init__()
        self.body = body
        self.content_type = content_type

    def __getitem__(self, k: str):
        return getattr(self, k)

    def __setitem__(self, k: str, v: Any):
        setattr(self, k, v)

    def as_dict(self):
        return self.__dict__
