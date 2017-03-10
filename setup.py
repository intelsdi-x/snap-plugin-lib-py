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
from setuptools import setup, find_packages
import versioneer

setup(
    name="snap-plugin-lib-py",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=['grpcio>=1.1.3,<2', 'protobuf>=3.2.0,<4',
                      'futures>=3.0.5', 'future>=0.16.0'],
    author="Joel Cooklin",
    author_email="joel.cooklin@gmail.com",
    description="This is a lib for creating plugins for the Snap telementry "
                "framework.",
    long_description_markdown_filename="README.md",
    license="Apache 2.0",
    keywords="snap telemetry plugin plugins metrics",
    url="http://github.com/intelsdi-x/snap-plugin-lib-py"
)
