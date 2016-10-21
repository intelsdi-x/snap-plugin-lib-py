# -*- coding: utf-8 -*-

# http://www.apache.org/licenses/LICENSE-2.0.txt
#
# Copyright 2016 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from builtins import int

from .plugin_pb2 import IntegerPolicy as PbIntegerPolicy
from .plugin_pb2 import IntegerRule as PbIntegerRule


class _IntegerPolicy(object):
    """An _IntegerPolicy wraps IntegerRules.

    The _IntegerPolicy class is instantiated by the ConfigPolicy constructor.
    Users should never need to create an instance of this class themselves.

    See:
        - :py:class:`snap_plugin.v1.config_policy.ConfigPolicy`
    """
    def __init__(self, key, *args, **kwargs):
        self._pb = kwargs.get("pb", PbIntegerPolicy())
        for v in args:
            self._pb.rules[key].MergeFrom(v._pb)


class IntegerRule(object):
    """A configuration item with a integer value type.

    Args:
        default (:obj:`int`): The default value
        maximum (:obj:`int`): The maximum allowed value
        minimum (:obj:`int`): The minimum allowed value
        required (:obj:`bool`): Is the config item required

    """
    def __init__(self, default=None, maximum=None, minimum=None,
                 required=False, **kwargs):
        self._pb = kwargs.get("pb", PbIntegerRule())
        if default is not None:
            self._pb.default = int(default)
            self._pb.has_default = True
        if maximum is not None:
            self._pb.maximum = maximum
            self._pb.has_max = True
        if minimum is not None:
            self._pb.minimum = minimum
            self._pb.has_min = True
        self._pb.required = required

    @property
    def default(self):
        """The default value"""
        return self._pb.default

    @default.setter
    def default(self, value):
        if value is None:
            self._pb.has_default = False
            self._pb.default = 0
        else:
            self._pb.has_default = True
            self._pb.default = value

    @property
    def maximum(self):
        """The maximum allowed value"""
        return self._pb.maximum

    @maximum.setter
    def maximum(self, value):
        if value is None:
            self._pb.maximum = 0
            self._pb.has_max = False
        else:
            self._pb.maximum = value
            self._pb.has_max = True

    @property
    def minimum(self):
        """The minimum allowed value"""
        return self._pb.minimum

    @minimum.setter
    def minimum(self, value):
        if value is None:
            self._pb.minimum = 0
            self._pb.has_min = False
        else:
            self._pb.minimum = value
            self._pb.has_min = True

    @property
    def required(self):
        """Is the config item required"""
        return self._pb.required

    @required.setter
    def required(self, value):
        self._pb.required = value
