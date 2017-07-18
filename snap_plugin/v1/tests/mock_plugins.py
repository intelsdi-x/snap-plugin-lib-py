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

import threading
import time
from builtins import int as bigint

import snap_plugin.v1 as snap


class MockCollector(snap.Collector, threading.Thread):
    """Mock collector plugin """

    def __init__(self, name, ver):
        super(MockCollector, self).__init__(name, ver)
        self._flags.add('require-config', snap.plugin.FlagType.toggle, '')
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
        policy = [
            ("acme", "sk8", "matix"),
            [
                (
                    "password",
                    snap.StringRule(default="grace", required=True),
                ),
                (
                    "user",
                    snap.StringRule(default="kristy", required=True),
                ),
            ]
        ]

        if self._args.require_config:
            policy[1].append(("database", snap.StringRule(required=True)))

        return snap.ConfigPolicy(policy)

    def run(self):
        self.start_plugin()

    def stop(self):
        self._stopper.set()
        self.stop_plugin()


class MockProcessor(snap.Processor, threading.Thread):
    """Mock processor plugin """
    def __init__(self, name, ver):
        super(MockProcessor, self).__init__(name, ver)
        threading.Thread.__init__(self, group=None, target=None, name=None)
        self._stopper = threading.Event()

    def process(self, metrics, config):
        for metric in metrics:
            for (k, v) in config.items():
                metric.tags[k] = v
            metric.tags["processed"] = "true"
        return metrics

    def get_config_policy(self):
        return snap.ConfigPolicy(
            [
                None,
                [
                    (
                        "some-config",
                        snap.StringRule(default="some-value")
                    )
                ]
            ],
        )

    def run(self):
        self.start_plugin()

    def stop(self):
        self._stopper.set()
        self.stopped = True
        self.stop_plugin()


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


class MockStreamCollector(snap.StreamCollector, threading.Thread):
    """Mock streaming plugin """

    def __init__(self, name, ver):
        super(MockStreamCollector, self).__init__(name, ver)
        self._flags.add('require-config', snap.plugin.FlagType.toggle, '')
        threading.Thread.__init__(self, group=None, target=None, name=None)
        self._stopper = threading.Event()

    def stream(self):
        while True:
            now = time.time()
            metric = snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="streaming"),
                    snap.NamespaceElement(value="random"),
                    snap.NamespaceElement(value="int")
                ],
                version=1,
                tags={"mtype": "counter"},
                description="some description".format("int"),
                timestamp=now,
                data=200
            )
            self.proxy.metrics_queue.put(metric)
            time.sleep(1)

    def update_catalog(self, config):
        metrics = [
            snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="streaming"),
                    snap.NamespaceElement(value="random"),
                    snap.NamespaceElement(value="int")
                ],
                unit="some unit",
                description="some description",
            )
        ]
        return metrics

    def get_config_policy(self):
        policy = [
            ("intel", "streaming", "random"),
            [
                (
                    "password",
                    snap.StringRule(default="pass", required=True),
                ),
                (
                    "user",
                    snap.StringRule(default="user", required=True),
                ),
            ]
        ]

        if self._args.require_config:
            policy[1].append(("database", snap.StringRule(required=True)))

        return snap.ConfigPolicy(policy)

    def run(self):
        self.start_plugin()

    def stop(self):
        self._stopper.set()
        self.stop_plugin()
