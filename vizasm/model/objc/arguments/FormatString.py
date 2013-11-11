'''
VizAsm

Created on 04.04.2013

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

import sys

from vizasm.model.objc.arguments.Arguments import Arguments
from vizasm.model.objc.arguments.ArgumentsOverloadedException import \
    ArgumentsOverloadedException
from vizasm.model.objc.arguments.ArgumentsUnderloadedException import \
    ArgumentsUnderloadedException
from vizasm.model.objc.object.nsobject.NSString import NSString
from itertools import imap

class FormatStringOverLoadedException(ArgumentsOverloadedException):
    pass  

class FormatStringUnderLoadedException(ArgumentsUnderloadedException):
    pass

class FormatString(Arguments):
    ''' 
    Represents a string with format included like e.g. @"%s", @"foo"

    Parameters
    ----------
    format_string: NSString
        the format string (mapped to objc_name)
    '''
    
    ARGUMENT_DELIMITER = '%'
    
    def __init__(self, format_string, arguments = None):
        if arguments is None:
            arguments = []
        self.__arguments = arguments
        Arguments.__init__(self, format_string, arguments, is_static = False)

    def __str__(self):
        return '%s%s' % (self.get_format_string(), self._format_arguments())
            
    def __repr__(self):
        return '%s(%s, arguments: %s)' % (self.__class__.__name__, self.get_format_string(), self.get_arguments())
    
    def __hash__(self):
        return Arguments.__hash__(self)
    
    def __eq__(self, other):
        return Arguments.__eq__(self, other)
    
    def get_format_string(self):
        return self.get_objc_name()

    def set_format_string(self, value):
        self.set_objc_name(value)
        
    format_string = property(get_format_string, set_format_string, None, "format_string -- the format string (mapped to value from Value)")
    
    def add_argument(self, argument):
        ''' 
        Add an argument to the FormatString 
        
        Raises
        ------
        FormatStringOverLoadedException
            if FormatString has more arguments than it needs
        '''
        try:
            Arguments.add_argument(self, argument)
        except ArgumentsOverloadedException:
            raise FormatStringOverLoadedException(self, argument), None, sys.exc_info()[2]
    
    def cnt_needs_arguments(self):
        ''' Return the number of arguments the FormatString needs '''
        return str(self.get_format_string()).count(FormatString.ARGUMENT_DELIMITER)
    
    def cnt_has_arguments(self):
        ''' Return the number of arguments the FormatString already has '''
        return len(self.get_arguments())
    
    def fill_from_cpu(self, cpu, register_list = None):
        ''' 
        Fill the arguments of the selector from cpu (registers and stack)
        
        Parameters
        ----------
        register_list
            the list of register from which to fill (if None is passed, the default register list is used) 
    
        Raises
        ------
        FormatStringOverLoadedException
            raised if more arguments than needed came from the cpu 
        FormatStringUnderLoadedException
            raised if not enough arguments came from the cpu
        '''
        if register_list is None:
            register_list = cpu.nslog_arg_registers()
        try:
            Arguments.fill_from_cpu(self, cpu, register_list)
        except ArgumentsOverloadedException as e:
            raise FormatStringOverLoadedException(self, e._new_argument), None, sys.exc_info()[2]
        except ArgumentsUnderloadedException as e:
            raise FormatStringUnderLoadedException(self, cpu), None, sys.exc_info()[2]
        
               
    def _fill_remaining_args_from_stack(self, cpu):
        ''' 
        Fill the arguments of the selector from cpu stack
    
        Raises
        ------
        FormatStringOverLoadedException
            raised if more arguments than needed came from the stack of the cpu
        FormatStringUnderLoadedException
            raised if not enough arguments came from the stack of the cpu
        '''
        try:
            Arguments._fill_remaining_args_from_stack(self, cpu)
        except ArgumentsOverloadedException as e:
            raise FormatStringOverLoadedException(self, e._new_argument), None, sys.exc_info()[2]
        except ArgumentsUnderloadedException:
            raise FormatStringUnderLoadedException(self, cpu), None, sys.exc_info()[2]
        
    def _format_arguments(self):
        ''' Format the arguments to a string '''
        prefix_str = '' if len(self.get_arguments()) == 0 else ', '
        return prefix_str + ', '.join(imap(lambda x: str(x), self.arguments))

if __name__ == '__main__':
    format_string = NSString('%s: %s')
    fs = FormatString(format_string, ['class', 'AppDelegate'])
    print fs._format_arguments()
