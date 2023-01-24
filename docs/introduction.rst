Introduction
============

Overview
--------

Datura is a simple, pure Python library for creating data visualizations.


Installation
------------
.. role:: bash(code)
   :language: bash

:bash:`pip install datura`

Why does the world need another Python plotting library?
--------------------------------------------------------

There are several excellent visualization libraries already available for Python.
(The author can personally recommend `matplotlib`_ , `plotly`_, and `pyqtgraph`_.)
So why create another? Datura is free and open source, easy to install, and works well in both notebook environments and other development environments.
Further, Datura creates figures that are beautiful by default and reproducible.

Each one of these criteria resulted in design choices for Datura that make it substantially different from other libraries.
Insisting that it be easy to install resulted in the choice to have zero requirements (outside of the Python standard library).
Datura does not have any configuration files that users need to maintain or adjust (more on this later).

The desire to have it work in a variety of environments drove the usage of svg files as the file format — these files can be rendered anywhere a notebook is running and basically any environment with a browser.

Although beauty is subjective, the default settings for Datura are intentionally chosen to take advantage of the space and colors available to the human visual system to express common quantitative concepts clearly and with minimal clutter.

The final motivating factor, reproducibility, drove the decision to wrap all figure creation into a single line of code.
While this design can result in commands with somewhat lengthy lists of arguments, it guarantees that running the same command generates the same figure, which is especially important in notebook environments where individual cells can be run and re-run in any order.
This consideration also factored into the decision to exclude any configuration files, which can invisibly change the behavior of other plotting libraries.

.. _matplotlib: https://matplotlib.org/stable/index.html
.. _plotly: https://plotly.com/
.. _pyqtgraph: https://www.pyqtgraph.org/

Contributing
------------
Create an `issue`_

Or contribute directly to the Datura `repo`_

.. _issue: https://github.com/ptweir/datura/issues
.. _repo: https://github.com/ptweir/datura
