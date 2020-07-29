Neosensory Python SDK
=====================

A Python package for interacting with Neosensory products. This is designed to work with `Bleak <https://github.com/hbldh/bleak>`_, a cross-platform Python Bluetooth Low Energy (BLE) client for Windows, MacOS, and Linux.

Requirements
============
You will need to install `Bleak <https://github.com/hbldh/bleak>`_ to work alongside this package. See the Bleak documentation for specific supported platforms.

Installation
============

.. code-block:: bash

	pip install neosensory-python

or

you can clone this repo and run

.. code-block:: bash

	python setup.py develop

from within the root directory.


Usage
=====
You may need to first pair your Neosensory Buzz in advance with your operating system (OS). To do so, find your OS's Bluetooth settings/panel and follow its instructions for pairing a new device. To put Buzz into pairing mode, hold down the (+) and (-) buttons until the LEDs flash blue.

See this repo's `examples <https://github.com/neosensory/neosensory-sdk-for-python/tree/master/examples>`_ directory to get up and running quickly. 

License
=======

Please note that while this project has an Apache 2.0 license, usage of the Neosensory API to interface with Neosensory products is still subject to the Neosensory developer terms of service located `here <https://neosensory.com/legal/dev-terms-service>`_