Filter Api
----------

Method call
^^^^^^^^^^^

All the functions that you can use to filter method calls are prefixed with mc_ .

.. currentmodule:: vizasm.analysis.security.filter.util.MethodCallFilterUtil

C stuff
```````

.. autosummary::
   
   mc_is_c_function
   mc_get_c_function_name
   mc_c_function_has_any_name

Objective-C stuff
`````````````````

.. autosummary::

	mc_is_objectivec_function
	mc_has_objc_class
	mc_get_objc_class
	mc_has_any_selector
	mc_sel_via_nsselector_from_string
	mc_objc_class_with_any_name

FunctionInterface stuff
```````````````````````

.. autosummary::
	mc_has_format_string
	mc_filter_method_call
	mc_is_function
	mc_contains_imp_got
	mc_function_has_arg_with_name
	mc_function_has_arg_with_exact_name
	mc_function_has_arg_with_subname

Other stuff
```````````

.. autosummary::
	mc_is_exploitable_log_func


Method definition
^^^^^^^^^^^^^^^^^

All the functions that you can use to filter on a method definition are prefixed with md_

.. currentmodule:: vizasm.analysis.security.filter.util.MethodDefFilterUtil

.. autosummary::
	md_filter_method_defintion
	md_filter_category
	md_is_static_category_method
	md_is_category
	md_has_category_class
	md_get_category_class


ModelUtil
^^^^^^^^^
All the functions that you can use to check if something is of a certain class are prefixed with is_

.. currentmodule:: vizasm.model.ModelUtil

.. autosummary::
	is_c_function
	is_sub
	is_objc_function
	is_msg_send
	is_method_implementation
	is_method_implementation_argument

Imp stuff
`````````

.. autosummary::
	is_imp_got
	is_imp_stub

Objective-C stuff
`````````````````

.. autosummary::
	is_selector
	is_objc_class
	is_category_class
	is_nsstring
	is_frameworkclass
	is_format_string

C-Stuff
```````
.. autosummary::
	is_memcpy
	is_c_format_string

Other
`````
.. autosummary::
	is_stackvar
	is_python_string
	is_number
	destination_not_initialized
	