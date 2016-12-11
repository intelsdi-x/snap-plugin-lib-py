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

from .plugin_pb2 import NamespaceElement as PbNamespaceElement


class NamespaceElement(object):
    """Namespace element of a metric.

    A namespace element is static when the `value` attribute is set
    and where the `name` attribute is not set.  This is the case when the 
    namespace does not change based on what is being collected.

    A dynamic namespace element is defined by an element that contains
    non-static data relative to the metric being collected.  For instance, when
    collecting metrics for a given virtual machine the namespace element that
    contains the virtual-machine-id would be dynamic.  This is modeled by
    the NamespaceElement when its `name` attribute contains the value
    'virtual-machine-id'.  In this example the `value` attribute would be set
    to the ID of the virtual machine when the metric is collected and '*' when
    the metric catalog is updated.

    Args:
        value (:obj:`str`): The value of an element.
        name (:obj:`str`): The name of an element.
        description (:obj:`str`): A short description of the element.

    """

    def __init__(self, name="", description="", value="", **kwargs):
        if "pb" in kwargs:
            self._pb = kwargs.get("pb")
        else:
            self._pb = PbNamespaceElement()
            self._pb.Value = value
            self._pb.Description = description
            self._pb.Name = name
            if name != "" and value == "":
                # If the name is provided it's a dynamic metric.
                # If the value field is not also set it needs to be set to the
                # default '*'.
                self._pb.Value = "*"

    def __getattr__(self, attr):
        if attr in self.__dict__:
            # this object has it
            return getattr(self, attr)
        # proxy to the wrapped object
        return getattr(self._pb, attr)

    @property
    def value(self):
        return self._pb.Value

    @value.setter
    def value(self, value):
        self._pb.Value = value

    @property
    def description(self):
        return self._pb.Description

    @description.setter
    def description(self, description):
        self._pb.Description = description

    @property
    def name(self):
        return self._pb.Name

    @name.setter
    def name(self, name):
        self._pb.Name = name

    @classmethod
    def static_namespace_element(cls, value):
        """Returns a static namespace_element.

        A static namespace element is one whose `value` attribute is set and
        the `name` attribute is not.

        Args:
            value (`str`): Value of the namespace element

        Returns:
            :py:class:`~snap_plugin.v1.namespace_element.NamespaceElement`: NamespaceElement
        """
        return cls(value=value)

    @classmethod
    def dynamic_namespace_element(cls, name, description):
        """Returns a dynamic namespace_element.

        A dynamic namespace element is one whose `value` attribute is set while
        the `name` attribute is not.

        Args:
            name (`str`): Name of the namespace element
            description (`str`): Decription of the namespace element

        Returns:
            :py:class:`~snap_plugin.v1.namespace_element.NamespaceElement`: NamespaceElement
        """
        return cls(name=name, description=description)
