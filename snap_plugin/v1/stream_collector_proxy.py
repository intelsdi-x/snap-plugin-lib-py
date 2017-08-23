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
        for metric in metrics.Metrics_Arg.metrics:
            requested_metrics.append(Metric(pb=metric))
        while self.done_queue.empty():
            returned_metrics = self.plugin.stream(requested_metrics)
            if not isinstance(returned_metrics, list):
                self.metrics_queue.put([returned_metrics])
            else:
                self.metrics_queue.put(returned_metrics)

    def StreamMetrics(self, request_iterator, context):
        """Dispatches metrics streamed by collector"""
        LOG.debug("StreamMetrics called")
        collect_args = (next(request_iterator))
        max_metrics_buffer = 0
        max_collect_duration = 0
        cfg = Metric(pb=collect_args.Metrics_Arg.metrics[0])
        try:
            max_metrics_buffer = int(cfg.config["max-metrics-buffer"])
        except Exception as ex:
            LOG.debug("Unable to get schedule parameters: {}".format(ex))
        try:
            max_collect_duration = int(cfg.config["max-collect-duration"])
        except Exception as ex:
            LOG.debug("Unable to get schedule parameters: {}".format(ex))
        if max_metrics_buffer > 0:
            self.max_metrics_buffer = max_metrics_buffer
        if max_collect_duration > 0:
            self.max_collect_duration = max_collect_duration
        thread = threading.Thread(target=self._stream_wrapper, args=(collect_args,),)
        thread.daemon = True
        thread.start()

        metrics = []
        metrics_to_stream = []
        while context.is_active():
            try:
                # wait for new metrics until max collect duration timeout
                metrics = self.metrics_queue.get(block=True, timeout=self.max_collect_duration)
            except queue.Empty:
                LOG.debug("Max collect duration exceeded. Streaming metrics")
                for metric in metrics:
                    metrics_to_stream.append(metric)
                metrics_col = CollectReply(Metrics_Reply=MetricsReply(metrics=[m.pb for m in metrics_to_stream]))
                metrics_to_stream = []
                yield metrics_col
            else:
                for metric in metrics:
                    metrics_to_stream.append(metric)
                    if len(metrics_to_stream) == self.max_metrics_buffer:
                        LOG.debug("Max metrics buffer reached. Streaming metrics")
                        metrics_col = CollectReply(
                            Metrics_Reply=MetricsReply(metrics=[m.pb for m in metrics_to_stream]))
                        metrics_to_stream = []
                        yield metrics_col
                # stream metrics if max_metrics_buffer is 0 or enough metrics has been collected
                if self.max_metrics_buffer == 0:
                    LOG.debug("Max metrics buffer set to 0. Streaming metrics")
                    metrics_col = CollectReply(Metrics_Reply=MetricsReply(metrics=[m.pb for m in metrics_to_stream]))
                    metrics_to_stream = []
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
