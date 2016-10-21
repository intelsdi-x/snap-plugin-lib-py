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

from past.builtins import basestring

from .bool_policy import BoolRule, _BoolPolicy
from .float_policy import FloatRule, _FloatPolicy
from .integer_policy import IntegerRule, _IntegerPolicy
from .plugin_pb2 import GetConfigPolicyReply
from .string_policy import StringRule, _StringPolicy


class ConfigPolicy(object):
    """ConfigPolicy describes the configuration items for a plugin.

    A plugin exposes its configuration to the Snap framework through the object
    :py:class:`~snap_plugin.v1.config_policy.ConfigPolicy`.  The policy
    describes the configuration items value type (`string`,
    `float`, `integer` and `bool`), it's default value (if any) as well as its
    contraints (min, max, etc).

    Args:
            *args: A variable length list of tuples/lists where the first item
                of the list/tuple is a tuple/list representing the namespace.
                The second item is a tuple/list where the first item is the
                config's key and the second is the specific configuration rule
                that should be applied.

    Example:
    ::
        snap.ConfigPolicy(
            [
                ("random"),
                [
                    (
                        "int_max",
                        snap.IntegerRule(default=100, minimum=1, maximum=10000)
                    ),
                    (
                        "int_min",
                        snap.IntegerRule(default=0, minimum=0)
                    )
                ]
            ]
        )

    Also see:
        - :py:class:`snap_plugin.v1.integer_policy.IntegerRule`
        - :py:class:`snap_plugin.v1.float_policy.FloatRule`
        - :py:class:`snap_plugin.v1.string_policy.StringRule`
        - :py:class:`snap_plugin.v1.bool_policy.BoolPolicy`

    """

    def __init__(self, *args):
        self._pb = GetConfigPolicyReply()
        for (ns, policies) in args:
            if isinstance(ns, basestring):
                ns = (ns,)
            if ns is not None and not isinstance(ns, (list, tuple)):
                raise TypeError("A tuple representing the namespace was "
                                "expected.  Given: {} {}.".format(type(ns), ns))
            ns, str_key = _check_key(ns)
            for policy in policies:
                if isinstance(policy, (list, tuple)) and len(policy) == 2:
                    if isinstance(policy[1], StringRule):
                        stringPolicy = _StringPolicy(policy[0], policy[1])
                        # we only want to add the key once to the rule
                        if len(self._pb.string_policy[str_key].key) == 0:
                            for nse in ns:
                                stringPolicy._pb.key.append(nse)
                        self._pb.string_policy[str_key].MergeFrom(stringPolicy._pb)
                    elif isinstance(policy[1], IntegerRule):
                        integerPolicy = _IntegerPolicy(policy[0], policy[1])
                        # we only want to add the key once to the rule
                        if len(self._pb.integer_policy[str_key].key) == 0:
                            for nse in ns:
                                integerPolicy._pb.key.append(nse)
                        self._pb.integer_policy[str_key].MergeFrom(
                            integerPolicy._pb)
                    elif isinstance(policy[1], BoolRule):
                        boolPolicy = _BoolPolicy(policy[0], policy[1])
                        # we only want to add the key once to the rule
                        if len(self._pb.bool_policy[str_key].key) == 0:
                            for nse in ns:
                                boolPolicy._pb.key.append(nse)
                        self._pb.bool_policy[str_key].MergeFrom(boolPolicy._pb)
                    elif isinstance(policy[1], FloatRule):
                        floatPolicy = _FloatPolicy(policy[0], policy[1])
                        # we only want to add the key once to the rule
                        if len(self._pb.float_policy[str_key].key) == 0:
                            for nse in ns:
                                floatPolicy._pb.key.append(nse)
                        self._pb.float_policy[str_key].MergeFrom(floatPolicy._pb)
                else:
                    raise TypeError("Expected a tuple where the first item is "
                                    "the config key and the second is the "
                                    "rule that should be applied")

    def __len__(self):
        return (len(self._pb.string_policy) + len(self._pb.integer_policy)
                + len(self._pb.bool_policy) + len(self._pb.float_policy))

    def __setitem__(self, key, value):
        _, str_key = _check_key(key)
        if isinstance(value, _StringPolicy):
            self._pb.string_policy[str_key].MergeFrom(value._pb)
        elif isinstance(value, _IntegerPolicy):
            self._pb.integer_policy[str_key].MergeFrom(value._pb)
        elif isinstance(value, _BoolPolicy):
            self._pb.bool_policy[str_key].MergeFrom(value._pb)
        elif isinstance(value, _FloatPolicy):
            self._pb.float_policy[str_key].MergeFrom(value._pb)

    def __getitem__(self, key):
        import itertools
        rules = dict(
            itertools.chain(self._pb.string_policy[key].rules.items(),
                            self._pb.bool_policy[key].rules.items(),
                            self._pb.integer_policy[key].rules.items(),
                            self._pb.float_policy[key].rules.items()))
        return type('Rules', (object,), {"rules": rules})


def _check_key(key):
    errors = []
    if isinstance(key, tuple):
        for i in key:
            if not isinstance(i, basestring):
                errors.append("Expected: string, Received: {}:{}"
                              .format(type(i), i))
    elif isinstance(key, basestring):
        return (key,), key
    elif key is None:
        return "", ""
    else:
        raise TypeError("Expected: tuple of strings, Received: {}"
                        .format(type(key)))
    if len(errors) > 0:
        raise TypeError(errors)
    return key, ".".join(key)
