Examples
=======================================

First example
-------------

.. literalinclude:: ../examples/first_example.py

.. image:: ../examples/first_example.svg


Displaying error patches
------------------------

The following demonstrates how to display error patches with output from a
typical SQL query. (You can see the query that generated the data using an open
data set available through the `Bigquery`_ console.)

.. _Bigquery: https://console.cloud.google.com/marketplace/product/sportradar-public-data/mlb-pitch-by-pitch
.. literalinclude:: ../examples/error_patch_example.py

..  figure:: ../examples/error_patch_example.svg

    error_patch_example.svg

Displaying data in a Pandas dataFrame
-------------------------------------

.. literalinclude:: ../examples/pandas_example.py

..  figure:: ../examples/pandas_example.svg

    pandas_example.svg

Displaying time series data in a Pandas dataFrame
-------------------------------------------------

.. literalinclude:: ../examples/time_example.py

..  figure:: ../examples/time_example.svg

    time_example.svg

Displaying histograms
---------------------

.. literalinclude:: ../examples/hist_example.py

..  figure:: ../examples/hist_example.svg

    hist_example.svg