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
import time
# It is needed to prevent ImportError in python 3.x, caused by renaming package Queue to queue
try:
    import Queue as queue
except ImportError:
    import queue as queue

from .metric import Metric
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
        self.done_queue = queue.Queue(maxsize=1)
        self.max_metrics_buffer = 0
        self.max_collect_duration = 10

    def _stream_wrapper(self, metrics):
        requested_metrics = []
        for mt in metrics:
            for metric in mt.Metrics_Arg.metrics:
                requested_metrics.append(Metric(pb=metric))
        while self.done_queue.empty():
            returned_metrics = []
            returned_metrics.extend(self.plugin.stream(requested_metrics))
            for returned_metric in returned_metrics:
                self.metrics_queue.put(returned_metric)

    def StreamMetrics(self, request_iterator, context):
        """Dispatches metrics streamed by collector"""
        LOG.debug("StreamMetrics called")
        collect_args = []
        collect_args.append(next(request_iterator))
        try:
            if collect_args[0].MaxCollectDuration > 0:
                self.max_collect_duration = collect_args[0].MaxCollectDuration
            if collect_args[0].MaxMetricsBuffer > 0:
                self.max_metrics_buffer = collect_args[0].MaxMetricsBuffer
        except Exception as ex:
            LOG.debug("Unable to get schedule parameters: {}".format(ex))

        thread = threading.Thread(target=self._stream_wrapper, args=(collect_args,),)
        thread.daemon = True
        thread.start()

        after_collect_duration = time.time() + self.max_collect_duration
        metrics = []
        while context.is_active():
            # check if max_collect_duration has been reached
            if time.time() >= after_collect_duration:
                metrics_col = CollectReply(Metrics_Reply=MetricsReply(metrics=[m.pb for m in metrics]))
                metrics = []
                after_collect_duration = time.time() + self.max_collect_duration
                yield metrics_col
            # if plugin puts metrics on queue
            while not self.metrics_queue.empty():
                # get metric from queue and add it to list
                metrics.append(self.metrics_queue.get())
                # if mex_metrics_buffer is set to 0, stream metric
                if self.max_metrics_buffer == 0:
                    metrics_col = CollectReply(Metrics_Reply=MetricsReply(metrics=[m.pb for m in metrics]))
                    metrics = []
                    after_collect_duration = time.time() + self.max_collect_duration
                    yield metrics_col
                else:
                    # verify if length of metrics buffer has been reached
                    if len(metrics) == self.max_metrics_buffer:
                        metrics_col = CollectReply(Metrics_Reply=MetricsReply(metrics=[m.pb for m in metrics]))
                        metrics = []
                        after_collect_duration = time.time() + self.max_collect_duration
                        yield metrics_col
                    # check if max_collect_duration has been reached
                    if time.time() >= after_collect_duration:
                        metrics_col = CollectReply(Metrics_Reply=MetricsReply(metrics=[m.pb for m in metrics]))
                        metrics = []
                        after_collect_duration = time.time() + self.max_collect_duration
                        yield metrics_col
        # sent notification if stream has been stopped
        self.done_queue.put(True)

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
