.. _Processor-label:

#########
Processor
#########

Below you will find details that cover writing a snap processor plugin in
Python.

.. include:: plugin_naming.rst

Creating a processor
====================

In order to write a processor plugin you will want to start by defining a class
that inherits from :py:class:`snap_plugin.v1.processor.Processor`.

.. code-block:: Python
    :linenos: 
    :emphasize-lines: 3

    import snap_plugin.v1 as snap

    class Rand(snap.Processor):

The next step is to provide an implementation for the following methods:
 * :py:meth:`~snap_plugin.v1.plugin.Plugin.get_config_policy`
 * :py:meth:`~snap_plugin.v1.processor.Processor.process`

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
                        "instance-id",
                        snap.StringRule(default="xyz-abc-qwerty")
                    )
                ]
            ]
        )

Policies are grouped by namespaces for collector plugins however since this is 
a processor plugin it should be set to `None`.  The single  
:py:class:`~IntegerRule` defines a config item "instance-id" with the default 
value "xyz-abc-qwerty".  We could have choosen to make this a required field 
and not provided a `default` which would have had the affect of requiring that 
any task that leveraged this plugin to include a config item providing the 
required value.  

Next we have :py:class:`~snap_plugin.v1.processor.Processor.process`.

:py:meth:`~snap_plugin.v1.processor.Processor.process`
------------------------------------------------------

This method is called by the framework when a task manifest includes the use
of a processor plugin like in the following example task.

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 12-13

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
:py:meth:`~snap_plugin.v1.processor.Processor.process` method.

.. code-block:: Python
    :linenos:

    def process(self, metrics, config):
        for metric in metrics:
            metric.tags["instance-id"] = config["instance-id"]
        return metrics

This example demonstrates using the config to add a tag to the metrics before
returning them.  A less trivial demonstration of adding context (tags) to a 
metric could have involved calling out to another system to obtain additional
context (the owner, datacenter, instance-id, etc..).  Besides adding adding 
additional context to a metric processor plugins are a great place to apply
functions like 'min', 'max', 'mean' etc. 
