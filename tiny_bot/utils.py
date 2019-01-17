# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    utils.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ioriiod0 <ioriiod0@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/01/08 19:24:18 by ioriiod0          #+#    #+#              #
#    Updated: 2019/01/17 13:14:55 by ioriiod0         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


from typing import Type, Any, Optional, Callable, Tuple


def create_flask_app(bot: type['Bot'], endpoint: str, req2req: Callable[[Any], 'Request'] = None, res2res: Callable[['Response'], Any] = None):
    from flask import App
