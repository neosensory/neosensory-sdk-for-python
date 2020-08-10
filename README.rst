Neosensory Python SDK
=====================

A Python package for interacting with Neosensory products. This is designed to work with `Bleak <https://github.com/hbldh/bleak>`_, a cross-platform Python Bluetooth Low Energy (BLE) client for Windows, MacOS, and Linux. Please see the Bleak project page for more specifics on supported platforms. **IMPORTANT: At the moment this is tested and only working on Windows.**

Requirements
============
This SDK relies on `Bleak <https://github.com/hbldh/bleak>`_ to take care of the underlying Bluetooth low energy shenanigans. It is included as a dependency and should get automatically installed if using pip or setup.py.

Installation
============

you can clone this repo and run

.. code-block:: bash

	python setup.py develop

from within the root directory.


Usage
=====
You may need to first pair your Neosensory Buzz in advance with your operating system (OS). To do so, find your OS's Bluetooth settings/panel and follow its instructions for pairing a new device. To put Buzz into pairing mode, hold down the (+) and (-) buttons until the LEDs flash blue.

See this repo's `examples <https://github.com/neosensory/neosensory-sdk-for-python/tree/master/examples>`_ directory to get up and running quickly. 

Documentation
=============
You can learn more about the available commands on this `project documentation page <https://neosensory.github.io/neosensory-sdk-for-python/neosensory_python.html#module-neosensory_python>`_. Neosensory platform-agnostic documentation can be obtained from the Neosensory `developer site <https://neosensory.com/developers/>`_.

License
=======

Please note that while this project has an Apache 2.0 license, usage of the Neosensory API to interface with Neosensory products is still subject to the Neosensory developer terms of service located `here <https://neosensory.com/legal/dev-terms-service>`_