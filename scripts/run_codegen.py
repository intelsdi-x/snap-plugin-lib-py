"""Runs protoc with the gRPC plugin to generate messages and gRPC stubs."""

from grpc.tools import protoc
import logging
import os
import sys

snap_proto = os.environ.get("SNAP_PROTO")
if snap_proto == None:
    logging.error("Environment variable `SNAP_PROTO` must be set")
    sys.exit(1)

protoc.main(
    (
	'',
	'-I{}/'.format(snap_proto),
	'--python_out=./snap_plugin/v1/',
	'--grpc_python_out=./snap_plugin/v1/',
    '{}/plugin.proto'.format(snap_proto),
    )
)
