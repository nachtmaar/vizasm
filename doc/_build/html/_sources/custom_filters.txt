Custom Filters
==============

.. highlight:: python
   :linenothreshold: 5

.. toctree::
    :maxdepth: 2

    filter_api
    example_filters

The following text shows you how to write your own filter and how to supply it to VizAsm.

Write
-----

Use the template from vizasm.analysis.security.filter.CustomFilter and the filter api to write a custom filter
and have a look at the builtin-filters provided in the example section.

.. warning::

	In general, try to write your filters without checking for a specific class.
	E.g. if you want to filter all NSUserDefaults access, try to match rather on the selector "standardUserDefaults" than on the class itself!
	Or use it as an optinoal test!

	The reason for this is, that on the arm architecture most class names or instance variables cannot be detected properly.

.. warning::

	Be careful, VizAsm expects the class name to be the same as the module name.
	Moreover it has to be in the same package (not subpackage or subdirectory) as the other filters.
	This means, place your filter here: vizasm/analysis/security/filter/ .

Custom filter template
^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: ../vizasm/analysis/security/filter/CustomFilter.py


Load
----
Add the -sf parameter to VizAsm and supply the name(s) of the filter(s) seperated by whitespace
See the usage site for an example.
