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

from snap_plugin.v1.bool_policy import _BoolPolicy, BoolRule
from snap_plugin.v1.config_policy import ConfigPolicy
from snap_plugin.v1.float_policy import _FloatPolicy, FloatRule
from snap_plugin.v1.integer_policy import _IntegerPolicy, IntegerRule
from snap_plugin.v1.string_policy import _StringPolicy, StringRule


def test_config_policy():
    cfg = ConfigPolicy(
        (
            ("acme", "something1"),
            (
                (
                    "asdf",
                    StringRule(default="asdf", required=True),
                ),
                (
                    "myint",
                    IntegerRule(default=1, required=False),
                ),
                (
                    "debug",
                    BoolRule(default=True)
                ),
                (
                    "somefloat",
                    FloatRule(default=1.1, minimum=1.0, maximum=2.0)
                )
            )
        )
    )
    assert len(cfg) == 4
    assert len(cfg["acme.something1"].rules) == 4
    assert cfg["acme.something1"].rules["asdf"].default == "asdf"
    assert cfg["acme.something1"].rules["somefloat"].default == 1.1
    assert cfg["acme.something1"].rules["debug"].default is True
    assert len(cfg._pb.string_policy["acme.something1"].key) == 2
    assert cfg._pb.string_policy["acme.something1"].key == ["acme", "something1"]

    cfg[("acme", "something2")] = _StringPolicy(
        "asdf2",
        StringRule(default="asdf2", required=True),
    )
    assert len(cfg) == 5
