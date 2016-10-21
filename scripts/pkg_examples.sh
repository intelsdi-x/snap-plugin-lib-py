#!/bin/bash

#http://www.apache.org/licenses/LICENSE-2.0.txt
#
#
#Copyright 2016 Intel Corporation
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

set -e
set -u
set -o pipefail

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__proj_dir="$(dirname "$__dir")"

. "${__dir}/common.sh"

_debug "verifying we are running on a Linux system"
if [[ $OSTYPE != "linux-gnu" ]]
then
    _error "This script can only be run from a Linux system"
    exit 1
fi

_debug "checking for acbuild"
if ! which acbuild > /dev/null
then
	_error "Error: acbuild not installed"
    _info "hint: see https://github.com/containers/build"
	exit 1
fi

if [ -z "$VIRTUAL_ENV" ]; then
    echo "Need to set VIRTUAL_ENV"
    _info "hint: see https://github.com/yyuu/pyenv"
    exit 1
fi

_info "packaging ${__proj_dir}/examples/collector/rand.py"
_info "running: acbuild begin"
acbuild begin
_info "running: acbuild set-name randpy"
acbuild set-name randpy
_info "running: acbuild copy $VIRTUAL_ENV .venv"
acbuild copy $VIRTUAL_ENV .venv
_info "running: acbuild copy ${__proj_dir}/examples/collector/rand.py rand.py"
acbuild copy ${__proj_dir}/examples/collector/rand.py rand.py
_info "running: acbuild set-exec ./.venv/bin/python rand.py"
acbuild set-exec ./.venv/bin/python rand.py
_info "running: acbuild write ${__proj_dir}/snap-plugin-collector-randpy-linux-x86_64.aci"
acbuild write ${__proj_dir}/snap-plugin-collector-randpy-linux-x86_64.aci
_info "running: acbuild end"
acbuild end

_info "packaging ${__proj_dir}/examples/processor/tag.py"
_info "running: acbuild begin"
acbuild begin
_info "running: acbuild set-name tagpy"
acbuild set-name randpy
_info "running: acbuild copy $VIRTUAL_ENV .venv"
acbuild copy $VIRTUAL_ENV .venv
_info "running: acbuild copy ${__proj_dir}/examples/processor/tag.py tag.py"
acbuild copy ${__proj_dir}/examples/processor/tag.py tag.py
_info "running: acbuild set-exec ./.venv/bin/python rand.py"
acbuild set-exec ./.venv/bin/python tag.py
_info "running: acbuild write ${__proj_dir}/snap-plugin-processor-tagpy-linux-x86_64.aci"
acbuild write ${__proj_dir}/snap-plugin-processor-tagpy-linux-x86_64.aci
_info "running: acbuild end"
acbuild end

_info "packaging ${__proj_dir}/examples/publisher/file.py"
_info "running: acbuild begin"
acbuild begin
_info "running: acbuild set-name filepy"
acbuild set-name randpy
_info "running: acbuild copy $VIRTUAL_ENV .venv"
acbuild copy $VIRTUAL_ENV .venv
_info "running: acbuild copy ${__proj_dir}/examples/publisher/file.py file.py"
acbuild copy ${__proj_dir}/examples/publisher/file.py file.py
_info "running: acbuild set-exec ./.venv/bin/python file.py"
acbuild set-exec ./.venv/bin/python file.py
_info "running: acbuild write ${__proj_dir}/snap-plugin-publisher-filepy-linux-x86_64.aci"
acbuild write ${__proj_dir}/snap-plugin-publisher-filepy-linux-x86_64.aci
_info "running: acbuild end"
acbuild end

_info "done"
