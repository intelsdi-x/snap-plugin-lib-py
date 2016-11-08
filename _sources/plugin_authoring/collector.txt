.. _collector-label:

#########
Collector
#########

Below you will find details that cover writing a Snap collector plugin in
Python.

.. include:: plugin_naming.rst

Creating a collector
====================

In order to write a collector plugin you will want to start by defining a class
that inherits from :py:class:`snap_plugin.v1.collector.Collector`.

.. code-block:: Python
    :linenos: 
    :emphasize-lines: 3

    import snap_plugin.v1 as snap

    class Rand(snap.Collector):

The next step is to provide an implementation for the following methods:
 * :py:meth:`~snap_plugin.v1.plugin.Plugin.get_config_policy` 
 * :py:meth:`~snap_plugin.v1.collector.Collector.collect` 
 * :py:meth:`~snap_plugin.v1.collector.Collector.update_catalog` 

We'll start with :py:meth:`~snap_plugin.v1.plugin.Plugin.get_config_policy`.

:py:meth:`~snap_plugin.v1.plugin.Plugin.get_config_policy`  
----------------------------------------------------------

This method is called by the framework when a plugin loads.  It communicates
what configuration items are needed, whether they are required or optional and
what default values and constraints (min, max) the values may have.  

.. code-block:: Python
    :linenos: 

    def get_config_policy(self):
        LOG.debug("GetConfigPolicy called")
        return snap.ConfigPolicy(
            [
                ("random"),
                [
                    (
                        "int_max",
                        snap.IntegerRule(default=100, minimum=1, maximum=10000)
                    ),
                    (
                        "int_min",
                        snap.IntegerRule(default=0, minimum=0)
                    )
                ]
            ]
        )

Policies are grouped by namespaces for collector plugins so in this case the two 
`IntegerRule` policies that we have defined will be applied to all metrics 
that are exposed under the '/random/' namespace.  

Next we have :py:meth:`~snap_plugin.v1.collector.Collector.update_catalog`.

:py:meth:`~snap_plugin.v1.collector.Collector.update_catalog`
-------------------------------------------------------------

This method is called when a plugin is intially loaded.  It communicates to the
framework those metrics the plugin collects.

.. code-block:: Python
    :linenos:

    def update_catalog(self, config):                
        metrics = []
        for key in ("float64", "int64", "string"):
            metric = snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="random"),
                    snap.NamespaceElement(value=key)
                ],
                version=1,
                tags={"mtype": "gauge"},                
                Description="Random {}".format(key),
            )
            metrics.append(metric)
        return metrics

In the examples above we are adding to the Snap framework three separate 
metrics ('/random/float64', '/random/int64' and '/random/string').   
 
Finally we have :py:meth:`~snap_plugin.v1.collector.Collector.collect_metrics`.

:py:meth:`~snap_plugin.v1.collector.Collector.collect`
------------------------------------------------------

This method is called by the framework when a metric is collected.

.. code-block:: Python
    :linenos:
    
    def collector_metrics(self, metrics):
        for metric in metrics:
        switch = {
            "float64": random.random(),
            "string": "bah",
            "int64": random.randint(
                metric.config["int_min"],
                metric.config["int_max"]
                )
        }
        typ = metric.namespace[len(metric.namespace)-1].Value
        metric.data = switch[typ]
        metric.timestamp = time.time()
    return metrics

This examples demonstrates using config.  For instance, the 'int_min' and 
'int_max' (lines 7, 8) are config entries that are available because of the 
:py:class:`~snap_plugin.v1.config_policy.ConfigPolicy` that is exposed by this 
plugin.  
