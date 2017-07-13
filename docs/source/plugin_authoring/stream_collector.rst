.. _stream-collector-label:

###############
StreamCollector
###############

Below you will find details that cover writing a Snap stream collector plugin in
Python.

.. include:: plugin_naming.rst

Creating a collector
====================

In order to write a collector plugin you will want to start by defining a class
that inherits from :py:class:`snap_plugin.v1.stream_collector.StreamCollector`.

.. code-block:: Python
    :linenos: 
    :emphasize-lines: 3

    import snap_plugin.v1 as snap

    class RandomStream(snap.StreamCollector):

The next step is to provide an implementation for the following methods:
 * :py:meth:`~snap_plugin.v1.plugin.Plugin.get_config_policy` 
 * :py:meth:`~snap_plugin.v1.stream_collector.StreamCollector.stream`
 * :py:meth:`~snap_plugin.v1.stream_collector.StreamCollector.update_catalog`

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
                ("random-stream"),
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
that are exposed under the '/random-stream/' namespace.

Next we have :py:meth:`~snap_plugin.v1.stream_collector.StreamCollector.update_catalog`.

:py:meth:`~snap_plugin.v1.collector.Collector.update_catalog`
-------------------------------------------------------------

This method is called when a plugin is intially loaded.  It communicates to the
framework those metrics the plugin can stream.

.. code-block:: Python
    :linenos:

    def update_catalog(self, config):                
        metrics = []
        for key in ("float64", "int64"):
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
metrics ('/intel/streaning/random/float64', '/intel/streaning/random/int64').
 
Finally we have :py:meth:`~snap_plugin.v1.stream_collector.StreamCollector.stream`.

:py:meth:`~snap_plugin.v1.stream_collector.StreamCollector.stream`
------------------------------------------------------------------

Method runs in separate thread, and puts data on queue implemented in StreamCollector class

.. code-block:: Python
    :linenos:
    
    def stream(self):
        LOG.debug("Metrics streaming started")
        while True:
            time.sleep(1)
            metrics = []
            metric = snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="streaming"),
                    snap.NamespaceElement(value="random"),
                    snap.NamespaceElement(value="int")
                ],
                version=1,
                tags={"mtype": "gauge"},
                description="Random {}".format("int"),
                data=random.randint(1, 100)
            )
            metrics.append(metric)
            metric = snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="streaming"),
                    snap.NamespaceElement(value="random"),
                    snap.NamespaceElement(value="float")
                ],
                version=1,
                tags={"mtype": "gauge"},
                description="Random {}".format("float"),
                data=random.random()
            )
            metrics.append(metric)

            for mt in metrics:
                self.proxy.metrics_queue.put(mt)
