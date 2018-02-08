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
.. automodule:: reportng
    :members:

.. autoclass:: ReportWriter
    
    .. automethod:: __init__

Helper
------
.. automodule:: reportng.rnghelpers
:members:

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`