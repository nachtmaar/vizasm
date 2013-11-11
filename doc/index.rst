VizAsm
=================================

:Release: |version|
:Date: |today|

.. toctree::
    :maxdepth: 2

    action
    install
    usage
    builtin_filters
    custom_filters

.. contents:: :local:

Description
===========
VizAsm is a reverse-enineering-tool for Mach-O binaries (Mach and iOS).
It is capable of reading the Objective-C and C method calls and performing a security audit.
VizAsm comes with a few built-in filters that you can use but is also expandable with user written filters (easy to write with the help of the Filter Api).

The results of the security audit is visualized as a graph (viewable in `Gephi <http://gephi.org/>`_)
but can also be viewed as simple text.

VizAsm needs the help of the `Hopper Disassembler <http://hopperapp.com/>`_ to get the disassembly.
You can either run it as script from Hopper or export the .asm file and run the analysis from the command line.

Documentation
=============
If you want to see the whole documentation checkout the project and have a look at doc/_build/html/index.html

About
=====
VizAsm has been created at the University of Marburg 2013 out of a software project in the Distributed Systems Group.

The idee came from my two advisers:

1. Lars Baumgärtner
2. Matthias Leinweber

which supported me during the whole project. 

Features
=========
- Read Objective-C and C method calls
- Automated security audit
- Create method call graph
- Extensible with user supplied filters
	- Filter Api
- Commandline version
- Integration into the `Hopper Disassembler <http://hopperapp.com/>`_
	- Annotate method calls
	- Annotate intance variables
	- Annotate registers and stack


Supported architectures
=======================
- x86
- x86_64
- arm (32 bit)

Requirements
============
- python >= 2.6 (2.6 only for Mac and usage inside Hopper)
- networkx 
- argparse
- `Hopper Disassembler <http://hopperapp.com/>`_
- `Gephi <http://gephi.org/>`_ (optional)

.. autoclass:: vizasm

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


