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


Utility for determining if an object is of specific type.

The functions have in common, that they take all one positional argument
and return a boolean value (object => bool).  
'''

#####################################################################################
# Functions and method definitions                                                  #
#####################################################################################

from vizasm.analysis.asm.cpu.objcruntime.ObjectiveCRuntime import \
    NOT_INITIALIZED_CLASS
from vizasm.model.asm.StackVar import StackVar
from vizasm.model.asm.imp.ImpGot import ImpGot
from vizasm.model.asm.imp.ImpStub import ImpStub
from vizasm.model.objc.arguments.CFormatString import CFormatString
from vizasm.model.objc.arguments.FormatString import FormatString
from vizasm.model.objc.arguments.Selector import Selector
from vizasm.model.objc.function.FunctionInterface import FunctionInterface
from vizasm.model.objc.function.MethodImplementation import MethodImplementation
from vizasm.model.objc.function.MethodSelectorArgument import \
    MethodSelectorArgument
from vizasm.model.objc.object.nsobject.NSString import NSString
from vizasm.model.objc.object.nsobject.objcclass.CategoryClass import \
    CategoryClass
from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass
from vizasm.model.objc.function.Sub import Sub


def is_c_function(c_function):
    ''' Check if the given argument is a `Function` ''' 
    if FunctionInterface.is_function(c_function):
        return c_function.is_c_function()
    return False

def is_sub(sub):
    ''' Check if `sub` is a subroutine like e.g. "sub_10013ec80" ''' 
    return isinstance(sub, Sub)

def is_objc_function(objc_function):
    ''' Check if `objc_function` is an objective-c function '''
    return is_msg_send(objc_function)
    
def is_msg_send(msg_send):
    ''' Check if the given argument is a `MsgSend` ''' 
    if FunctionInterface.is_function(msg_send):
        return msg_send.is_objc_function()
    return False

def is_method_implementation(function):
    ''' Check if the `function` is a `MethodImplementation`. '''
    return isinstance(function, MethodImplementation)

def is_method_implementation_argument(arg):
    ''' Check if the given argument is a `MethodSelectorArgument` '''
    return isinstance(arg, MethodSelectorArgument)

#####################################################################################
# Imp stuff                                                                         #
#####################################################################################
def is_imp_got(imp_got):
    ''' Check for `ImpGot` '''
    return isinstance(imp_got, ImpGot)

def is_imp_stub(imp_stub):
    ''' Check for `ImpStub` '''
    return isinstance(imp_stub, ImpStub)

#####################################################################################
# Objective-C stuff                                                                 #
#####################################################################################

def is_selector(selector):
    ''' Check if the given argument is a `Selector` ''' 
    return isinstance(selector, Selector)

def is_objc_class(clazz):
    ''' Check if the given argument is an `ObjcClass` ''' 
    return isinstance(clazz, ObjcClass)

def is_category_class(clazz):
    ''' Check if the given argument is an `CategoryClass` ''' 
    return isinstance(clazz, CategoryClass)

def is_nsstring(string):
    ''' Check if the string is a `NSString` '''
    return isinstance(string, NSString)

def is_frameworkclass(arg):     
    ''' Check if the given argument is a framework class.
    Only works for x86_64! ''' 
    return is_objc_class(arg) and arg.is_frameworkclass    

def is_format_string(string):
    ''' Check if the given `string` is a `FormatString` '''
    return isinstance(string, FormatString)

#####################################################################################
# C only stuff                                                                      #
#####################################################################################

def is_memcpy(arg):
    ''' Check if argument is a memcpy() '''
    from vizasm.analysis.security.filter.util.MethodCallFilterUtil import ut_search_string
    return is_c_function(arg) and ut_search_string(str(arg), 'memcpy', search_substring = True) 

def is_c_format_string(c_format_string):
    ''' Check if the given `string` is a `CFormatString` '''
    return isinstance(c_format_string, CFormatString)


#####################################################################################
# Other                                                                             #
#####################################################################################

def is_stackvar(stackvar):
    ''' Check if the given argument is a `StackVar` '''
    return isinstance(stackvar, StackVar)

def is_python_string(string):
    ''' Check if the given `string` is a python string '''
    return isinstance(string, str)

def is_number(int_val):
    ''' Check if the given argument is a number '''
    return isinstance(int_val, (int, long))

def destination_not_initialized(val):
    ''' Check if the destination of an objc_msgSend is not initialized (has 0 as value).
    Do not check for 0 as int!
    Because an zero destination will be wrapped inside a certain class indicating a not initialized variable/destination '''
    return val == NOT_INITIALIZED_CLASS
