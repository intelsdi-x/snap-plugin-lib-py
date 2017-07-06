# <img src="http://snap-telemetry.io/assets/img/snap_url.png" align="middle" height="75">Snap Plugin Library for Python

This is a library for writing plugins in Python for the
[Snap telemetry framework](https://github.com/intelsdi-x/snap).

----

1. [Brief overview of Snap architecture](#brief-overview-of-snap-architecture)
2. [Writing a plugin](#writing-a-plugin)
    * [Before writing a Snap plugin](#before-writing-a-snap-plugin)
3. [Example plugins](#example-plugins)
4. [Plugin diagnostics](#plugin-diagnostics)
    * [Custom config](#custom-config)
    * [Custom flags](#custom-flags)

## Brief overview of Snap architecture

For an overview of Snap checkout: [http://snap-telemetry.io/](http://snap-telemetry.io/)

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

## Writing a plugin

For reference on authoring plugins see [library's documentation](https://intelsdi-x.github.io/snap-plugin-lib-py/).

### Before writing a Snap plugin

* See if one already exists in the
[Plugin Catalog](https://github.com/intelsdi-x/snap/blob/master/docs/PLUGIN_CATALOG.md)
* See if someone mentioned it in the
[plugin wishlist](https://github.com/intelsdi-x/snap/labels/plugin-wishlist)

If you do decide to write a plugin, open a new issue following the plugin
[wishlist guidelines](https://github.com/intelsdi-x/snap/blob/master/docs/PLUGIN_CATALOG.md#wish-list)
 and let us know you are working on one!

## Example plugins

You will find example plugins that cover the basics for writing collector, processor, and publisher plugins in the [examples folder](https://github.com/intelsdi-x/snap-plugin-lib-py/tree/master/examples).

## Plugin diagnostics

Snap collector plugins using lib-py can be run independent of Snap to show their current running diagnostics.

To run diagnostic simply execute your plugin (just make sure all dependencies are met in your environment).

Diagnostic information includes:

* Runtime details
    * Plugin name and version
    * RPC type and version
    * OS, architecture
    * Python version
* Config policy
    * Warning if config items required and not provided
* Collectible metrics and their current values
* How long it took to run each of these diagnostics

### Custom config

While running diagnostic you might (or must, if plugin requires it) specify additional config for plugin.

To do so you can run your plugin with `--config` flag and provide valid JSON argument. For example:
```sh
./myplugin.py --config '{"key": "value", "answer": "42"}'
```

### Custom flags

You can also specify your own CLI flags to change behaviour of your plugin while running diagnostics.

#### Flag format

Flag uses following format: `(name, type, description, (optional) default value)`:

`name`: name of your flag under which it will be accessible to use

**Note**: To access values of flags with names containing hyphens `-` you need to replace them with underscore `_`.

`type`: value of enum `snap_plugin.v1.plugin.FlagType` which indicate if your flag should act as a bool toggle, or store value

`description`: description for your flag visible while using `--help` option

`default value`: default value for your flag, which will be available if user doesn't specify any value

#### Adding flags

Flags must be added in your plugin's constructor, **after** calling superclass constructor.

To add your flag you can use methods `add` and `add_multiple` of object `self._flags`:
```python
import snap_plugin.v1 as snap

class MyPlugin(snap.Collector):
    def __init__(self, *args, **kwargs):
        super(MyPlugin, self).__init__(*args, **kwargs)
        self._flags.add('require-config', snap.plugin.FlagType.toggle, 'require additional config')
        self._flags.add_multiple([('stand-alone', snap.plugin.FlagType.toggle, 'enable stand alone mode'), ('port', FlagType.value, 'port to run on', 8080)])
```

#### Accessing flag values

Flag values can be accessed at `self._args` object:
```python

if self._args.require_config:
    # note changing hyphen to underscore in flag name when accessing it
    pass
```

As always, if you have any questions, please reach out to the Snap team via [Slack](https://intelsdi-x.herokuapp.com/) or by opening an issue in Github.
