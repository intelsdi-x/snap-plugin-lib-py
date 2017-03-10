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

"""This is a module for writing python plugins for the `Snap telemetry
framework <https://github.com/intelsdi-x/snap>`_.

This module provides provides everything you need to write a
:ref:`collector-label`, :ref:`processor-label` or :ref:`publisher-label`
plugin for Snap.  For more details checkoout the plugin authoring details at
https://intelsdi-x.github.io/snap-plugin-lib-py/.

"""

__all__ = ['Collector', 'Processor', 'Publisher', 'Metric', 'Namespace',
           'NamespaceElement', 'ConfigMap', 'StringRule', 'IntegerRule',
           'BoolRule', 'FloatRule', 'ConfigPolicy']

import logging
import sys

from .collector import Collector
from .processor import Processor
from .publisher import Publisher
from .metric import Metric
from .namespace import Namespace
from .namespace_element import NamespaceElement
from .config_map import ConfigMap
from .config_policy import ConfigPolicy
from .string_policy import StringRule
from .integer_policy import IntegerRule
from .bool_policy import BoolRule
from .float_policy import FloatRule
from ._version import get_versions

LOG = logging.getLogger()
_OUT_HDLR = logging.StreamHandler(sys.stderr)
_OUT_HDLR.setFormatter(logging.Formatter("""%(asctime)s - %(name)s - \
%(levelname)s - %(message)s"""))
_OUT_HDLR.setLevel(logging.DEBUG)
LOG.addHandler(_OUT_HDLR)
LOG.setLevel(logging.DEBUG)

PLUGIN_VERSION = 0

__version__ = get_versions()['version']
del get_versions
