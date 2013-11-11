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

class ObjcRuntimeSelectorWrongTypeException(CpuException):
    ''' 
    Exception for the case that the selector has not the right class. Has to be: `Selector`.
    
    Parameters
    ----------
    cpu: Cpu
    wrong_type: object 
    '''
    def __init__(self, cpu, wrong_type):
        self._wrong_type = wrong_type
        CpuException.__init__(self, cpu)    
        
    def __str__(self):
        return 'The type of the selector has to be Selector, but is: %s (type: %s)\nCpu: %s' % (self._wrong_type, type(self._wrong_type), self._cpu)

