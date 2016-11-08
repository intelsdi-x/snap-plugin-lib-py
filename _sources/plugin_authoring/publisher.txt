.. _publisher-label:

#########
Publisher
#########

Below you will find details that cover writing a Snap publisher plugin in
Python.

.. include:: plugin_naming.rst

Creating a publisher
====================

In order to write a publisher plugin you will want to start by defining a class
that inherits from :py:class:`snap_plugin.v1.publisher.Publisher`.

.. code-block:: Python
    :linenos: 
    :emphasize-lines: 3

    import snap_plugin.v1 as snap

    class Rand(snap.Publisher):

The next step is to provide an implementation for the following methods:
 * :py:meth:`~snap_plugin.v1.plugin.Plugin.get_config_policy`
 * :py:meth:`~snap_plugin.v1.publisher.Publisher.publish`

We'll start with :py:meth:`~snap_plugin.v1.plugin.Plugin.get_config_policy`
---------------------------------------------------------------------------

This method is called by the framework when a plugin loads.  It communicates
what configuration items are needed, whether they are required or optional and
what default values and constraints (min, max) the values may have.  

.. code-block:: Python
    :linenos: 

    def get_config_policy(self):        
        return snap.ConfigPolicy(
            [
                None,
                [
                    (
                        "file",
                        snap.StringRule(default="/tmp/snap-py.out")
                    )
                ]
            ],
        )

Policies are grouped by namespaces for collector plugins however since this is 
a publisher plugin it should be set to `None`.  The single  
:py:class:`~snap_plugin.v1.string_policy.StringRule` defines a config item 
"file" with the default value "/tmp/snap-py.out" defining what file metrics 
will be published to.  We could have choosen to make this a required field and 
not provided a `default` which would have had the affect of requiring that any 
task that leveraged this plugin to include a config item providing the required 
value.  

Next we have :py:meth:`~snap_plugin.v1.publisher.Publisher.publish`.

:py:meth:`~snap_plugin.v1.publisher.Publisher.publish`
------------------------------------------------------

This method is called by the framework when a task manifest includes the use
of a publisher plugin like in the following example task.

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 14-15

   ---
    version: 1
    schedule: 
        type: "simple"
        interval: "1s"
    workflow:
        collect:
            metrics:
                /random/float64: {}
                /random/int64: {}
                /random/string: {}
            process:
                - plugin_name: "tag-py"
                  publish:
                    - plugin_name: "file-py"


Below is an example implementation of a
:py:meth:`~snap_plugin.v1.publisher.Publisher.publish` method.

.. code-block:: Python
    :linenos:

    def publish(self, metrics, config):
        if len(metrics) > 0:
                with open(config["file"], 'a') as outfile:
                    for metric in metrics:
                        outfile.write(
                            json_format.MessageToJson(
                                metric._pb, including_default_value_fields=True))


This example demonstrates using the config to define the location of the file
we will publish to. 
