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

import grpc
import pytest

import snap_plugin.v1 as snap
from snap_plugin.v1.plugin_pb2 import ProcessorStub, Empty
from snap_plugin.v1.pub_proc_arg import _ProcessArg

from . import ThreadPrinter
from .mock_plugins import MockProcessor


@pytest.fixture(scope="module")
def processor_client():
    """Returns a client (grpc) fixture that is passed into processor
    tests """
    sys.stdout = ThreadPrinter()
    sys.argv = ["", '{}']
    proc = MockProcessor("MyProcessor", 1)
    proc.start()
    t_end = time.time() + 5
    # wait for our collector to print its preamble
    while len(sys.stdout.lines) == 0 and time.time() < t_end:
        time.sleep(.1)
    resp = json.loads(sys.stdout.lines[0])
    client = ProcessorStub(
        grpc.insecure_channel(resp["ListenAddress"]))
    yield client
    proc.stop()


def test_process(processor_client):
    now = time.time()
    metrics = [
        snap.Metric(
            namespace=[
                snap.NamespaceElement(value="org"),
                snap.NamespaceElement(value="metric"),
                snap.NamespaceElement(value="foo")
            ],
            version=1,
            unit="some unit",
            description="some description",
            timestamp=now,
        )
    ]
    config = snap.ConfigMap(foo="bar")
    reply = processor_client.Process(
        _ProcessArg(metrics=metrics,
                   config=config).pb
    )
    assert reply.error == ""
    assert len(reply.metrics) == 1
    for m in reply.metrics:
        assert "processed" in m.Tags
        assert m.Tags["processed"] == "true"
        assert "foo" in m.Tags
        assert m.Tags["foo"] == "bar"


def test_get_config_policy(processor_client):
    reply = processor_client.GetConfigPolicy(Empty())
    assert reply.error == ""
    assert reply.string_policy[""].rules["some-config"].default == "some-value"
