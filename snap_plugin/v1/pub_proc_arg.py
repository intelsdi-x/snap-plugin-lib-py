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

from .plugin_pb2 import PubProcArg


class _PubProcArg(object):
    def __init__(self, metrics=[], **kwargs):
        self._pb = PubProcArg(Metrics=[m.pb for m in metrics])
        if "config" in kwargs:
            self._pb.Config.MergeFrom(kwargs.get("config").pb)

    @property
    def pb(self):
        return self._pb


class _ProcessArg(_PubProcArg):
    def __init__(self, metrics=[], **kwargs):
        super(_ProcessArg, self).__init__(metrics=metrics, **kwargs)


class _PublishArg(_PubProcArg):
    def __init__(self, metrics=None, **kwargs):
        super(_PublishArg, self).__init__(metrics=metrics, **kwargs)
