# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    fields.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ioriiod0 <ioriiod0@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/01/07 18:28:23 by ioriiod0          #+#    #+#              #
#    Updated: 2019/01/10 13:14:17 by ioriiod0         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


from typing import Dict, Type, Optional, Any, Callable


class ValidateError(Exception):
    pass


class Field(object):
    def __init__(self, _type: Type[type], default: Any = None, validator: Optional[Callable] = None, factory: Optional[Callable] = None):
        self.name = None
        self.type = _type
        assert default is None or isinstance(default, _type)
        self.default = default
        self.validator = validator
        self.factory = factory

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)


class StringField(Field):
    def __init__(self, **kwargs):
        super(StringField, self).__init__(str, **kwargs)


class IntegerField(Field):
    def __init__(self, **kwargs):
        super(IntegerField, self).__init__(int, **kwargs)


class FloatField(Field):
    def __init__(self, **kwargs):
        super(FloatField, self).__init__(float, **kwargs)


class ListField(Field):
    def __init__(self, **kwargs):
        if "factory" not in kwargs:
            kwargs['factory'] = list
        super(ListField, self).__init__(list, **kwargs)


class DictField(Field):
    def __init__(self, **kwargs):
        if "factory" not in kwargs:
            kwargs['factory'] = dict
        super(DictField, self).__init__(dict, **kwargs)


class BooleanField(Field):
    def __init__(self, **kwargs):
        super(BooleanField, self).__init__(bool, **kwargs)
