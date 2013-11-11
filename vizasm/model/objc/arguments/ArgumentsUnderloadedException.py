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

from vizasm.analysis.asm.cpu.exceptions.CpuException import CpuException
from vizasm.model.objc.arguments.ArgumentsException import ArgumentsException
            
class ArgumentsUnderloadedException(ArgumentsException, CpuException):
    '''
    Exception for the case that there are not enough arguments 
    
    Parameters
    __________
    cpu: Cpu
    arguments_interface: object<Arguments>
        subclass of Arguments
    '''
    
    def __init__(self, arguments_interface, cpu):
        ArgumentsException.__init__(self, arguments_interface)
        CpuException.__init__(self, cpu)
    
    def __str__(self):
        return '%s has less arguments than it needs!\nArguments: %s\nCpu: %s' % (self._arguments_interface, self._arguments_interface.get_arguments(), self._cpu)
   
