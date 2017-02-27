.. _packaging-label:

#########
Packaging
#########

Below you find details that cover packaging a Python based Snap plugin.
Packaging a python plugin depends on the following tools being installed and 
appropriately configured.

- `acbuld <https://github.com/containers/build>`_ (only builds Linux)
- `virtualenv <https://pypi.python.org/pypi/virtualenv>`_

Using the `acbuild` tool we will create an archive that contains a relocatable
python virtualenv with our plugin and dependencies.  The archive includes a 
manifest that describes how to start the plugin which will execute 
our entry point using the included virtualenv.  

Creating the virtual environment
--------------------------------

I'm using `pyenv <https://github.com/yyuu/pyenv>`_ to manage virtualenv but
you can achieve the same without it by using virtualenv (or venv) directly.  In
the example below we will be packaging the example collector, processor and 
publisher from 
`snap-plugin-lib-py <https://github.com/intelsdi-x/snap-plugin-lib-py>`_.  The
same approach will work for packaging any python based plugin. 

*Note: Assume the commands below are run from the projects root.*  

1. **Create a (relocatable) virtualenv**
  ``pyenv virtualenv --copies 3.5.2 snap-plugins``
2. **Install the deps into the virtualenv**  
   In this example we are packaging the
   example plugin which is contained in a single `py` file so we'll install the 
   plugin lib `snap-plugin-lib-py <https://github.com/intelsdi-x/snap-plugin-lib-py>`_
   directly into our virtualenv with the following command *(Note: the virtual env 
   should be activated)*.
   ``pip install snap-plugin-lib-py``   
3. **Create the aci**
    1. ``acbuild acbuild begin``
    2. ``acbuild set-name randpy``
    3. ``acbuild copy ~/.pyenv/versions/3.5.2/envs/snap-plugins .venv``
    4. ``acbuild copy ./examples/collector/rand.py randy.py``
    5. ``acbuild set-exec ./.venv/bin/python randy.py``
    6. ``acbuild write snap-plugin-collector-randpy-linux-x86_64.aci``
    7. ``acbuild end``

Now you're ready to load your plugin
``snap-plugin-collector-randpy-linux-x86_64.aci``.

On Linux systems you can run scripts/pkg_examples.sh to package up the example 
collector, processor and publisher.

The screen capture below demonstrates packaging the example plugins, starting snap and loading the plugin packages and 
starting the example task.

.. |PackageExample| image:: https://www.dropbox.com/s/ier98lvwjm5rrle/packaging.gif?raw=1    
.. _PackageExample: https://github.com/intelsdi-x/snap-plugin-lib-py

|PackageExample|_