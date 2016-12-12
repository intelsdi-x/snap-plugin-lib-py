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
from builtins import int

import pytest
from past.builtins import basestring

from snap_plugin.v1 import ConfigMap, Metric, NamespaceElement


class TestMetric(object):

    def test_constructor(self):
        m = Metric()
        assert len(m.namespace) == 0
        assert len(m.config) == 0

        m = Metric(namespace=[NamespaceElement(value="foo"),
                              NamespaceElement(value="bar")],
                   version=1,
                   config={"string": "some_string",
                           "int": 1,
                           "float": 1.1,
                           "bool": True},
                   tags={"key": "value"},
                   unit="b",
                   description="some description",
                   data=5)
        assert len(m.namespace) == 2
        assert m.namespace[0].value == "foo"
        assert m.namespace[1].value == "bar"
        assert m.version == 1
        assert len(m.config) == 4
        assert m.timestamp.sec > 0
        assert len(m.tags) == 1
        assert m.tags["key"] == "value"
        assert m.unit == "b"
        assert m.description == "some description"
        assert not m._pb.HasField("float64_data")
        assert not m._pb.HasField("int32_data")
        assert not m._pb.HasField("string_data")
        assert not m._pb.HasField("bytes_data")
        assert not m._pb.HasField("bool_data")
        assert m._pb.HasField("int64_data")
        assert m._data_type is int
        assert m.data == 5

        m = Metric(config=(("string", "string"), ("int", 1)), timestamp=0)
        assert len(m.config) == 2
        assert (m.config["string"] == "string" and
                m.config["int"] == 1)
        assert m.timestamp.sec == 0

    def test_metric_attrs(self):
        m = Metric()
        now = time.time()
        # timestamp
        m.timestamp.set(now)
        assert m.timestamp.sec == int(now)
        m.timestamp = now
        assert m.timestamp.sec == int(now)
        # version
        m.version = 1
        assert m.version == 1
        # tags
        assert len(m.tags) == 0
        m.tags = {"asdf": "asdf"}
        assert len(m.tags) == 1
        assert m.tags["asdf"] == "asdf"
        m.tags = {"something": "different", "foo": "bar"}
        assert len(m.tags) == 2
        assert m.tags["something"] == "different"
        assert m.tags["foo"] == "bar"
        # unit
        assert m.unit == ""
        m.unit = "ms"
        assert m.unit == "ms"
        # description
        assert m.description == ""
        m.description = "some description"
        assert m.description == "some description"
        # data
        m.data = 1.0
        assert type(m.data) is float
        m.data = "test"
        assert isinstance(m.data, basestring)
        m.data = True
        assert isinstance(m.data, bool)
        m.data = int(5)
        assert isinstance(m.data, int)


    def test_metric_namespace(self):
        m = Metric(namespace=[NamespaceElement(value="el0"),
                              NamespaceElement(value="el1")])
        assert len(m.namespace) == 2
        assert m.namespace[0].value == "el0"
        assert m.namespace[1].value == "el1"
        # add a static namespace element
        m.namespace.add_static_element("el2")
        assert len(m.namespace) == 3
        assert (m.namespace[2].value == "el2" and
                m.namespace[2].description == "" and
                m.namespace[2].name == "")
        # add a dynamic namespace element
        m.namespace.add_dynamic_element("el3", "i'm dynamic!")
        assert len(m.namespace) == 4
        assert (m.namespace[3].value == "*" and
                m.namespace[3].name == "el3" and
                m.namespace[3].description == "i'm dynamic!")
        # pop/remove the last element of the namespace
        m.namespace.pop()
        assert len(m.namespace) == 3
        assert m.namespace[len(m.namespace)-1].value == "el2"
        # pop/remove the first element of the NamespaceElement
        m.namespace.pop(0)
        assert len(m.namespace) == 2
        assert m.namespace[0].value == "el1"

        m = Metric(namespace=("foo","bar","baz"))
        assert len(m.namespace) == 3
        assert m.namespace[0].value == "foo"
        assert m.namespace[1].value == "bar"
        assert m.namespace[2].value == "baz"

    def test_metric_config(self):
        m = Metric(config={"string": "some_string",
                           "int": 1,
                           "float": 1.1,
                           "bool": True})
        assert len(m.config) == 4
        assert (m.config["string"] == "some_string" and
                m.config["float"] == 1.1 and
                m.config["int"] == 1 and
                m.config["bool"] is True)

        with pytest.raises(AttributeError) as excinfo:
                m.config = ConfigMap()
        assert "can't set attribute" in str(excinfo.value)
