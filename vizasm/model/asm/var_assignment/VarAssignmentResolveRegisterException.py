'''
VizAsm

Created on 31.03.2013

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

class VarAssignmentResolveRegisterException(CpuException):
    ''' 
    General exception for errors while resolving the values of the VarAssignment registers 
    
    Parameters
    ----------
    _unresolved_register: string
        the register that couldn't be resolved
    _register_name: string
        the register of the VarAssingment that could't be resolved
    '''
    
    def __init__(self, unresolved_register, register_name, cpu = None):
        self._unresolved_register = unresolved_register
        self._register_name = register_name
        return CpuException.__init__(self, cpu)

    def __str__(self):
        exception_str_cpu_none = 'Could not resolve %s register %s. This should not happen.\nThe Cpu should always be tracking the values of the registers.' % (self._register_name, self._unresolved_register)
        if self._cpu is None:
            return exception_str_cpu_none
        return exception_str_cpu_none + '\nCpu is: %s' % (self._cpu)
  
