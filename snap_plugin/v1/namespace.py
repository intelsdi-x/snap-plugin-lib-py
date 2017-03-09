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

from past.builtins import basestring

from .namespace_element import NamespaceElement


class Namespace(object):
    """Namespace of a metric.

    Args:
        elements (:obj:`list` of
            :py:class:`~snap_plugin.v1.namespace_element.NamespaceElement`
            or :obj:`list` of `strings`):
            namespace elements

    """

    def __init__(self, pb, *elements):
        self._pb = pb
        for nse in elements:
            if isinstance(nse, basestring):
                self.add_static_element(nse)
            else:
                if nse is not None:
                    self.add(nse)

    def __getitem__(self, index):
        return NamespaceElement(pb=self._pb.__getitem__(index))

    def __delitem__(self, index):
        return self._pb.__delitem__(index)

    def __len__(self):
        return len(self._pb)

    def add_dynamic_element(self, name, description):
        """Adds a dynamic namespace element to the end of the Namespace.

        A dynamic namespace element is defined by an element that contains a
        non-static data relative to the metric being collected.  For instance,
        when collecting metrics for a given virtual machine the namespace
        element that contains the virtual-machine-id would be dynamic.  This is
        modeled by the a NamespaceElement when its `name` attribute contains the
        value 'virtual-machine-id'.  In this example the `value` attribute would
        be set to the ID of the virtual machine when the metric is collected.

        Args:
            value (:py:class:`snap_plugin.v1.namespace_element.NamespaceElement`):
                namespace element

        Returns:
            :py:class:`snap_plugin.v1.namespace.Namespace`
        """
        self._pb.add(Name=name, Description=description, Value="*")
        return self

    def add_static_element(self, value):
        """Adds a static namespace element to the end of the Namespace.

        A static namespace element is defined by the `value` attribute being set
        and where the `name` attribute is not used (set to None).  This is the
        case when the namespace does not change based on what is being
        collected.

        Args:
            value (:py:class:`snap_plugin.v1.namespace_element.NamespaceElement`):
                namespace element

        Returns:
            :py:class:`snap_plugin.v1.namespace.Namespace`
        """
        self._pb.add(Value=value)
        return self

    def pop(self, key=-1):
        """Removes and retuns the namespace element at a given index.

        If the kwarg 'key' is provided the item at the given index is removed
        and returned.  If the kwarg 'key'' is not provided the last Namespace
        element is removed and returned.

        Args:
            **kwargs (optional): key=-1
        """
        return self._pb.pop(key)

    def add(self, namespace_element):
        self._pb.add(Value=namespace_element.value,
                     Name=namespace_element.name,
                     Description=namespace_element.description)
