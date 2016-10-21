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
import traceback

from .metric import Metric

from .plugin_pb2 import MetricsReply
from .plugin_proxy import PluginProxy

LOG = logging.getLogger(__name__)


class _CollectorProxy(PluginProxy):
    """Dispatches collector requests to the plugins implementation"""
    def __init__(self, collector):
        super(_CollectorProxy, self).__init__(collector)
        self.plugin = collector

    def CollectMetrics(self, request, context):
        """Dispatches the request to the plugins collect method"""
        LOG.debug("CollectMetrics called")
        try:
            metrics_to_collect = []
            for metric in request.metrics:
                metrics_to_collect.append(Metric(pb=metric))
            metrics_collected = self.plugin.collect(metrics_to_collect)
            return MetricsReply(metrics=[m.pb for m in metrics_collected])
        except Exception as err:
            msg = "message: {}\n\nstack trace: {}".format(
                err, traceback.format_exc())
            return MetricsReply(metrics=[], error=msg)

    def GetMetricTypes(self, request, context):
        """Dispatches the request to the plugins update_catalog method"""
        LOG.debug("GetMetricTypes called")
        try:
            metrics = self.plugin.update_catalog(request.config)
            return MetricsReply(metrics=[m.pb for m in metrics])
        except Exception as err:
            msg = "message: {}\n\nstack trace: {}".format(
                err, traceback.format_exc())
            return MetricsReply(metrics=[], error=msg)
