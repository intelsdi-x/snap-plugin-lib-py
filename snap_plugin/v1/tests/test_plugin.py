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
import os
import pytest
import stat
import sys
import time
from enum import Enum

from http.client import HTTPConnection
from threading import Thread

from snap_plugin.v1.collector import Collector
from snap_plugin.v1.plugin import Plugin, Meta, MissingRequiredArgument, PluginType
from snap_plugin.v1.processor import Processor
from snap_plugin.v1.publisher import Publisher

from .mock_plugins import MockCollector


def _test_tls_vars_set(plugin):
    # Create the files for test
    root_cert = "root.crt"
    server_cert = "server.crt"
    private_key = "private.key"
    open(root_cert, "w+")
    open(server_cert, "w+")
    open(private_key, "w+")
    # Make up proper input args
    sys.argv = [
        "test_plugin"
        "--tls",
        "--root-cert-paths", root_cert,
        "--cert-path", server_cert,
        "--key-path", private_key,
        ]
    plugin._parse_args()
    plugin._tls_setup()
    # Check that the proper variables are set
    assert plugin.meta.tls
    assert plugin.meta.root_cert_paths == [root_cert]
    assert plugin.meta.server_cert_path == server_cert
    assert plugin.meta.private_key_path == private_key
    # Remove the test files
    os.remove(root_cert)
    os.remove(server_cert)
    os.remove(private_key)


def _test_tls_bad_file_raises_exc(plugin):
    # Create the files for test
    root_cert = "root.crt"
    server_cert = "server.crt"
    private_key = "private.key"
    # Make up proper input args
    sys.argv = [
        "test_plugin",
        "--tls",
        "--root-cert-paths", root_cert,
        "--cert-path", server_cert,
        "--key-path", private_key,
        ]
    plugin._parse_args()
    plugin._tls_setup()
    with pytest.raises(Exception) as excinfo:
        plugin._generate_tls_credentials()
    assert "No such file or directory" in str(excinfo.value)


def test_tls():
    # Generate a derived type of Plugin for testing purposes
    derived = type('Derived', (Plugin,), {'get_config_policy': None})

    def override(self):
        return ""
    setattr(derived, 'get_config_policy', override)
    plugin = derived()
    # If a meta is not created first, then this test fails
    # on a None type error. Here we set Meta.
    plugin.meta = Meta(derived, "mytest", 1)
    _test_tls_vars_set(plugin)
    plugin = derived()
    plugin.meta = Meta(derived, "mytest", 1)
    _test_tls_bad_file_raises_exc(plugin)

class DummyServer(json.JSONEncoder):
    def add_secure_port(*args, **kwargs):
        pass
    
    def add_insecure_port(*args, **kwargs):
        pass
    
    @staticmethod
    def start():
        pass
    
    def default(self, obj):
        if isinstance(obj, object):
            return obj.__dict__
        return json.JSONEncoder().encode(obj)


tls_emits_valid_meta_args_input = {
    '0': ["test_plugin", '{"CertPath":"libtest-srv.crt","KeyPath":"libtest-srv.key","RootCertPaths":"libtest-ca.crt","TLSEnabled":true}'],
    '1': ["test_plugin", '{"CertPath":"libtest-srv.crt","KeyPath":"libtest-srv.key","RootCertPaths":"libtest-ca.crt:libtest-BADCA.crt","TLSEnabled":true}'],
    '2': ["test_plugin", '{"TLSEnabled":false}'],
    '3': ["test_plugin", "--stand-alone", '{"TLSEnabled":false}'],
    '4': ["test_plugin", "--stand-alone", '{"CertPath":"libtest-srv.crt","KeyPath":"libtest-srv.key","RootCertPaths":"libtest-ca.crt","TLSEnabled":true}']
}
tls_emits_valid_meta_output = {
    '0': '{"CertPath": "libtest-srv.crt", "KeyPath": "libtest-srv.key", "RootCertPaths": ["libtest-ca.crt"], "TLSEnabled": true}',
    '1': '{"CertPath": "libtest-srv.crt", "KeyPath": "libtest-srv.key", "RootCertPaths": ["libtest-ca.crt", "libtest-BADCA.crt"], "TLSEnabled": true}',
    '2': '{"CertPath": null, "KeyPath": null, "RootCertPaths": null, "TLSEnabled": false}',
    '3': '{"CertPath": null, "KeyPath": null, "RootCertPaths": null, "TLSEnabled": false}',
    '4': '{"CertPath": "libtest-srv.crt", "KeyPath": "libtest-srv.key", "RootCertPaths": ["libtest-ca.crt"], "TLSEnabled": true}'
}

