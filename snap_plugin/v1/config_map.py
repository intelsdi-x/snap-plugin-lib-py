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
from collections import MutableMapping
from itertools import chain

from .plugin_pb2 import ConfigMap as PbConfigMap


class ConfigMap(MutableMapping):
    """ConfigMap provides a map of config key value pairs.

    Args:
        *args: variable length argument list.  A valid argument is a two item
            tuple/list.  The first item is the key and the second is the value.
        **kwargs: Arbitrary keyword arguments representing the config.

    Example:
    ::
        cfg0 = snap.ConfigMap(user="john", port=911)
        cfg1 = snap.ConfigMap(("user","john"),("port", 911))

    Also see:
        - :py:class:`snap_plugin.v1.metric.Metric`
    """

    def __init__(self, *args, **kwargs):
        if "pb" in kwargs:
            self._pb = kwargs.get("pb")
        else:
            self._pb = PbConfigMap()
        for k, v in [(k, v) for (k, v) in kwargs.items() if k != "pb"]:
            self[k] = v
        if len(args) > 0:
            for arg in args:
                if isinstance(arg, (tuple, list)) and len(arg) == 2:
                    self[arg[0]] = arg[1]


    def __getattr__(self, attr):
        if attr in self.__dict__:
            # this object has it
            return getattr(self, attr)
        # proxy to the wrapped object
        return getattr(self._pb, attr)

    def __setitem__(self, key, item):
        if isinstance(item, float):
            self._pb.FloatMap[key] = item
        elif isinstance(item, bool):
            self._pb.BoolMap[key] = item
        elif isinstance(item, int):
            self._pb.IntMap[key] = item
        elif isinstance(item, str):
            self._pb.StringMap[key] = item
        else:
            raise TypeError("The type is '{}' and should be string, int, long, float "
                            "or bool".format(type(item)))

    def __getitem__(self, key):
        for dict in [self._pb.IntMap, self._pb.FloatMap, self._pb.StringMap,
                     self._pb.BoolMap]:
            if key in dict:
                return dict[key]
        raise KeyError(key)

    def __repr__(self):
        return repr(dict(chain(self._pb.StringMap.items(),
                               self._pb.IntMap.items(),
                               self._pb.FloatMap.items(),
                               self._pb.BoolMap.items())))

    def __len__(self):
        return (len(self._pb.IntMap) + len(self._pb.StringMap) +
                len(self._pb.FloatMap) + len(self._pb.BoolMap))

    def __delitem__(self, key):
        if key in self:
            for dict in [self._pb.IntMap, self._pb.FloatMap,
                         self._pb.StringMap, self._pb.BoolMap]:
                try:
                    del dict[key]
                    return
                except KeyError:
                    pass
        else:
            raise KeyError(key)

    def __iter__(self):
        for k in self._pb.IntMap:
            yield k
        for k in self._pb.FloatMap:
            yield k
        for k in self._pb.StringMap:
            yield k
        for k in self._pb.BoolMap:
            yield k

    def __contains__(self, key):
        for dict in [self._pb.IntMap, self._pb.FloatMap, self._pb.StringMap,
                     self._pb.BoolMap]:
            try:
                if key in dict.keys():
                    return True
            except KeyError:
                pass
        return False

    def __unicode__(self):
        return unicode(repr(self))

    def clear(self):
        "Removes all entries from the config map"
        self._pb.IntMap.clear()
        self._pb.StringMap.clear()
        self._pb.FloatMap.clear()
        self._pb.BoolMap.clear()

    def has_key(self, key):
        """Does the config map contain the key?

        Returns:
            bool: True if key exists, False otherwise.
        """
        return key in self

    def update(self, *args, **kwargs):
        """Update ConfigMap from mapping/iterable.

        If the key exists the entry is updated else it is added.

        Args:
            *args: variable length argument list.  A valid argument is a two item
                tuple/list.  The first item is the key and the second is the value.
            **kwargs: Arbitrary keyword arguments representing the config.
        """
        for k, v in args:
            self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def keys(self):
        "Returns a list of ConfigMap keys."
        return (list(self._pb.IntMap.keys()) + list(self._pb.StringMap.keys()) +
                list(self._pb.FloatMap.keys()) + list(self._pb.BoolMap.keys()))

    def values(self):
        "Returns a list of ConfigMap values."
        return (list(self._pb.IntMap.values()) + list(self._pb.StringMap.values()) +
                list(self._pb.FloatMap.values()) + list(self._pb.BoolMap.values()))

    def iteritems(self):
        "Returns an iterator over the items of ConfigMap."
        return chain(self._pb.StringMap.items(),
                     self._pb.IntMap.items(),
                     self._pb.FloatMap.items(),
                     self._pb.BoolMap.items())

    def itervalues(self):
        "Returns an iterator over the values of ConfigMap."
        return chain(self._pb.StringMap.values(),
                     self._pb.IntMap.values(),
                     self._pb.FloatMap.values(),
                     self._pb.BoolMap.values())

    def iterkeys(self):
        "Returns an iterator over the keys of ConfigMap."
        return chain(self._pb.StringMap.keys(),
                     self._pb.IntMap.keys(),
                     self._pb.FloatMap.keys(),
                     self._pb.BoolMap.keys())

    def items(self):
        "Returns a list of (key, value) pairs as 2-tuples."
        return (list(self._pb.IntMap.items()) + list(self._pb.StringMap.items()) +
                list(self._pb.FloatMap.items()) + list(self._pb.BoolMap.items()))

    def pop(self, key, default=None):
        """Remove specified key and return the corresponding value.
           If key is not found, default is returned if given, otherwise 
           KeyError is raised.
        """
        if key not in self:
            if default is not None:
                return default
            raise KeyError(key)
        for map in [self._pb.IntMap, self._pb.FloatMap, self._pb.StringMap,
                    self._pb.BoolMap]:
            if key in map.keys():
                return map.pop(key)

    def popitem(self):
        """Remove and return some (key, value) pair as a 2-tuple"""        
        try:
            key = next(iter(self))
        except StopIteration:
            raise KeyError
        value = self[key]
        del self[key]
        return key, value

    @property
    def pb(self):
        return self._pb
