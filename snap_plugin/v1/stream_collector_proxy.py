# -*- coding: utf-8 -*-
# http://www.apache.org/licenses/LICENSE-2.0.txt
#
# Copyright 2017 Intel Corporation
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
import threading
import traceback
# It is needed to prevent ImportError in python 3.x, cased by renaming package Queue to queue
try:
    import Queue as queue
except ImportError:
    import queue as queue

from .plugin_pb2 import MetricsReply, CollectReply
from .plugin_proxy import PluginProxy
from .config_map import ConfigMap

LOG = logging.getLogger(__name__)


class _StreamCollectorProxy(PluginProxy):
    """Dispatches collector requests to the plugins implementation"""
    def __init__(self, stream_collector):
        super(_StreamCollectorProxy, self).__init__(stream_collector)
        self.plugin = stream_collector
        self.metrics_queue = queue.Queue(maxsize=0)

    def StreamMetrics(self, request_iterator, context):
        """Dispatches metrics streamed by collector"""

        thread = threading.Thread(target=self.plugin.stream,)
        thread.daemon = True
        thread.start()

        while True:
            metrics = []
            while not self.metrics_queue.empty():
                metrics.append(self.metrics_queue.get())
            metrics_col = CollectReply(Metrics_Reply=MetricsReply(metrics=[m.pb for m in metrics]))
            yield metrics_col

    def GetMetricTypes(self, request, context):
        """Dispatches the request to the plugins update_catalog method"""
        LOG.debug("GetMetricTypes called")
        try:
            metrics = self.plugin.update_catalog(ConfigMap(pb=request.config))
            return MetricsReply(metrics=[m.pb for m in metrics])
        except Exception as err:
            msg = "message: {}\n\nstack trace: {}".format(
                err, traceback.format_exc())
            return MetricsReply(metrics=[], error=msg)
