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

class AsmParserInterface:
    ''' 
    Interface for creating an object from a line of assembler code.
    '''
        
    @staticmethod
    def create_from_asm_line(asmline, cpu):
        ''' 
        Parse a line of asm code and try to create an instance of the object from which the method has been called.
        Return None if not possible.
        
        Parameters
        ----------
        asmline: string
        cpu: Cpu
            the cpu/architecture to use
        '''
        raise NotImplementedError
