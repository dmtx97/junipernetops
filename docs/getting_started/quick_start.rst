Quick Start
===========

.. toctree::
   :maxdepth: 1

Prerequisites
-------------

Python Knowledge
^^^^^^^^^^^^^^^^
You will need a bit of Python programming knowledge to use this library. If you are stuck or encounter a problem, `r/learnpython <https://www.reddit.com/r/learnpython>`_ is a good resource for learning.

Juniper Knowledge
^^^^^^^^^^^^^^^^^^^^
The Juniper instance heavily utilizes the `Juniper PyEz <https://junos-pyez.readthedocs.io/en/2.5.1/>`_ Python Library so it is important to get yourself familiar with some of its features.


Obtaining A Juniper Instance
----------------------------

To create a **Juniper** instance, you need:

1. host name
2. host addresss
3. username
4. password

After obtaining this information, we can instantiate a Juniper instance to directly use its methods. For example:

.. literalinclude:: example1.py
   :language: python

