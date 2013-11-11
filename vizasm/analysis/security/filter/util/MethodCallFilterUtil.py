'''
VizAsm

Created on 07.08.2013

@author: Nils Schmidt

Copyright 2013 Nils Schmidt

This file is part of VizAsm.

VizAsm is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

VizAsm is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with VizAsm.  If not, see <http://www.gnu.org/licenses/>.
'''

from itertools import imap

from vizasm.analysis.security.filter.FormatStringFilter import \
    FormatStringFilter
from vizasm.analysis.security.filter.util.Util import ut_search_string
from vizasm.model import ModelUtil
from vizasm.model.ModelUtil import is_stackvar, \
    is_method_implementation_argument, is_memcpy, destination_not_initialized, \
    is_format_string, is_c_function
from vizasm.model.objc.function.FunctionInterface import FunctionInterface
from vizasm.util import Util


#####################################################################################
# C Stuff                                                                           #                                                                                                                                                    #
#####################################################################################
def mc_is_c_function(function):
    ''' Check if the function is a c function '''
    return ModelUtil.is_c_function(function)

def mc_get_c_function_name(c_function):
    ''' Get the function name of the c function 
    
    Parameters
    ----------
    c_function: Function
    '''
    if mc_is_c_function(c_function):
        return c_function.get_function_name()
    return None

def mc_c_function_has_any_name(c_function, names, search_substring = False):
    '''
    Check if the given c function has any of the names specified by `names`.
    This means that the names are equal (character for character).
     
    Parameters
    ----------
    names: list<string>
        possible names the function can have
    search_substring: bool (default is False)
        If True match even if just substring found (`find`).
        Otherwise check for exact equality via `==`.        
    '''
    if mc_is_c_function(c_function):
        c_func_name = mc_get_c_function_name(c_function)
        for name in names:
            if ut_search_string(c_func_name, name, search_substring):
                return True
    return False

#####################################################################################
# Objective-C Stuff                                                                 #                                                                                                                                                    #
#####################################################################################

def mc_is_objectivec_function(function):
    ''' Check if the function is an objective c function '''
    return ModelUtil.is_msg_send(function)

def mc_has_objc_class(function):
    ''' 
    Check if the receiver of a message is an objective c class.
    E.g. "[[NSString alloc] init]" is an objective c function and NSString is the objective c class.
    
    But sending a message to the return result of a c function (e.g. "[c_func() anyThing]")
    means that the objective c function does not an objective c class. 
    
    Parameters
    ----------
    function: FunctionInterface
    ''' 
    if mc_is_objectivec_function(function):
        return ModelUtil.is_objc_class(function.get_msg_receiver())
    return False

def mc_get_objc_class(objc_function):
    '''
    Same as `mc_has_objc_class` but returns the objective c class.
    E.g. "[[NSString alloc] init]" returns objective c class "NSString".
    
    Parameters
    ----------
    objc_function: MsgSend
    
    Returns
    -------
    objc_class: ObjcClass
        the objective c class of the objective c function
    '''
    
    if mc_has_objc_class(objc_function):
        return objc_function.get_msg_receiver() 
    return None

def mc_has_any_selector(function, selector_names, search_substring = False):
    '''
    Check if the `function` has a `Selector` with one of the specified names or will be loaded via NSSelectorFromString(...). 
    Can also be a c function (e.g. [c_func_res() someSelector]).
    
    Parameters
    ----------
    function: FunctionInterface
    selectorname: list<string>
        name of the `Selector` (without arguments filled, e.g: "setProperty:forKey:") 
    search_substring: bool
        If True match even if just substring found (`find`).
        Otherwise check for exact equality via `==`.
    '''
    if mc_is_function(function):
        # check if selector will be loaded via NSSelectorFromString(selectorname)
        if is_c_function(function):
            for sel_name in selector_names:
                if mc_sel_via_nsselector_from_string(function, sel_name):
                    return True
        
        for arg in function:
            # check if selector found
            if ModelUtil.is_selector(arg):
                for selname in selector_names:
                    if ut_search_string(arg.selector_name, selname, search_substring = search_substring):
                        return True
        
            # go deeper into structure
            if mc_is_function(arg):
                if mc_has_any_selector(arg, selector_names, search_substring):
                    return True
    return False

def mc_sel_via_nsselector_from_string(function, sel_name):
    ''' Check if a `Selector` is loaded via the NSSelectorFromString function ''' 
    if ModelUtil.is_c_function(function):
        if function.function == 'NSSelectorFromString':
            if function.cnt_has_arguments() >= 1:
                arg = function.func_arguments[0]
                return ut_search_string(str(arg), sel_name, search_substring = True, ignore_case = True)
    return False

def mc_objc_class_with_any_name(objc_function, names, search_substring = True, modelutil_func = None):
    ''' 
    Check if the name of the objective c class equals any name of `names`.
    For definition of equality see `search_substring` parameter.
    
    Parameters
    ----------
    objc_function: MsgSend
    names: list<string>
        the names to search for
    search_substring: bool (default is True)
        If True match even if just substring found (`find`).
        Otherwise check for exact equality via `==`.
    modelutil_func: function from `ModelUtil`
        use this to check if the argument is a certain class
    '''
    if mc_has_objc_class(objc_function):
        objc_class = mc_get_objc_class(objc_function)
        class_match = True if modelutil_func is None else modelutil_func(objc_class)
        for name in names:
            if ut_search_string(objc_class.get_obj_name(), name, search_substring) and class_match:
                return True
    return False

#####################################################################################
# FunctionInterface stuff                                                           #
#####################################################################################

