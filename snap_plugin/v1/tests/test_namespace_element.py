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

from snap_plugin.v1.namespace_element import NamespaceElement


def test_namespace_element():
    ns1 = NamespaceElement(name="myName",
                           value="myValue",
                           description="myDescription")
    assert (ns1.name == "myName" and
            ns1.value == "myValue" and
            ns1.description == "myDescription")

    ns2 = NamespaceElement.dynamic_namespace_element("myName", "myDescription")
    assert (ns2.name == "myName" and
            ns2.description == "myDescription")

    ns3 = NamespaceElement.static_namespace_element("myValue")
    assert (ns3.value == "myValue")
