'''
VizAsm

Created on 10.04.2013

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

from vizasm.model.objc.arguments.ArgumentsException import ArgumentsException

class ArgumentsOverloadedException(ArgumentsException):
    ''' 
    Exception for the case that there are too many arguments.
    
    Parameters
    __________
    arguments_interface: object<Arguments>
        subclass of Arguments
    new_argument: object, optional
        the new argument added
    '''
    
    def __init__(self, arguments_interface, new_argument = None):
        self._new_argument = new_argument
        ArgumentsException.__init__(self, arguments_interface)
    
    def __str__(self):
        if self._new_argument is not None:
            return '%s has more arguments than it needs!\nNew argument: %s\nArguments: %s' % (self._arguments_interface, self._new_argument, self._arguments_interface.get_arguments())
        return '%s has more arguments than it needs!\nArguments: %s' % (self._arguments_interface, self._arguments_interface.get_arguments())