def mc_has_format_string(function):
    ''' 
    Check if the function has a `FormatString` as any of its arguments.
    
    Parameters
    ----------
    function: FunctionInterface
    '''
    return mc_filter_method_call(function, [ModelUtil.is_format_string])

def mc_filter_method_call(iterable, func_list, steps = None):
    '''
    Run over the iterable structure and check if one of the specified function matches on any argument.
    
    [SomeClass someSelector:@"SomeString" 2ndarg:@"foo" 3rdarg:@"bar"]
    Be careful, this does not apply the function on the class of the MsgSend! Because it does not belong to the iterable part.
    
    steps:     1            2
    
    Parameters
    ----------
    iterable: iterable
    func_list: list<object -> bool>
        list of functions to apply on every argument
    steps: int, optional (default is None)
        Maximum number of steps to go into iterable structure.
        None means take as much steps as available.
        
    Examples
    --------
    >>> func = lambda x: str(x) == '@"foo"'
    >>> c_func = MsgSend(ObjcClass('Bla'), [Selector('foo:', [NSString('foo')])]) 
    >>> msgsend = MsgSend(ObjcClass('SomeClass'), [Selector('someSelector:2dnarg:3rdarg:', [c_func, NSString('SomeString'), NSString('bar')])])
    >>> print mc_filter_method_call(msgsend, func, steps = 3)
    True
    
    [SomeClass someSelector:[Bla foo:@"foo"] 2dnarg:@"SomeString" 3rdarg:@"bar"]
                ^            ^   ^   ^ 
                |            |   |   | 
    steps:      0            1   2   3 
    '''
    one_func_matches = lambda arg: any(imap(lambda f: f(arg), func_list))
    
    def _check(iterable, func, steps = None, cur_steps = 0):
        if one_func_matches(iterable):
            return True 
        if Util.is_iterable_no_string(iterable):
            for arg in iterable:
                # got given number of steps into iterable structure 
                if steps is None or (steps is not None and cur_steps < steps): 
                    if _check(arg, func, steps, cur_steps + 1):
                        return True
                if one_func_matches(arg):
                    return True
        return one_func_matches(iterable)
    
    return _check(iterable, func_list, steps)
    
def mc_is_function(function):
    ''' Check if the `function` is a `Function` at all '''
    return FunctionInterface.is_function(function)

def mc_contains_imp_got(function, imp_got_name, search_substring = False):
    ''' Check if function has the `imp_got_name` as an any argument and is a subclass of `ImpGot`.
    
    Parameters
    ----------
    function: FunctionInterface
    imp_got_name: string
        the name of the `ImpGot`
    search_substring: bool (default is False)
        If True match even if just substring found (`find`).
        Otherwise check for exact equality via `==`.        
    '''
    return mc_function_has_arg_with_name(function, imp_got_name, search_substring = search_substring, modelutil_func = ModelUtil.is_imp_got)

def mc_function_has_arg_with_name(function, name, search_substring = False, modelutil_func = None):            
    ''' Check if the `function` contains an argument with the specified `name`.
    
    Parameters
    ----------
    function: FunctionInterface
    name: string
        the name to look for
    search_substring: bool
        If True match even if just substring found (`find`).
        Otherwise check for exact equality via `==`.
    modelutil_func: function from `ModelUtil`
        use this to check if the function argument is a certain class
    '''
    def __check(func_arg):
        is_class = True
        if modelutil_func is not None:
            # check if `func_arg` is specified class (through `modelutil_func`)
            is_class = modelutil_func(func_arg)
        # check for match
        match = ut_search_string(str(func_arg), name, search_substring)
        if is_class and match:
            return True        
    
    return mc_filter_method_call(function, [__check])

def mc_function_has_arg_with_exact_name(function, exact_name, modelutil_func = None):            
    ''' Check if the `function` contains an argument with the specified `exact_name`.
    
    Parameters
    ----------
    function: FunctionInterface
    exact_name: string
        the name to look for
    modelutil_func: function from `ModelUtil`
        use this to check if the argument is a certain class
    '''
    return mc_function_has_arg_with_name(function, exact_name, search_substring = False, modelutil_func = modelutil_func)

def mc_function_has_arg_with_subname(function, subname, modelutil_func = None):            
    ''' Check if the `function` contains an argument with the specified `subname`.
    
    Parameters
    ----------
    function: FunctionInterface
    subname: string
        the name to look for
    modelutil_func: function from `ModelUtil`
        use this to check if the argument is a certain class
    '''
    return mc_function_has_arg_with_name(function, subname, search_substring = True, modelutil_func = modelutil_func)

#####################################################################################
# Other stuff                                                                       #
#####################################################################################

def mc_is_exploitable_log_func(function):
    if mc_is_function(function):
        # check if is log function at all
        is_log_func = mc_c_function_has_any_name(function, ['NSLog', 'printf'], search_substring = True)
        
        # no log function
        if not is_log_func:
            return False
        
        # check if log function contains uninitialized data
        uninitialized_checks = [is_stackvar, is_method_implementation_argument, is_memcpy, destination_not_initialized]
        unintialized = mc_filter_method_call(function, uninitialized_checks)
        
        # not uninitialized
        if not unintialized:
            return False
        
        # check if the format string of the log function is set
        format_string_set = False
        func_name = mc_get_c_function_name(function)
        # check if log function is known
        if FormatStringFilter.FORMAT_STRING_ARG_IDX.has_key(func_name):
            # get the idx of the format stirng
            format_string_idx = FormatStringFilter.FORMAT_STRING_ARG_IDX[func_name]
            func_args = function.get_arguments()
            if len(func_args) >= format_string_idx + 1:
                format_string_set = is_format_string(func_args[format_string_idx])
        
        # format string is set    
        if format_string_set:
            return False
        
        return True
        
    # no c function at all
    return False    
