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

from past.builtins import basestring

from .config_map import ConfigMap
from .namespace import Namespace
from .plugin_pb2 import Metric as PbMetric
from .timestamp import Timestamp


class Metric(object):
    """Metric

    The metric object is the core entity of snap representing metrics.

    Args:
        namespace (:obj:`list` of
            :py:class:`~snap_plugin.v1.namespace_element.NamespaceElement`):
            namespace elements
        version (:obj:`int`): metric version
        tags (:obj:`dict`): metric tags (key/value pairs)
        config (:py:class:`~snap_plugin.v1.config_map.ConfigMap`): config for
            metric (key/value pairs)
        timestamp (:obj:`float`): metric timestamp (see time.time())
        unit (:obj:`str`): metric unit
        description (:obj:`str`): metric description

    Example:
        metric = Metric(namespace=("acme", "sk8", "matix", "rotations"),
                        description="Rotation count")

    """
    def __init__(self, namespace=[], version=None, tags={}, config={},
                 timestamp=time.time(), unit="", description="", **kwargs):
        if "pb" in kwargs:
            self._pb = kwargs.get("pb")
            self._config = ConfigMap(pb=self._pb.Config)
            self._namespace = Namespace(pb=self._pb.Namespace)
            self._timestamp = Timestamp(pb=self._pb.Timestamp)
            if self._pb.HasField("int32_data"):
                self._data_type = int
            elif self._pb.HasField("int64_data"):
                self._data_type = int
            elif self._pb.HasField("uint32_data"):
                self._data_type = int
            elif self._pb.HasField("uint64_data"):
                self._data_type = int
            elif self._pb.HasField("float64_data"):
                self._data_type = float
            elif self._pb.HasField("float32_data"):
                self._data_type = float
            elif self._pb.HasField("string_data"):
                self._data_type = str
            elif self._pb.HasField("bool_data"):
                self._data_type = bool
            elif self._pb.HasField("bytes_data"):
                self._data_type = bytes
            return
        self._pb = PbMetric()
        # namespace
        if isinstance(namespace, (list, tuple)):
            self._namespace = Namespace(self._pb.Namespace, *namespace)
        else:
            raise TypeError("The 'namespace', kwarg requires a list or tuple "
                            "of :obj:`snap_plugin.v1.namespace_element.Namesp"
                            "aceElement.  (given: `{}`)"
                            .format(type(namespace)))
        # version
        if version is None:
            from snap_plugin.v1 import PLUGIN_VERSION
            self._pb.Version = PLUGIN_VERSION
        else:
            self._pb.Version = version
        # unit
        self._pb.Unit = unit
        # description
        self._pb.Description = description
        # tags
        if isinstance(tags, dict):
            self._pb.Tags.update(tags)
        else:
            raise TypeError("The 'tags' kwarg requires a dict of strings. "
                            "(given: `{}`)".format(type(tags)))
        # configs
        if isinstance(config, (list, tuple)):
            self._config = ConfigMap(pb=self._pb.Config, *config)
        elif isinstance(config, dict):
            self._config = ConfigMap(pb=self._pb.Config, **config)
        elif isinstance(config, ConfigMap):
            self._config = ConfigMap(config.items(), pb=self._pb.Config)
        else:
            raise TypeError("The 'config' kwarg requires a list, tuple or"
                            " dict.  (given: `{}`)".format(type(config)))
        # timestamp
        self._timestamp = Timestamp(pb=self._pb.Timestamp,
                                    time=timestamp)

        # this was added as a stop gap until
        # https://github.com/intelsdi-x/snap/issues/1394 lands
        self._last_advertised_time = Timestamp(pb=self._pb.LastAdvertisedTime,
                                               time=timestamp)
        # data
        if "data" in kwargs:
            self.data = kwargs.get("data")
        else:
            self._data_type = None

    @property
    def namespace(self):
        """Metric namespace elements.

        Returns:
            :obj:`list` of
                :py:class:`~snap_plugin.v1.namespace_element.NamespaceElement`)
        """
        return self._namespace

    @property
    def version(self):
        """Metric version.

        Args:
            value (:obj:`int`): version

        Returns:
            :obj:`int`
        """
        return self._pb.Version

    @version.setter
    def version(self, value):
        self._pb.Version = value

    @property
    def config(self):
        """Metric config

        Returns:
            :py:class:`~snap_plugin.v1.config_map.ConfigMap`

        """
        return self._config

    @property
    def timestamp(self):
        """Time in seconds since Epoch.

        Args:
            value (:obj:`float`): time in seconds since Epoch (see time.time())

        Returns:
            `float`: time in seconds since Epoch (see time.time())
        """
        return self._timestamp.time

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp.set(value)

    @property
    def tags(self):
        """Metric tags.

        Args:
            value (:obj:`dict` of strings): {"tag-key": "tag-value"}

        Returns:
            :obj:`list` of :obj:`tuple`: Example: [("tag-key", "tag-value")]

        """
        return self._pb.Tags

    @tags.setter
    def tags(self, value):
        self._pb.Tags.clear()
        self._pb.Tags.update(value)

    @property
    def unit(self):
        """Metric unit

        Args:
            value (:obj:`str`)

        Returns:
            :obj:`str`
        """
        return self._pb.Unit

    @unit.setter
    def unit(self, value):
        self._pb.Unit = value

    @property
    def description(self):
        """Metric description

        Args:
            value (:obj:`str`)

        Returns:
            :obj:`str`
        """
        return self._pb.Description

    @description.setter
    def description(self, value):
        self._pb.Description = value

    @property
    def data(self):
        """Metric data

        Args:
            value (:obj:`bool` or :obj:`int` or :obj:`long` or :obj:`float`
                or :obj:`basestring` or :obj:`bytes`)

        Returns:
            value

        Raises:
            :obj:`TypeError`

        """
        if self._data_type == "int":
            if self._pb.HasField("int64_data"):
                return self._pb.int64_data
            if self._pb.HasField("int32_data"):
                return self._pb.int32_data
            if self._pb.HasField("uint64_data"):
                return self._pb.uint64_data
            if self._pb.HasField("uint32_data"):
                return self._pb.uint32_data
        elif self._data_type == "float":
            if self._pb.HasField("float32_data"):
                return self._pb.float32_data
            if self._pb.HasField("float64_data"):
                return self._pb.float64_data
        elif self._data_type == "str":
            return self._pb.string_data
        elif self._data_type == "bool":
            return self._pb.bool_data
        elif self._data_type == "bytes":
            return self._pb.bytes_data
        return None

    @data.setter
    def data(self, value):
        if isinstance(value, bool):
            self._data_type = bool
            self._pb.bool_data = value
        elif isinstance(value, int):
            self._data_type = int
            self._pb.int64_data = value
        elif isinstance(value, float):
            self._data_type = float
            self._pb.float64_data = value
        elif isinstance(value, basestring):
            self._data_type = str
            self._pb.string_data = value
        elif isinstance(value, bytes):
            self._data_type = bytes
            self._pb.bytes_data = value
        else:
            raise TypeError("Unsupported data type '{}'.  (Supported: "
                            "int, long, float, str and bool)".format(value))

    @property
    def pb(self):
        return self._pb

    def __repr__(self):
        return self._pb.__repr__()
