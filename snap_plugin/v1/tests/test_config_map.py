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

import pytest

from snap_plugin.v1.config_map import ConfigMap


class TestConfigMap(object):

    def test_constructor(self):
        # empty
        cfg = ConfigMap()
        assert len(cfg) == 0
        # kwargs
        cfg = ConfigMap(int=1, string="asdf", bool=True, float=1.1)
        assert len(cfg) == 4
        assert len(cfg._pb.IntMap) == 1        
        assert (len(cfg._pb.StringMap) == 1 and len(cfg._pb.IntMap) == 1 and
                len(cfg._pb.FloatMap) == 1 and len(cfg._pb.BoolMap) == 1)
        # args
        cfg = ConfigMap(("int", 1), ("string", "asdf"), ("bool", True),
                        ("float", 1.1))
        assert len(cfg) == 4
        assert (len(cfg._pb.StringMap) == 1 and len(cfg._pb.IntMap) == 1 and
                len(cfg._pb.FloatMap) == 1 and len(cfg._pb.BoolMap) == 1)
        # kwargs and args
        cfg = ConfigMap(("int", 1), ("string", "asdf"), bool=True, float=1.1)
        assert len(cfg) == 4
        assert (len(cfg._pb.StringMap) == 1 and len(cfg._pb.IntMap) == 1 and
                len(cfg._pb.FloatMap) == 1 and len(cfg._pb.BoolMap) == 1)

    def test_set_get(self):
        cfg = ConfigMap()
        cfg["string"] = "asdf"
        cfg["int"] = 1
        cfg["float"] = 1.1
        cfg["bool"] = True
        assert len(cfg) == 4
        assert (len(cfg._pb.StringMap) == 1 and len(cfg._pb.IntMap) == 1 and
                len(cfg._pb.FloatMap) == 1 and len(cfg._pb.BoolMap) == 1)
        assert (cfg._pb.StringMap["string"] == "asdf" and
                cfg._pb.IntMap["int"] == 1 and
                cfg._pb.FloatMap["float"] == 1.1 and
                cfg._pb.BoolMap["bool"] == True)

    def test_keys_values(self):
        cfg = ConfigMap(("int", 1), ("string", "asdf"), ("bool", True),
                        ("float", 1.1))
        keys = cfg.keys()
        assert len(keys) == 4
        assert ("int" in keys and "float" in keys and
                "bool" in keys and "string" in keys)

        values = cfg.values()
        assert len(values) == 4
        assert (1 in values and 1.1 in values and
                "asdf" in values and True in values)

    def test_delete_clear(self):
        cfg = ConfigMap(("int", 1), ("string", "asdf"), ("bool", True),
                        ("float", 1.1))
        del(cfg["int"])
        assert len(cfg) == 3
        assert "int" not in cfg.keys()

        del(cfg["bool"])
        assert len(cfg) == 2
        assert "bool" not in cfg.keys()

        cfg.clear()
        assert len(cfg) == 0
        assert len(cfg.keys()) == 0
        assert len(cfg.values()) == 0

    def test_update(self):
        cfg = ConfigMap(("int", 1), ("string", "asdf"), ("bool", True),
                        ("float", 1.1))
        # provided a tuple that exists
        cfg.update(("int", 2))
        assert cfg["int"] == 2
        assert len(cfg) == 4
        # provided a tuple that doesn't exist
        cfg.update(("another_int", 3))
        assert cfg["another_int"] == 3
        assert len(cfg) == 5
        # provided a kwarg that exists
        cfg.update(string="qwerty")
        assert cfg["string"] == "qwerty"
        assert len(cfg) == 5
        # provided a kwarg that doesn't exist
        cfg.update(another_string="zxcv")
        assert cfg["another_string"] == "zxcv"
        assert len(cfg) == 6

    def test_iters(self):
        cfg = ConfigMap(("int", 1), ("string", "asdf"), ("bool", True),
                        ("float", 1.1))
        # iteritems
        size = len(cfg)
        count = 0
        for k, v in cfg.iteritems():
            count += 1
            assert k in cfg
        assert size == count
        # iterkeys
        count = 0
        for k in cfg.iterkeys():
            count += 1
            assert k in cfg
        assert size == count
        # itervalues
        count = 0
        for v in cfg.itervalues():
            count += 1
            assert v in cfg.values()
        assert size == count

    def test_pop(self):
        cfg = ConfigMap(("int", 1), ("string", "asdf"), ("bool", True),
                        ("float", 1.1))
        # item exists
        value = cfg.pop("string")
        assert value == "asdf"
        assert len(cfg) == 3
        assert "string" not in cfg

        # item doesn't exist (default provided)
        value = cfg.pop("string", default="oops")
        assert value == "oops"
        assert len(cfg) == 3
        assert "string" not in cfg

        # item doesn't exist (default not provided)
        with pytest.raises(KeyError) as err:
            cfg.pop("foo")
        assert str(err.value) == "'foo'"
        assert len(cfg) == 3

    def test_popitem(self):
        cfg = ConfigMap(("int", 1), ("string", "asdf"), ("bool", True),
                        ("float", 1.1))
        (key, value) = cfg.popitem()
        assert len(cfg) == 3
