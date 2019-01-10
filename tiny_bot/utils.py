# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    utils.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ioriiod0 <ioriiod0@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/01/08 19:24:18 by ioriiod0          #+#    #+#              #
#    Updated: 2019/01/10 21:03:12 by ioriiod0         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


from typing import Type, Dict, List, Union, Any, Optional, Callable, Tuple


def create_flask_app(bot: type['Bot'], req2req: Callable[[Any], 'Request'], res2res: Callable[['Response'], Any]):
    pass
