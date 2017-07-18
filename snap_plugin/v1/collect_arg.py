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

from .plugin_pb2 import CollectArg as PbCollectArg
from .plugin_pb2 import MetricsArg


class CollectArg(object):
    """CollectArg

    This is the arg for the RPC method StreamMetrics.
    """
    def __init__(self, *metrics):
        self._pb = PbCollectArg(Metrics_Arg=MetricsArg(metrics=[m.pb for m in metrics]))

    @property
    def pb(self):
        "Returns the wrapped protobuf data holder."
        return self._pb
