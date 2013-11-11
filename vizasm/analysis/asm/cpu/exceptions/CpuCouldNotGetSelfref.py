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

class CpuCouldNotGetSelfref(CpuException):
    ''' Exception for the case that the value of the self reference for the current method could not be detected 
    
    Parameters
    ----------
    _current_meth_impl: ObjcClass
        the current method that is read
    _selfref_reg: string
        the register in which the self reference is stored
    '''
    
    def __init__(self, cpu, selfref_reg, current_meth_impl):
        self._current_meth_impl = current_meth_impl
        self._selfref_reg = selfref_reg
        CpuException.__init__(self, cpu)
        
    def __str__(self):
        return 'Could not get the self reference (stored in register: %s) for the current method: %s\nCpu: %s' % (self._selfref_reg, self._current_meth_impl, self._cpu)   

