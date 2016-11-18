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


import logging
from abc import ABCMeta, abstractmethod

import six

from .collector_proxy import _CollectorProxy
from .plugin import Meta, Plugin, PluginType
from .plugin_pb2 import add_CollectorServicer_to_server

LOG = logging.getLogger(__name__)


@six.add_metaclass(ABCMeta)
class Collector(Plugin):
    """Abstract base class for 'collector' plugins.

    This class makes the creation of a snap 'collector'
    plugin as easy as possible.  For instance, when a class inherits from
    py:class:`snap_plugin.v1.collector.Collector` plugins can be created by
    providing implementations for:

        - :py:meth:`~snap_plugin.v1.collector.Collector.collect`
        - :py:meth:`~snap_plugin.v1.collector.Collector.update_catalog`
        - :py:meth:`~snap_plugin.v1.plugin.Plugin.get_config_policy`
    """

    def __init__(self, name, version, **kwargs):
        super(Collector, self).__init__()
        self.meta = Meta(PluginType.collector, name, version, **kwargs)
        self.proxy = _CollectorProxy(self)
        add_CollectorServicer_to_server(self.proxy, self.server)

    @abstractmethod
    def collect(self, metrics):
        """Collect requested metrics.

        This method is ``abstract`` so the implementation **must be provided**
        by the plugin which extends :obj:`snap_plugin.v1.Collector`.

        This method is called by the Snap deamon during the collection phase
        of the execution of a Snap workflow.

        Args:
            metrics (:obj:`list` of :obj:`snap_plugin.v1.Metric`):
                List of metrics to be collected.

        Returns:
            :obj:`list` of :obj:`snap_plugin.v1.Metric`:
                List of collected metrics.
        """
        pass

    @abstractmethod
    def update_catalog(self, config):
        """Returns the metrics which the plugin provides.

        This method is called by the Snap daemon when the plugin is loaded and
        returns a :obj:`list` of :py:class:`snap_plugin.v1.metric.Metric` that
        will populate the snap metric catalog.  The method is ``abstract`` so
        the implementation **must be provided** by the plugin which extends
        :obj:`snap_plugin.v1.Collector`.

        Note:  Requiring config to successfully return metric types should be
        avoided.  Only in rare circumstances should a plugin require
        configuration data for it to load.

        Args:
            config (:obj:`snap_plugin.v1.ConfigMap`):
                Provides configuration data.

        Returns:
            :obj:`list` of :obj:`snap_plugin.v1.Metric`:
                List of collectable metrics.
        """
        pass
