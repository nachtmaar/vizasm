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

class FunctionInterface(object):
    ''' Interface for a function.
    
    Parameters
    ----------
    _is_static: bool
        check if the function is static 
    '''
    
    def __init__(self, is_static = False):
        self._is_static = is_static

    def get_is_static(self):
        return self._is_static

    def set_is_static(self, value):
        self._is_static = value

    is_static = property(get_is_static, set_is_static, None, "_is_static(bool) -- check if the function is static")
        
    def __iter__(self):
        ''' Use to iterate over the function arguments '''
        raise NotImplementedError
    
    def __len__(self):
        ''' Get the number of arguments the function has '''
        return self.cnt_has_arguments()
    
    def get_arguments(self):
        '''
        Get the arguments.
        
        Returns
        -------
        arguments: list<object>
        '''
        raise NotImplementedError
    
    def get_function_name(self):
        ''' Get the function name '''
        raise NotImplementedError
    
    def is_c_function(self):
        ''' Returns if the function is a c function '''
        from vizasm.model.objc.function.Function import Function
        return isinstance(self, Function)
    
    def is_objc_function(self):
        ''' Returns if the function is an objective c function '''
        from vizasm.model.objc.function.MsgSend import MsgSend
        return isinstance(self, MsgSend)
    
    def cnt_needs_arguments(self):
        ''' Returns the number of arguments the function needs '''
        raise NotImplementedError
    
    def cnt_has_arguments(self):
        ''' Returns the number of arguments the function has '''
        raise NotImplementedError
    
    @staticmethod
    def is_function(function):
        ''' Check if the given `function` is a subclass of `FunctionInterface` '''
        return isinstance(function, FunctionInterface)
    
    
        