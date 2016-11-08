## How to build the docs

1. Install dependecies
    - `pip install -r test-requirements.txt`
2. Make the docs
    - `(sphinx-apidoc -f -e -o docs/source snap_plugin snap_plugin/v1/tests && cd docs && make html)`

*Note: The commands above need to be run from the root of the project.*