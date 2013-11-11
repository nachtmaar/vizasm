'''
VizAsm

Created on 09.09.2013

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

from vizasm.analysis.security.filter.util import MethodCallFilterUtil
from vizasm.model import ModelUtil
from vizasm.analysis.security.filter.util.Util import ut_search_string


def md_filter_method_defintion(msg_send, class_name = None, selector_name = None, search_substring = False):        
    '''
    Filter a method definition like e.g. "[AppDelegate application:didFinishLaunchingWithOptions:]"

    Parameters
    ----------
    msg_send: MsgSend
    class_name: string, optional (default is None)
        E.g. "AppDelegate". None means to not filter on the class name.
    selector_name: string, optional (default is None)
        E.g. "application:didFinishLaunchingWithOptions:".
        The name is the pure selector name without any arguments.
        None means to not filter on the selector name.
    search_substring: bool (default is False)
        If True match even if just substring found (`find`).
        Otherwise check for exact equality via `==`.    
    '''
    if MethodCallFilterUtil.mc_is_objectivec_function(msg_send):
        match_class = match_sel = True 
        if class_name is not None:
            match_class = MethodCallFilterUtil.mc_objc_class_with_any_name(msg_send, [class_name], search_substring)
            if not match_class:
                return False
        if selector_name is not None:
            match_sel = MethodCallFilterUtil.mc_has_any_selector(msg_send, [selector_name], search_substring = search_substring)
        return match_class and match_sel
    return False

def md_filter_category(msg_send, selector = None, category_on = None, category_name = None, search_substring = False):
    '''
    Filter a category.
    
    E.g. +[NSURLRequest(AnyHttpsCert) allowsAnyHTTPSCertificateForHost:].
    This is a category on NSURLRequest (`category_on`) with the name AnyHttpsCert (`category_name`).
    
    If you do not want to match on a keyword property, simple leave it out or set it to None!
     
    Parameters
    ----------
    msg_send: MsgSend
    selector: string, optional (default is '' and means to match always)
        the unfilled selector name, without any arguments!
    category_name: string, optional (default is '' and means to match always)
        the name of the category
    category_on: string, optional (default is None and means to match always)
    search_substring: bool (default is False)
        If True match even if just substring found (`find`).
        Otherwise check for exact equality via `==`.
    '''
    if MethodCallFilterUtil.mc_is_objectivec_function(msg_send):
        if category_name is None:
            # match on all category names cause no argument given
            category_name = ''
        if selector is None:
            selector = ''
        category_class = md_get_category_class(msg_send)
        if category_class is not None:
            category_on_match = True
            if category_on is not None:
                category_class_name = str(category_class.category_on_class)
                category_on_match = ut_search_string(category_class_name, category_on, search_substring)
            method_def_match = md_filter_method_defintion(msg_send, category_name, selector, search_substring = True)
            return category_on_match and method_def_match
    return False

def md_is_static_category_method(function):
    ''' Check if the category is static.
    This means that the method that the category overwrites is static.
    
    E.g. "+[NSURLRequest(AnyHttpsCert) allowsAnyHTTPSCertificateForHost:]" is static ("+").
    "-[NSURLRequest(AnyHttpsCert) allowsAnyHTTPSCertificateForHost:]" is not static ("-").
    '''
    if ModelUtil.is_method_implementation(function):
        return function.is_static
    return False

def md_is_category(function):
    ''' Check if `function` is a category '''
    category_class = md_get_category_class(function)
    return ModelUtil.is_category_class(category_class)
    
def md_has_category_class(function):
    ''' Check if the `function` has a `CategoryClass` '''
    return md_get_category_class(function) is not None

def md_get_category_class(function):
    ''' Get the category class.
    
    E.g. "+[NSURLRequest(AnyHttpsCert) allowsAnyHTTPSCertificateForHost:]" has the category class "NSURLRequest(AnyHttpsCert)".
     
    Parameters
    ----------
    function: FunctionInterface
    
    Returns
    -------
    CategoryClass
    None
        if `msg_send` is no category
    '''
    if MethodCallFilterUtil.mc_is_objectivec_function(function):
        receiver = function.msg_receiver
        md_is_category = ModelUtil.is_category_class(receiver)
        if md_is_category:
            return receiver
    return None    
    