'''
VizAsm

Created on 21.04.2013

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

from vizasm.model.objc.function.FunctionInterface import FunctionInterface
from vizasm.model.objc.function.MsgSend import MsgSend
from vizasm.model.objc.function.MsgSendInterface import MsgSendInterface
from itertools import imap

class Function(FunctionInterface, MsgSendInterface):
    ''' 
    Represents a function that can take arguments.

    Parameters
    ----------
    __function: string
        The name of the function.
    __func_arguments: list<object>, optional
        The arguments of the function.
    '''
    
    def __init__(self, function, func_arguments = None, is_static = True):
        FunctionInterface.__init__(self, is_static)
        self.__function = function
        if func_arguments is None:
            func_arguments = []
        self.__func_arguments = func_arguments

    def get_function(self):
        return self.__function

    def get_func_arguments(self):
        return self.__func_arguments

    def set_function(self, value):
        self.__function = value

    def set_func_arguments(self, value):
        self.__func_arguments = value
    
    def __str__(self):
        return '%s(%s)' % (self.get_function(), self._arguments_formatted_with_comma())
    
    def __repr__(self):
        return '%s(%s, args: %s)' % (self.__class__.__name__, self.get_function(), self.get_func_arguments())

             
    def __eq__(self, other):
        if isinstance(other, Function):
            return self is other or (self.function) == (other.function)
        return False
    
    def __ne__(self, other):
        return not self == other    
    
    def __hash__(self):
        return hash((self.function))
    
    def __iter__(self):         
        ''' Return an iterator over the function arguments '''
        return iter(self.func_arguments)
    
    def _arguments_formatted_with_comma(self):
        ''' Return a string where the arguments are separated with a comma '''
        return ', '.join(imap(lambda x: str(x), self.func_arguments))
    
    function = property(get_function, set_function, None, "__function(string) -- the name of the function")
    func_arguments = property(get_func_arguments, set_func_arguments, None, "__func_arguments(list<string>) -- the name of the function")

#####################################################################################
# FunctionInterface                                                                 #
#####################################################################################    

    def get_arguments(self):
        return self.get_func_arguments()

    def get_function_name(self):
        return self.get_function()

    def is_c_function(self):
        return FunctionInterface.is_c_function(self)

    def is_objc_function(self):
        return False

    def cnt_needs_arguments(self):
        raise NotImplementedError("Currently not supported. The number of arguments for a c function cannot be read from the asm file!")
    
    def cnt_has_arguments(self):
        return len(self.get_arguments())

#####################################################################################
# MsgSendInterface                                                                  #
#####################################################################################    
    def create_msg_send(self, selector, *args, **kwargs):
        ''' Create a `MsgSend` with the specified `selector`.
        
        Parameters
        ----------
        selector: Selector
            the `Selector` with which the `MsgSend` shall be created.
            
        Returns
        -------
        MsgSend
            the created `MsgSend` 
        ''' 
        return MsgSend(self, [selector])
    
if __name__ == '__main__':
    function = 'function'
    args = ['1', '2', '3']
    classfunc = Function(function, args)
    print classfunc
    function = 'function'
    classfunc = Function(function)
    print classfunc
