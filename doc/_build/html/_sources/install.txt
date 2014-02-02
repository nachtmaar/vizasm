Installation
============

Get a copy
----------

Git
^^^

.. code-block:: sh

	git clone https://bitbucket.org/nachtmaar/vizasm.git

General steps
--------------

- Install python (check below which version you need)
- Install libraries

	.. code-block:: sh

		 # be sure to use the correct easy_install because easy_install will install the lib for the default python version only!
		 # use e.g. easy_install-2.6 for python 2.6 !
		 easy_install networkx
		 easy_install argparse

- Copy the scripts from vizasm/hopper/scripts/ into the Hopper scripts folder (see below for the default location)

Which Python version do I need?
--------------------------------
- Mac: 2.6
	- Hopper uses Python 2.6, so if you plan to run VizAsm from Hopper you need 2.6!
- others >= 2.6

Hopper Scripts location
-----------------------
- Mac: ~/Library/Application\ Support/Hopper/Scripts/
- Ubuntu: ~/.local/share/data/Hopper/scripts/
- Windows: C:\\Users\\<username>\\AppData\\Local\\Hopper\\scripts


Specific installation
---------------------

Windows
^^^^^^^

- Download Python 2.7 from http://www.python.org/download/releases/2.7/
- Get Hopper from http://hopperapp.com/download.html
- use git (http://msysgit.github.io/) go get a copy of VizAsm
- Use the setuptools to install needed libs:
	- get it from here: http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools
	- use the easy_install-2.7.py from the Scripts folder

	.. code-block:: sh

	   easy_install-2.7.exe networkx
	   easy_install-2.7.exe argparse

- Copy the scripts from vizasm/hopper/scripts/ into C:\\Users\\<username>\\AppData\\Local\\Hopper\\scripts


Mac
^^^

.. code-block:: sh

	easy_install-2.6 networkx
 	easy_install-2.6 argparse

	 # from the vizasm src folder, where VizAsm.py is located
	 cp -r vizasm/hopper/scripts/*.py ~/Library/Application\ Support/Hopper/Scripts/vizasm

