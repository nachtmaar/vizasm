'''
VizAsm

Created on 07.04.2013

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

class MemoryLookupException(CpuException):
    ''' 
    Exception for the case that multiple values could not be looked up from memory.
    
    Parameters
    ----------
    _looked_up_list: list<object>
        list of the already looked up ones 
    '''
    def __init__(self, cpu, looked_up_list):
        self._looked_up_list = looked_up_list
        CpuException.__init__(self, cpu)
        
    def __str__(self):
        raise NotImplementedError 
    
class MemoryCouldNotGetAllRegisterValues(MemoryLookupException):
    ''' 
    Exception for the case that not all register values could be resolved (e.g. are None)
    
    Parameters
    ----------
    _looked_up_list: list<object>
        list of the already looked up ones 
    _register_list: list<object>
        list of the registers that have been looked up
    '''
    def __init__(self, cpu, register_list, looked_up_list):
        self._register_list = register_list
        MemoryLookupException.__init__(self, cpu, looked_up_list)
        
    def __str__(self):
        return 'Could not get all register values. Needed register values: %s\nLooked up register values: %s\nCpu: %s' % (self._register_list, self._looked_up_list, self._cpu) 
    
class MemoryCouldNotGetAllStackValues(MemoryLookupException):
    ''' 
    Exception for the case that not all stack values could be resolved (e.g. are None)
    
    Parameters
    ----------
    _cnt_stack_values: int 
        the number of stack values that should be looked up
    '''
    def __init__(self, cpu, cnt_stack_values, looked_up_list):
        self._cnt_stack_values = cnt_stack_values
        MemoryLookupException.__init__(self, cpu, looked_up_list)
        
    def __str__(self):
        return 'Could not get all stack values. Needed %d stack values\nLooked up stack values: %s\nCpu: %s' % (self._cnt_stack_values, self._looked_up_list, self._cpu) 
