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

import json
import logging
import sys
import time
from abc import ABCMeta, abstractmethod
from concurrent import futures
from enum import Enum
from threading import Thread

import grpc
import six

from .plugin_pb2 import GetConfigPolicyReply

LOG = logging.getLogger(__name__)


class _EnumEncoder(json.JSONEncoder):
    # pylint: disable=E0202
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return json.JSONEncoder.default(self, obj)


class RoutingStrategy(Enum):
    """Plugin routing strategies

    - lru (default): Least recently used
        Calls are routed to the least recently called plugin instance.
    - sticky: Sticky based routing
        Calls are routed to the same instance of the running plugin.  See
        :py:class:`Meta` its attribute `concurrency_count`.
    - config: Config based routing
        Calls are routed based on the configuration matching.  In this case
        multiple tasks could be configured with the same configuration in which
        case the framework will route calls to only those running instances with
        a configuration matching the task that is firing.

    """
    lru = 0
    sticky = 1
    config = 2


class PluginType(Enum):
    """Plugin types """
    collector = 0
    processor = 1
    publisher = 2


class PluginResponseState(Enum):
    """Plugin response states"""
    plugin_success = 0
    plugin_failure = 1


class RPCType(Enum):
    """Snap RPC types"""
    native = 0
    json = 1
    grpc = 2


class Meta(object):
    """Snap plugin meta

    Arguments:
        type (:py:class:`PluginType`): Plugin type
        name (:obj:`string`): Plugin name
        version (:obj:`int`): Plugin version
        concurrency_count (:obj:`int`): ConcurrencyCount is the max number
            concurrent calls the plugin may take. If there are 5 tasks using the
            plugin and concurrency count is 2 there will be 3 plugins running.
        routing_strategy (:py:class:`RoutingStrategy`): RoutingStrategy will
            override the routing strategy this plugin requires.  The default
            routing strategy is least-recently-used.
        exclusive (:obj:`bool`): Exclusive results in a single instance of the
            plugin running regardless the number of tasks using the plugin.
        cache_ttl (:obj:`int`): CacheTTL will override the default cache TTL
            for the provided plugin and the metrics it exposes (default=500ms).
        rpc_type (:py:class:`RPCType`)> RPC type
        rpc_version (:obj:`int`): RPC version
        unsecure (:obj:`bool`): Unsecure
    """
    def __init__(self,
                 type,
                 name,
                 version,
                 concurrency_count=5,
                 routing_strategy=RoutingStrategy.lru,
                 exclusive=False,
                 cache_ttl=None,
                 rpc_type=RPCType.grpc,
                 rpc_version=1,
                 unsecure=True):
        self.name = name
        self.version = version
        setattr(sys.modules["snap_plugin.v1"], "PLUGIN_VERSION", version)
        self.type = type
        self.concurrency_count = concurrency_count
        self.routing_strategy = routing_strategy
        self.exclusive = exclusive
        self.cache_ttl = cache_ttl
        self.rpc_type = rpc_type
        self.rpc_version = rpc_version
        self.unsecure = unsecure


