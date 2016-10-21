# <img src="http://snap-telemetry.io/assets/img/snap_url.png" align="middle" height="75">Snap Plugin Library for Python

This is a library for writing plugins in Python for the
[Snap telemetry framework](https://github.com/intelsdi-x/snap) to get started
authoring a plugin checkout:
# [https://intelsdi-x.github.io/snap-plugin-lib-py/](https://intelsdi-x.github.io/snap-plugin-lib-py/)


## Brief Overview of Snap Architecture

For an overiew of Snap checkout: [http://snap-telemetry.io/](http://snap-telemetry.io/)

Snap is an open and modular telemetry framework designed to simplify the
collection, processing and publishing of data through a single HTTP based API.
Plugins provide the functionality of collection, processing and publishing and
can be loaded/unloaded, upgraded and swapped without requiring a restart of the
Snap daemon.

A Snap plugin is a program that responds to a set of well defined
[gRPC](http://www.grpc.io/) services with parameters and return types specified
as protocol buffer messages (see 
[plugin.proto](https://github.com/intelsdi-x/snap/blob/master/control/plugin/rpc/plugin.proto)).
The Snap daemon handshakes with the plugin over stdout and then communicates over gRPC.

### Before writing a Snap plugin:

* See if one already exists in the
[Plugin Catalog](https://github.com/intelsdi-x/snap/blob/master/docs/PLUGIN_CATALOG.md)
* See if someone mentioned it in the
[plugin wishlist](https://github.com/intelsdi-x/snap/labels/plugin-wishlist)

If you do decide to write a plugin, open a new issue following the plugin
[wishlist guidelines](https://github.com/intelsdi-x/snap/blob/master/docs/PLUGIN_CATALOG.md#wish-list)
 and let us know you are working on one!
