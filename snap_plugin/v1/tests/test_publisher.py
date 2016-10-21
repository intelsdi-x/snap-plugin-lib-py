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

import grpc
import pytest

import snap_plugin.v1 as snap
from snap_plugin.v1.plugin_pb2 import PublisherStub
from snap_plugin.v1.pub_proc_arg import _PublishArg

from . import ThreadPrinter


class MockPublisher(snap.Publisher, threading.Thread):
    """Mock publisher plugin """

    def __init__(self, name, ver):
        super(MockPublisher, self).__init__(name, ver)
        threading.Thread.__init__(self, group=None, target=None, name=None)
        self._stopper = threading.Event()

    def publish(self, metrics, config):
        assert len(config) == 4
        assert config["foo"] == "bar"
        assert config["port"] == 911
        assert config["debug"] is True
        assert config["availability"] == 99.9
        assert len(metrics) > 0
        return metrics

    def get_config_policy(self):
        raise NotImplementedError

    def run(self):
        self.start_plugin()

    def stop(self):
        self._stopper.set()
        self.stopped = True
        self.stop_plugin()


@pytest.fixture(scope="module")
def publisher_client():
    """Returns a client (grpc) fixture that is passed into publisher
    tests """
    sys.stdout = ThreadPrinter()
    pub = MockPublisher("MyPublisher", 1)
    pub.start()
    t_end = time.time() + 5
    # wait for our collector to print its preamble
    while len(sys.stdout.lines) == 0 and time.time() < t_end:
        time.sleep(.1)
    resp = json.loads(sys.stdout.lines[0])
    client = PublisherStub(
        grpc.insecure_channel(resp["ListenAddress"]))
    yield client
    pub.stop()


def test_publish(publisher_client):
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
    config = snap.ConfigMap(foo="bar",
                            port=911,
                            debug=True,
                            availability=99.9)
    reply = publisher_client.Publish(
        _PublishArg(metrics=metrics,
                   config=config).pb
    )
    assert reply.error == ""
