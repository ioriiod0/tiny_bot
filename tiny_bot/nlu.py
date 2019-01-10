# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    nlu.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ioriiod0 <ioriiod0@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/01/08 18:35:24 by ioriiod0          #+#    #+#              #
#    Updated: 2019/01/10 13:32:07 by ioriiod0         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


from typing import Type, List, Dict
from .tracker import Tracker


class NLU(object):
    def __init__(self):
        super(NLU, self).__init__()

    def parse(self, bot: Type['Bot'], tracker: Type['Request'], msg: Dict) -> Type['Request']:
        raise NotImplementedError("not implemented")

    def __call__(self, bot: Type['Bot'], tracker: Type['Request'], msg: Dict) -> Type['Request']:
        return self.parse(bot, tracker, msg)