@pytest.mark.parametrize(["data_id"], "0 1 2 3 4".split())
def test_tls_emits_valid_meta(data_id, tmpdir):
    args_input = tls_emits_valid_meta_args_input[data_id]
    preamble_output = tls_emits_valid_meta_output[data_id]
    sys.argv = args_input
    # Generate a derived type of Plugin for testing purposes, skip generating tls credentials with its file checking
    derived = type('Derived', (Plugin,), {'get_config_policy': None, '_generate_tls_credentials': None})

    def override(self):
        return ""
    setattr(derived, 'get_config_policy', override)
    setattr(derived, '_generate_tls_credentials', override)
    plugin = derived()
    plugin.server = DummyServer()
    plugin.meta = Meta(PluginType.collector, "mytest", 1)
    plugin._parse_args()
    preamble_meta = json.loads(plugin._generate_preamble_and_serve())["Meta"]
    # filter non-TLS properties from generated Meta
    preamble_meta = {k: preamble_meta[k] for k in preamble_meta if k in "CertPath KeyPath RootCertPaths TLSEnabled".split()}
    actual_out = json.dumps(preamble_meta, sort_keys=True)
    expect_out = json.dumps(json.loads(preamble_output), sort_keys=True)
    assert actual_out == expect_out

tls_reads_root_certs_input_rootpaths = {
    "0": "foo0.crt:bar0.crt",
    "1": "foo1BAD.crt",
    "2": "foo2.crt:bar2BAD.crt",
    "3": "foo3/:foo3/bar3.crt",
    "4": "foo4/:foo4/bar4.crt:foo4/hop4BAD.crt",
    "5": "foo5/:foo5/bar5.crt:hop5/:hop5/lol5BAD.crt",
    "6": "foo6BAD.crt:bar6BAD.crt",
}

tls_reads_root_certs_output_badfile = {
    "0": None, "1": "foo1BAD.crt", "2": "bar2BAD.crt", "3": None, "4": "hop4BAD.crt", "5": "lol5BAD.crt", "6": "foo6BAD.crt"
}

@pytest.mark.parametrize(["data_id"], "0 1 2 3 4 5 6".split())
def test_tls_reads_root_certs(tmpdir, data_id):
    def _make_root_cert_files(paths, basedir):
        pathlist = paths.split(":")
        res_pathlist = []
        res_rawfiles = []
        for path in pathlist:
            fpath = os.path.join(basedir, path)
            if "/" not in path or path.endswith("/"):
                res_pathlist.append(os.path.join(basedir, path.rstrip("/")))
            if path.endswith("/"):
                os.makedirs(fpath)
                continue
            else:
                res_rawfiles.append(os.path.basename(path))
            with open(fpath, "w") as f:
                f.write("test")
            if "BAD" in path:
                os.chmod(fpath, stat.S_IWUSR | stat.S_IXUSR)
        return ":".join(res_pathlist), res_rawfiles

    _make_root_cert_files("server.crt:server.key", basedir=str(tmpdir.dirpath()))
    rootpaths, rawfiles = _make_root_cert_files(tls_reads_root_certs_input_rootpaths[data_id], basedir=str(tmpdir.dirpath()))
    badfile = tls_reads_root_certs_output_badfile[data_id]

    derived = type('Derived', (Plugin,), {'get_config_policy': None})

    def override(self):
        return ""
    setattr(derived, 'get_config_policy', override)
    plugin = derived()
    plugin.server = DummyServer()
    plugin.meta = Meta(PluginType.collector, "mytest", 1)

    # Make up proper input args
    sys.argv = [
        "test_plugin",
        "--tls",
        "--root-cert-paths", rootpaths,
        "--cert-path", "server.crt",
        "--key-path", "server.key",
        ]
    plugin._parse_args()
    plugin._tls_setup()
    with pytest.raises(Exception) as excinfo:
        plugin._generate_tls_credentials()
    if badfile is not None:
        assert badfile in str(excinfo.value)
    else:
        for rawfile in rawfiles:
            assert rawfile not in str(excinfo.value)


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
    sys.argv = ["test_plugin", "--stand-alone", "--stand-alone-port", "0"]
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