@six.add_metaclass(ABCMeta)
class Plugin(object):
    """Abstract base class for Collector, Processor and Publisher plugins.

    Plugin authoris shoud not inherit directly from this class rather they
    should inherit from :py:class:`snap_plugin.v1.collector.Collector`,
    :py:class:`snap_plugin.v1.processor.Processor` or
    :py:class:`snap_plugin.v1.publisher.Publisher`.
    """

    def __init__(self):
        self.meta = None
        self.proxy = None
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self._port = 0
        self._last_ping = time.time()
        self._shutting_down = False
        self._monitor = None
        # process the arg (valid json) provided by the framework
        if len(sys.argv) > 1:
            try:
                self._args = json.loads(sys.argv[1])
            except ValueError:
                LOG.warning("Invalid arg provided: expected JSON. " +
                            "(provided={})".format(sys.argv[1]))
                self._args = {}
        else:
            self._args = {}
        self._set_log_level()
        self._monitor = Thread(
            target=_monitor,
            args=(self.last_ping,
                  self.stop_plugin,
                  self._is_shutting_down),
            kwargs={"timeout": self._get_ping_timout_duration()})

    def ping(self):
        """Ping responds to clients providing proof of life

        The Snap framework will ping plugins every 1.5s to confirm they are not
        hung.
        """
        self._last_ping = time.time()

    def stop_plugin(self):
        """Stops the plugin"""
        LOG.debug("plugin stopping")
        self._shutting_down = True
        _stop_event = self.server.stop(0)
        while not _stop_event.is_set():
            time.sleep(.1)
        LOG.debug("plugin stopped")

    def start_plugin(self):
        """Starts the Plugin

        Starting a plugin includes:
            - Finding an available port
            - Starting the gRPC server
            - Printing to STDOUT data (JSON) for handshaking with Snap
        """
        return
        LOG.debug("plugin start called..")
        # start grpc server
        self._port = self.server.add_insecure_port('127.0.0.1:{!s}'.format(0))
        self.server.start()
        sys.stdout.write(json.dumps(
            {
                "Meta": {
                    "Name": self.meta.name,
                    "Version": self.meta.version,
                    "Type": self.meta.type,
                    "RPCType": self.meta.rpc_type,
                    "RPCVersion": self.meta.rpc_version,
                    "ConcurrencyCount": self.meta.concurrency_count,
                    "Exclusive": self.meta.exclusive,
                    "Unsecure": self.meta.unsecure,
                    "CacheTTL": self.meta.cache_ttl,
                    "RoutingStrategy": self.meta.routing_strategy,
                },
                "ListenAddress": "127.0.0.1:{!s}".format(self._port),
                "Token": None,
                "PublicKey": None,
                "Type": self.meta.type,
                "ErrorMessage": None,
                "State": PluginResponseState.plugin_success,
            },
            cls=_EnumEncoder
        )+"\n")
        sys.stdout.flush()
        self._monitor.start()
        self._monitor.join()
        sys.exit()

    def _set_log_level(self):
        """Sets the log level provided by the framework.

        If no log level is passed the level is set to Warn.

        Snap communicates the following log levels to plugins.
            - 1 debug
            - 2 info
            - 3 warn
            - 4 error
            - 5 fatal
            - 6 panic
        """
        if "LogLevel" in self._args:
            if self._args["LogLevel"] >= 1 and self._args["LogLevel"] <= 5:
                # Multiplying the provided level by 10 will convert them to what
                # the python logging module uses.
                LOG.setLevel(self._args["LogLevel"] * 10)
                LOG.info("Setting loglevel to %s.", LOG.getEffectiveLevel())
            else:
                LOG.error("The log level should be between 1 and 5." +
                          " (given={})", self._args["LogLevel"])

    def _get_ping_timout_duration(self):
        """Gets the ping timout duration provided by the framework.

        The ping timeout duration returned from the framework is in ms. so we
        convert it to seconds.  If the is no timeout provided by the framework
        we return the default of 5(seconds).
        """
        if "PingTimeoutDuration" in self._args:
            return self._args["PingTimeoutDuration"] / 1000
        else:
            return 5

    def last_ping(self):
        """Returns the epoch time when the last ping was received"""
        return self._last_ping

    def _is_shutting_down(self):
        """Returns bool indicating whether the plugin is shutting down"""
        return self._shutting_down

    @abstractmethod
    def get_config_policy(self):
        """Returns the config policy for a plugin.

        The config policy for a plugin includes config value types (Integer,
        (Float, String and Bool) and rules which includes default values and
        min and max constraints for Float and Integery value types.

        Args:
            None

        Returns:
            :py:class:`snap_plugin.v1.config_policy.ConfigPolicy`

        """
        return GetConfigPolicyReply()


def _monitor(last_ping, stop_plugin, is_shutting_down, timeout=5):
    """Monitors health checks (pings) from the Snap framework.

    If the plugin doesn't recieve 3 consecutive health checks from Snap the
    plugin will shutdown.  The default timeout is set to 5 seconds.
    """
    _timeout_count = 0
    _last_check = time.time()
    _sleep_interval = 1
    # set _sleep_interval if less than the timeout
    if timeout < _sleep_interval:
        _sleep_interval = timeout
    while True:
        time.sleep(_sleep_interval)
        # Signals that stop_plugin has been called
        if is_shutting_down():
            return
        # have we missed a ping during the last timeout duration
        if ((time.time() - _last_check) > timeout) and ((time.time() - last_ping()) > timeout):
            # reset last_check
            _last_check = time.time()
            _timeout_count += 1
            LOG.warning("Missed ping health check from the framework. " +
                        "({} of 3)".format(_timeout_count))
            if _timeout_count >= 3:
                stop_plugin()
                return
        elif (time.time() - last_ping()) <= timeout:
            _timeout_count = 0
