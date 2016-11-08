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

import snap_plugin.v1 as snap

LOG = logging.getLogger(__name__)


class Tag(snap.Processor):
    """Tag

    Adds the tag 'instance-id' to metrics.  The value is provided by the config.
    The plugin exposes a default so if it's not overriden it will be set to
    'xyz-abc-qwerty'.
    """

    def process(self, metrics, config):
        """Processes metrics.

        This method is called by the Snap deamon during the process phase
        of the execution of a Snap workflow.  Examples of processing metrics
        include applying filtering, max, min, average functions as well as
        adding additional context to the metrics to name just a few.

        In this example we are adding a tag called 'context' to every metric.

        Args:
            metrics (obj:`list` of `snap_plugin.v1.Metric`):
                List of metrics to be processed.

        Returns:
            :obj:`list` of `snap_plugin.v1.Metric`:
                List of processed metrics.
        """
        LOG.debug("Process called")
        for metric in metrics:
            metric.tags["instance-id"] = config["instance-id"]
        return metrics

    def get_config_policy(self):
        """Get's the config policy

        The config policy for this plugin defines a string configuration item
        `instance-id` with the default value of `xyz-abc-qwerty`.
        """
        return snap.ConfigPolicy(
            [
                None,
                [
                    (
                        "instance-id",
                        snap.StringRule(default="xyz-abc-qwerty")
                    )
                ]
            ]
        )

if __name__ == "__main__":
    Tag("tag-py", 1).start_plugin()
