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

from .config_map import ConfigMap
from .plugin_pb2 import GetMetricTypesArg as PbGetMetricTypesArg


class GetMetricTypesArg(object):
    """GetMetricTypesrArg

    This is the arg for the RPC method GetMetricTypes.

    Args:
        config (:py:class:`snap_plugin.v1.config_map.ConfigMap`): config map.

    """
    def __init__(self, config=None):
        self._pb = PbGetMetricTypesArg()
        if isinstance(config, (list, tuple)):
            self._config = ConfigMap(pb=self._pb.config, *config)
        elif isinstance(config, dict):
            self._config = ConfigMap(pb=self._pb.config, **config)
        else:
            raise TypeError("The 'config' kwarg requires a list, tuple or"
                            " dict.  (given: `{}`)".format(type(config)))

    def __getattr__(self, attr):
        if attr in self.__dict__:
            # this object has it
            return getattr(self, attr)
        # proxy to the wrapped object
        return getattr(self._pb, attr)

    @property
    def pb(self):
        "Returns the wrapped protobuf data holder."
        return self._pb
