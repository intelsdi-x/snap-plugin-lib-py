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

from google.protobuf import json_format

import snap_plugin.v1 as snap

LOG = logging.getLogger(__name__)


class File(snap.Publisher):
    """Example snap file publisher plugin.

    The plugin requires a config option 'file' providing the path of the file
    that metrics will be written to.  The `Metric` will be published to
    the file in JSON.

    """

    def publish(self, metrics, config):
        """Publishes metrics to a file in JSON format.

        This method is called by the Snap deamon during the collection phase
        of the execution of a Snap workflow.

        In this example we are writing the metrics to a file in json format.
        We obtain the path to the file through the config (`ConfigMap`) arg.

        Args:
            metrics (obj:`list` of :obj:`snap_plugin.v1.Metric`):
                List of metrics to be collected.

        Returns:
            :obj:`list` of :obj:`snap_plugin.v1.Metric`:
                List of collected metrics.
        """
        if len(metrics) > 0:
            with open(config["file"], 'a') as outfile:
                for metric in metrics:
                    outfile.write(
                        json_format.MessageToJson(
                            metric._pb, including_default_value_fields=True))

    def get_config_policy(self):
        """As the name suggests this method returns the config policy for the
        plugin.

        This method is called by the Snap deamon when the plugin is loaded.
        A config policy describes the configuration key/value pairs that are
        required, optional, what the value type is and if there is a default
        value.

        In this example we returning a config policy that contains a `string`
        config item describing the location of the file that will be published
        to.  The 'file' config item has a default which the user may choose to
        override.

        Returns:
            `snap_plugin.v1.GetConfigPolicyReply`

        """
        LOG.debug("GetConfigPolicy called")
        return snap.ConfigPolicy(
            [
                None,
                [
                    (
                        "file",
                        snap.StringRule(default="/tmp/snap-py.out")
                    )
                ]
            ],
        )

if __name__ == "__main__":
    File("file-py", 1).start_plugin()
