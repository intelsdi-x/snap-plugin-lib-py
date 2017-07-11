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
import time
from builtins import int as bigint

import grpc
import pytest
from past.builtins import basestring

import snap_plugin.v1 as snap
from snap_plugin.v1.metrics_arg import MetricsArg
from snap_plugin.v1.plugin_pb2 import CollectorStub, Empty
from snap_plugin.v1.tests import ThreadPrinter

from .mock_plugins import MockCollector


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


def test_diagnostics(capsys, caplog):
    sys.argv = ["", "--config", '{"database": "123", "password": "321", "user": "admin"}', "--require-config"]
    col = MockCollector("MyCollector", 99)

    # run diagnostics and capture output
    col.start_plugin()
    out, _ = capsys.readouterr()
    lines = out.split('\n')

    # assert there are no logged errors
    for record in caplog.records:
        assert record.levelno < 40

    # check if output of each part of diagnostic print is correct

    CONFIG_OFFSET = 8
    CPOLICY_OFFSET = CONFIG_OFFSET + 2
    CATALOG_OFFSET = CPOLICY_OFFSET + 2
    METRIC_OFFSET = CATALOG_OFFSET + 3
    CONFIG_TIMER_MSG_LEN = CATALOG_TIMER_MSG_LEN = 15
    CATALOG_MSG_LEN = 14
    METRIC_MSG_LEN = 12
    METRIC_TIMER_MSG_LEN = 18

    assert lines[0] == "Runtime Details:"

    assert lines[CONFIG_OFFSET] == "Config Policy:"
    mock_cpolicy = [
        ("acme.sk8.matix", "password", "string", "True", "grace"),
        ("acme.sk8.matix", "database", "string", "True"),
        ("acme.sk8.matix", "user", "string", "True", "kristy"),
    ]
    cpolicy = []
    offset = len(mock_cpolicy)
    for index in range(len(mock_cpolicy)):
        fields = tuple(lines[CPOLICY_OFFSET + index].split())
        cpolicy.append(fields)

    def sort_by_key(policy): return policy[1]
    for mock_policy, policy in zip(sorted(mock_cpolicy, key=sort_by_key), sorted(cpolicy, key=sort_by_key)):
        assert mock_policy == policy
    assert lines[CPOLICY_OFFSET + offset][:CONFIG_TIMER_MSG_LEN] == "Printing config"

    assert lines[CATALOG_OFFSET + offset][:CATALOG_MSG_LEN] == "Metric catalog"
    mock_namespaces = ["/acme/sk8/matix"]
    for index, ns in enumerate(mock_namespaces):
        assert lines[13 + offset + index].strip() == ns
    offset += len(mock_namespaces)
    assert lines[CATALOG_OFFSET + 1 + offset][:CATALOG_TIMER_MSG_LEN] == "Printing metric"

    mock_metrics = [("/acme/sk8/matix", "float", "99.9")]
    assert lines[METRIC_OFFSET + offset][:METRIC_MSG_LEN] == "Metrics that"
    for index, metric in enumerate(mock_metrics):
        fields = tuple(lines[METRIC_OFFSET + 2 + offset + index].split())
        assert fields == metric
    offset += len(mock_metrics)
    assert lines[METRIC_OFFSET + 2 + offset][:METRIC_TIMER_MSG_LEN] == "Printing collected"

    # run plugin with flag '--require-config' which makes it require field 'database' in config
    sys.argv = ["", "--config", '{"password": "123", "user": "321"}', "--require-config"]
    col = MockCollector("MyCollector", 99)

    col.start_plugin()
    # we didn't provide necessary config field so we should get error logs
    errors = list(filter(lambda r: r.levelno >= 40, caplog.records))
    assert len(errors) > 0


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
