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

from .plugin_pb2 import ErrReply, GetConfigPolicyReply

LOG = logging.getLogger(__name__)


class PluginProxy(object):
    """Dispatches requests to the plugins implementation"""

    def __init__(self, plugin):
        self.plugin = plugin

    def Ping(self, request, context):
        """Responds to ping request"""
        self.plugin.ping()
        return ErrReply()

    def Kill(self, request, context):
        """Responds to kill request by stopping the gRPC server"""
        self.plugin.stop_plugin()
        return ErrReply()

    def GetConfigPolicy(self, request, context):
        """Dispatches the request to the plugins get_config_policy method"""
        try:
            policy = self.plugin.get_config_policy()
            return policy._pb
        except Exception as err:
            msg = "message: {}\n\nstack trace: {}".format(
                err.message, traceback.format_exc())
            return GetConfigPolicyReply(error=msg)
