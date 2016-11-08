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

from .plugin_pb2 import ErrReply
from .config_map import ConfigMap
from .metric import Metric
from .plugin_proxy import PluginProxy

LOG = logging.getLogger(__name__)


class PublisherProxy(PluginProxy):
    """Dispatches publisher requests to the plugins implementation"""
    def __init__(self, publisher):
        super(PublisherProxy, self).__init__(publisher)
        self.plugin = publisher

    def Publish(self, request, context):
        """Dispatches the request to the plugins publish method"""
        LOG.debug("Publish called")
        try:
            self.plugin.publish(
                [Metric(pb=m) for m in request.Metrics],
                ConfigMap(pb=request.Config)
            )
            return ErrReply()
        except Exception as err:
            msg = "message: {}\n\nstack trace: {}".format(
                err, traceback.format_exc())
            return ErrReply(error=msg)
