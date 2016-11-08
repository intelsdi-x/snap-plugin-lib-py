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


import pytest

from snap_plugin.v1.collector import Collector
from snap_plugin.v1.processor import Processor
from snap_plugin.v1.publisher import Publisher


class TestPlugin(object):

    def test_collector(self):
        with pytest.raises(TypeError) as excinfo:
            Collector("name", 1)
        assert "Can't instantiate abstract class Collector" in str(excinfo.value)

    def test_processor(self):
        with pytest.raises(TypeError) as excinfo:
            Processor("name", 1)
        assert "Can't instantiate abstract class Processor" in str(excinfo.value)

    def test_publisher(self):
        with pytest.raises(TypeError) as excinfo:
            Publisher("name", 1)
        assert "Can't instantiate abstract class Publisher" in str(excinfo.value)
