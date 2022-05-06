# Bridge-Simulations
This is a Python library, based on `anntzer/redeal`, which in turn is based on [Thomas Andrews' Deal](https://bridge.thomasoandrews.com/deal/), which is a tool to generate bridge deals, specifying various constraints. These deals can also be analysed with [Bo Haglund's Double Dummy Solver](https://github.com/dds-bridge/dds), with the Windows' dll found in `src/dds-64.dll`.

# Installation
To install this, clone the repository ```git clone https://github.com/KripaPanchagnula/Bridge-Simulations.git```

# Usage
To use the library, make sure the root directory is added to your `PYTHONPATH` environment variable, or work in a virtual environment which has access to the root directory. The `requirements.txt` file only includes packages for testing, type-checking, code coverage etc and they can be installed with ```pip install -r requirements.txt```.

In order to have access to the Double Dummy Solver, this must be run on Windows. Alternatively, the dll can be generated for the relevant OS and placed in `src/` directory, and it must be loaded in correctly in `src/double-dummy.py`.

To see various cases of how to use this library, look at the sample scripts in `examples/`, which have varying `accept(deal)` functions, and include `BestContract` and `BestLead` simulations.

# Testing
There are currently 44 tests which all pass, and code coverage of 99%. To run the tests, run `pytest` and to check coverage `pytest --cov=src tests`.
