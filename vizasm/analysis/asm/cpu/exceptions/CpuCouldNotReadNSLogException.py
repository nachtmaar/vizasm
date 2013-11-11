'''
VizAsm

Created on 08.08.2013

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

class CpuCouldNotReadLogFuncException(CpuException):
    ''' 
    Exception for the case than a log function could not be read.
    
    Parameters
    ----------
    cpu: Cpu
    log_func: string
    nslog_string: string
        what NSLog was supposed to log
    '''
    
    def __init__(self, cpu, log_func, nslog_string):
        CpuException.__init__(self, cpu, caused_by = None)
        self.nslog_string = nslog_string
        self.log_func = log_func
        
    def __str__(self):
        return 'Could not read %s! String representation of stuff to log: %s\ncpu: %s' % (self.log_func, self.nslog_string, self._cpu) 