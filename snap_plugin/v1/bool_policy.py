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

from .plugin_pb2 import BoolPolicy as PbBoolPolicy
from .plugin_pb2 import BoolRule as PbBoolRule


class _BoolPolicy(object):
    """An _BoolPolicy wraps BoolRules.

    The _BoolPolicy class is instantiated by the ConfigPolicy constructor.
    Users should never need to create an instance of this class themselves.

    See:
        - :py:class:`snap_plugin.v1.config_policy.ConfigPolicy`
    """
    def __init__(self, key, *args, **kwargs):
        self._pb = kwargs.get("pb", PbBoolPolicy())
        for arg in args:
            self._pb.rules[key].MergeFrom(arg._pb)


class BoolRule(object):
    """A configuration item with a integer value type.

    Args:
        default (:obj:`bool`): The default value
        required (:obj:`bool`): Is the config item required?

    """
    def __init__(self, default=False, required=False, **kwargs):
        self._pb = kwargs.get("pb", PbBoolRule())
        if default:
            self._pb.default = True
            self._pb.has_default = True
        self._pb.required = required

    @property
    def default(self):
        """The default value"""
        return self._pb.default

    @default.setter
    def default(self, value):
        if value is None:
            self._pb.has_default = False
            self._pb.default = False
        else:
            self._pb.has_default = True
            self._pb.default = value

    @property
    def required(self):
        """Is the config item required"""
        return self._pb.required

    @required.setter
    def required(self, value):
        self._pb.required = value
