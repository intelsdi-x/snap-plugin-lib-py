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
from http.client import HTTPConnection
from threading import Thread

import pytest

from snap_plugin.v1.collector import Collector
from snap_plugin.v1.processor import Processor
from snap_plugin.v1.publisher import Publisher

from .mock_plugins import MockCollector


def test_collector():
    with pytest.raises(TypeError) as excinfo:
        Collector("name", 1)
    assert "Can't instantiate abstract class Collector" in str(excinfo.value)


def test_processor():
    with pytest.raises(TypeError) as excinfo:
        Processor("name", 1)
    assert "Can't instantiate abstract class Processor" in str(excinfo.value)


def test_publisher():
    with pytest.raises(TypeError) as excinfo:
        Publisher("name", 1)
    assert "Can't instantiate abstract class Publisher" in str(excinfo.value)


def test_standalone(capsys, caplog):
    sys.argv = ["", "--stand-alone", "--stand-alone-port", "0"]
    col = MockCollector("MyCollector", 1)
    thread = Thread(target=col.start)
    thread.start()

    # wait for stand alone server to start
    time.sleep(.2)
    out, _ = capsys.readouterr()
    out = out.split()
    address, port = out[-1].split(':')

    connection = HTTPConnection(address, int(port), timeout=5)
    connection.request("GET", "/")
    response = connection.getresponse()
    assert response.status == 200
    data = response.read()
    connection.close()

    # response should be valid json
    preamble = json.loads(data.decode('utf-8'))
    # response should be valid preamble
    assert "Meta" and "ListenAddress" in preamble

    # try to start a standalone plugin on port already in use
    sys.argv = ["", "--stand-alone", "--stand-alone-port", port]
    col2 = MockCollector("MyCollector", 1)
    col2.start()
    time.sleep(.2)
    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == 40

    col.standalone_server.shutdown()
