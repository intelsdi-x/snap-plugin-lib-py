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
from .plugin_pb2 import add_ProcessorServicer_to_server
from .processor_proxy import _ProcessorProxy

LOG = logging.getLogger(__name__)


@six.add_metaclass(ABCMeta)
class Processor(Plugin):
    """Abstract base class for 'processor' plugins.

    This class makes the creation of snap 'processor' plugins as easy as
    possible.  For instance, when a class inherits from
    :py:class:`snap_plugin.v1.processor.Process` plugins can be created by
    providing implementation for:

        - :py:meth:`snap_plugin.v1.processor.Processor.process`
        - :py:meth:`~snap_plugin.v1.plugin.Plugin.get_config_policy`
    """

    def __init__(self, name, version, **kwargs):
        super(Processor, self).__init__()
        self.meta = Meta(PluginType.processor, name, version, **kwargs)
        self.proxy = _ProcessorProxy(self)
        add_ProcessorServicer_to_server(self.proxy, self.server)

    @abstractmethod
    def process(self, metrics, config):
        """Process metrics.

        This method is ``abstract`` so the implementation **must be provided**
        by the plugin which extends :obj:`snap_plugin.v1.Processor`.

        This method is called by the Snap deamon during the process phase
        of the execution of a Snap workflow.  Examples of processing metrics
        include applying filtering, max, min, average functions as well as
        adding additional context to the metrics to name just a few.

        Args:
            metrics (obj:`list` of :obj:`snap_plugin.v1.Metric`):
                List of metrics to be processed.

        Returns:
            :obj:`list` of :obj:`snap_plugin.v1.Metric`:
                List of processed metrics.
        """
        pass
