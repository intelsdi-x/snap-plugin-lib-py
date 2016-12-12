#!/usr/bin/env python

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
import os
import random
import time

import snap_plugin.v1 as snap

LOG = logging.getLogger(__name__)


class Rand(snap.Collector):
    """Rand

    Exposes random integer and float metrics.  The string metric is does not
    change.  The configuration policy that is exposed by `get_config_policy`
    applies default values for the 'int_min' and 'int_max' config items.
    """

    def collect(self, metrics):
        LOG.debug("CollectMetrics called")
        for metric in metrics:
            switch = {
                "float64": random.random(),
                "string": "bah",
                "int64": random.randint(
                    metric.config["int_min"],
                    metric.config["int_max"]
                    ),
                "*": None
            }
            typ = metric.namespace[1].value
            if typ == "*":
                metric.namespace[1].value = str(os.getpid())
                if metric.namespace[2].value == "uid":
                    metric.data = os.getuid()
                elif metric.namespace[2].value == "gid":
                    metric.data = os.getgid()
            else:
                metric.data = switch[typ]
            metric.timestamp = time.time()
        return metrics

    def update_catalog(self, config):
        LOG.debug("GetMetricTypes called")
        metrics = []
        for key in ("float64", "int64", "string"):
            metric = snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="random"),
                    snap.NamespaceElement(value=key)
                ],
                version=1,
                tags={"mtype": "gauge"},
                description="Random {}".format(key),
            )
            metrics.append(metric)

        metric = snap.Metric(version=1, Description="dynamic element example")
        # adds namespace elements (static and dynamic) via namespace methods
        metric.namespace.add_static_element("random")
        metric.namespace.add_dynamic_element("pid", "current pid")
        metric.namespace.add_static_element("uid")
        metrics.append(metric)

        # metric is added with the namespace defined in the constructor
        metric = snap.Metric(
            namespace=[
                snap.NamespaceElement(value="random"),
                snap.NamespaceElement(name="pid", description="current pid"),
                snap.NamespaceElement(value="gid")
            ],
            description="dynamic element example",
            version=1
        )
        metrics.append(metric)

        return metrics

    def get_config_policy(self):
        LOG.debug("GetConfigPolicy called")
        return snap.ConfigPolicy(
            [
                ("random"),
                [
                    (
                        "int_max",
                        snap.IntegerRule(default=100, minimum=1, maximum=10000)
                    ),
                    (
                        "int_min",
                        snap.IntegerRule(default=0, minimum=0)
                    )
                ]
            ]
        )


if __name__ == "__main__":
    Rand("rand-py", 1).start_plugin()
