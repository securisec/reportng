reportng
========
``reportng`` is a python module to build on the fly reports.
It leverages Bootstrap 4 to automatically create using user defined bootswatch themes.
``reportng`` is capable of handling any python out including but not limited to api output, stdio output, sql queries etc.

Some example use cases of ``reportng`` are

* Create a report for a tool
* Create a report of a test
* Create a report of debugging
* etc...

``reportng`` is stackable. This means that it follows the following convention

* report_header
* report_section
* ...
* report_footer

Social
------

- `Twitter <https://twitter.com/securisec/>`_
- `Github <https://github.com/securisec/>`_

Installation
------------
.. code-block:: bash

    pip install reportng

Documentation
-------------
.. toctree::
   :maxdepth: 2
   :caption: Contents:


.. automodule:: reportng
    :members:


.. autoclass:: ReportWriter
    
    .. automethod:: __init__


.. autoclass: DownloadAssets
    :members:

Helpers
-------

.. automodule:: reportng.rnghelpers
    :members:





Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
