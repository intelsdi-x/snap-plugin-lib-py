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
import sys
import threading
import time
from builtins import int as bigint

import grpc
import pytest
from past.builtins import basestring

import snap_plugin.v1 as snap
from snap_plugin.v1.metrics_arg import MetricsArg
from snap_plugin.v1.plugin_pb2 import CollectorStub, Empty
from snap_plugin.v1.tests import ThreadPrinter


class MockCollector(snap.Collector, threading.Thread):
    """Mock collector plugin """

    def __init__(self, name, ver):
        super(MockCollector, self).__init__(name, ver)
        threading.Thread.__init__(self, group=None, target=None, name=None)
        self._stopper = threading.Event()

    def collect(self, metrics):
        for metric in metrics:
            metric.timestamp = time.time()
            metric.version = 2
            if "bytes" in metric.config and metric.config["bytes"] is True:
                metric.data = b'qwerty'
            elif "string" in metric.config and metric.config["string"] is True:
                metric.data = "qwerty"
            elif "int32" in metric.config and metric.config["int32"] is True:
                metric.data = 99
            elif "int64" in metric.config and metric.config["int64"] is True:
                metric.data = bigint(99)
            elif "bool" in metric.config and metric.config["bool"] is True:
                metric.data = True
            else:
                metric.data = 99.9
        return metrics

    def update_catalog(self, config):
        assert config.IntMap["int"] == 1
        now = time.time()
        metrics = [
            snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="acme"),
                    snap.NamespaceElement(value="sk8"),
                    snap.NamespaceElement(value="matix")
                ],
                unit="some unit",
                description="some description",
                timestamp=now,
            )
        ]
        return metrics

    def get_config_policy(self):
        return snap.ConfigPolicy(
            (
                ("acme", "sk8", "matix"),
                (
                    (
                        "password",
                        snap.StringRule(default="grace", required=True),
                    ),
                    (
                        "user",
                        snap.StringRule(default="kristy", required=True),
                    ),
                )
            )
        )

    def run(self):
        self.start_plugin()

    def stop(self):
        self._stopper.set()
        self.stop_plugin()


@pytest.fixture(scope="module")
def collector_client():
    """Returns a client (grpc) fixture that is passed into collector tests"""
    sys.stdout = ThreadPrinter()
    sys.argv = ["", '{"LogLevel": 1, "PingTimeoutDuration": 5000}']
    col = MockCollector("MyCollector", 99)
    col.start()
    t_end = time.time() + 5
    # wait for our collector to print its preamble
    while len(sys.stdout.lines) == 0 and time.time() < t_end:
        time.sleep(.1)
    resp = json.loads(sys.stdout.lines[0])
    client = CollectorStub(
        grpc.insecure_channel(resp["ListenAddress"]))
    yield client
    col.stop()


def test_monitor():
    sys.argv = ["", '{"LogLevel": 1, "PingTimeoutDuration": 100}']
    col = MockCollector("MyCollector", 1)
    # with a PingTimeoutDuration at 50ms the plugin should shutdown
    # in just over 150ms
    col.start()
    assert col._shutting_down is False
    time.sleep(.4)
    assert col._shutting_down is True


def test_collect(collector_client):
    now = time.time()
    metric = snap.Metric(
        namespace=[snap.NamespaceElement(value="org"),
                   snap.NamespaceElement(value="metric"),
                   snap.NamespaceElement(value="foo")],
        version=1,
        config={"foo": "bar"},
        unit="some unit",
        description="some description",
        timestamp=now)
    reply = collector_client.CollectMetrics(MetricsArg(metric).pb)
    assert reply.error == ''
    assert len(reply.metrics) == 1
    assert reply.metrics[0].Version == 2
    assert reply.metrics[0].float64_data == 99.9
    assert snap.Metric(pb=reply.metrics[0]).data == 99.9
    reply2 = collector_client.CollectMetrics(MetricsArg(metric).pb)
    assert (reply2.metrics[0].Timestamp.sec +
            (reply2.metrics[0].Timestamp.nsec * 10 ** -9)) > (
                reply.metrics[0].Timestamp.sec +
                (reply.metrics[0].Timestamp.nsec * 10 ** -9))


    # collect bytes
    metric.config.clear()
    metric.config["bytes"] = True
    reply = collector_client.CollectMetrics(MetricsArg(metric).pb)
    assert reply.error == ''
    assert snap.Metric(pb=reply.metrics[0]).data == 'qwerty'

    # collect string
    metric.config.clear()
    metric.config["string"] = True
    reply = collector_client.CollectMetrics(MetricsArg(metric).pb)
    assert reply.error == ''
    assert snap.Metric(pb=reply.metrics[0]).data == "qwerty"
    assert isinstance(snap.Metric(pb=reply.metrics[0]).data, basestring)

    # collect int
    metric.config.clear()
    metric.config["int32"] = True
    reply = collector_client.CollectMetrics(MetricsArg(metric).pb)
    assert reply.error == ''
    assert snap.Metric(pb=reply.metrics[0]).data == 99
    assert isinstance(snap.Metric(pb=reply.metrics[0]).data, bigint)

    # collect int64 (long)
    metric.config.clear()
    metric.config["int64"] = True
    reply = collector_client.CollectMetrics(MetricsArg(metric).pb)
    assert reply.error == ''
    assert snap.Metric(pb=reply.metrics[0]).data == 99
    assert isinstance(snap.Metric(pb=reply.metrics[0]).data, bigint)

    # collect int
    metric.config.clear()
    metric.config["bool"] = True
    reply = collector_client.CollectMetrics(MetricsArg(metric).pb)
    assert reply.error == ''
    assert bool(snap.Metric(pb=reply.metrics[0]).data) is True



def test_get_metric_types(collector_client):
    from snap_plugin.v1.get_metrictypes_arg import GetMetricTypesArg
    reply = collector_client.GetMetricTypes(
        GetMetricTypesArg(config={"int": 1}).pb)
    assert reply.error == ''
    assert len(reply.metrics) == 1
    assert reply.metrics[0].Version == 99


def test_get_config_policy(collector_client):
    reply = collector_client.GetConfigPolicy(Empty())
    assert reply.error == ""
    assert reply.string_policy["acme.sk8.matix"].rules["password"].default == "grace"
