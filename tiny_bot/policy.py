# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    policy.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ioriiod0 <ioriiod0@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/01/08 17:55:38 by ioriiod0          #+#    #+#              #
#    Updated: 2019/01/10 14:48:28 by ioriiod0         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from typing import Type, List, Tuple, Optional, Dict
from .types import Request, Response


class Policy(object):
    def __init__(self):
        super(Policy, self).__init__()

    def predict(self, bot: Type['Bot'], tracker: Type['Tracker'], msg: Type[Request]) -> Tuple[List[str], Optional[int]]:
        raise NotImplementedError("not implemented")

    def __call__(self, bot: Type['Bot'], tracker: Type['Tracker'], msg: Type[Request]) -> Tuple[List[str], Optional[int]]:
        return self.predict(bot, tracker, msg)
