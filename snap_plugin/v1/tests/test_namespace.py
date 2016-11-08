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

from snap_plugin.v1.namespace import Namespace
from snap_plugin.v1.namespace_element import NamespaceElement
from snap_plugin.v1.plugin_pb2 import Metric


def test_namespace():
    ns1 = Namespace(Metric().Namespace)
    ns1.add_static_element("runc").add_static_element("libcontainer")

    assert len(ns1) == 2
    assert ns1[0].value == "runc"
    assert ns1[1].value == "libcontainer"

    ns1.add_dynamic_element("container-id", "container id")
    ns1.add_static_element("status")

    assert len(ns1) == 4
    assert (ns1[2].name == "container-id" and
            ns1[2].description == "container id")
    assert ns1[3].value == "status"

    ns2 = Namespace(
        Metric().Namespace,
        NamespaceElement.static_namespace_element("runc"),
        NamespaceElement.static_namespace_element("libcontainer"),
        NamespaceElement.dynamic_namespace_element("container-id",
                                                   "container id"),
        NamespaceElement.static_namespace_element("status"),
    )
    assert len(ns2) == 4
    assert ns2[0].value == "runc"
    assert ns2[1].value == "libcontainer"
    assert (ns2[2].name == "container-id" and
            ns2[2].description == "container id")
    assert ns2[3].value == "status"

    ns3 = Namespace(
        Metric().Namespace,
        "runc",
        "libcontainer"
    )
    assert len(ns3) == 2
    assert ns3[0].value == "runc"
    assert ns3[1].value == "libcontainer"
