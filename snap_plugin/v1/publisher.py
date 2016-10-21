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

from .plugin import Meta, Plugin, PluginType
from .plugin_pb2 import add_PublisherServicer_to_server
from .publisher_proxy import PublisherProxy

LOG = logging.getLogger(__name__)

@six.add_metaclass(ABCMeta)
class Publisher(Plugin):
    """Abstract base class for 'publisher' plugins.

    This class makes the creation of snap 'publisher' plugins as easy as
    possible.  For instance, when a class inherits from
    :py:class:`snap_plugin.v1.publisher.Publisher` plugins can be created by
    providing implementation for:

        - :py:meth:`~snap_plugin.v1.publisher.Publisher.publish`
        - :py:meth:`~snap_plugin.v1.plugin.Plugin.get_config_policy`

    """

    def __init__(self, name, version, **kwargs):
        super(Publisher, self).__init__()
        self.meta = Meta(PluginType.publisher, name, version, **kwargs)
        self.proxy = PublisherProxy(self)
        add_PublisherServicer_to_server(self.proxy, self.server)

    @abstractmethod
    def publish(self, metrics, config):
        """Publishes metrics.

        This method is ``abstract`` so the implementation **must be provided**
        by the plugin which extends :obj:`snap_plugin.v1.Publisher`.

        This method is called by the Snap deamon during the publish phase
        of a Snap workflow.

        Args:
            metrics (:obj:`list` of `snap_plugin.v1.Metric`):
                List of metrics to be published.
            config (`snap_plugin.v1.ConfigMap`):
                Dict of config values.

        Returns:
            None

        """
        pass
