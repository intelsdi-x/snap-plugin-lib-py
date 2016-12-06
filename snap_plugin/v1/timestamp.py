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

import time

from snap_plugin.v1.plugin_pb2 import Time as PbTime


class Timestamp(object):
    """Represents time in seconds since Epoch

    Args:
        time (:obj:`float`): time in seconds since Epoch

    Note:
        In most cases you shouldn't need to instantiate this class directly as
        the getter and setter on Metric automatically convert a `time.time()`
        into a :py:class:`~snap_plugin.v1.timestamp.Timestamp`.
    """
    def __init__(self, time=time.time(), pb=PbTime):
        self._pb = pb
        self._time = time
        self._pb.sec = int(self._time)
        self._pb.nsec = int((self._time - self._pb.sec) * 10 ** 9)

    def __getattr__(self, attr):
        if attr in self.__dict__:
            # this object has it
            return getattr(self, attr)
        # proxy to the wrapped object
        return getattr(self._pb, attr)

    @property
    def time(self):
        """Represents time in seconds since Epoch

        Args:
            :obj:`float`: time in seconds since Epoch (see time.time())

        Returns:
            None
        """
        return self._time

    def set(self, time):
        self._time = time
        self._pb.sec = int(self._time)
        self._pb.nsec = int((self._time - self._pb.sec) * 10 ** 9)
