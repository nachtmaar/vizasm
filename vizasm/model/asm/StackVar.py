'''
VizAsm

Created on 29.03.2013

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

from vizasm.model.asm.Value import Value

class StackVar(Value):
    ''' 
    Represents a stack variable which can be created from an assembler line e.g. "[ss:rbp-0x30+var_40]"
    
    Parameters
    ----------
    name: string
        the name of the StackVar
    '''
    
    def __init__(self, name):
        Value.__init__(self, name)

    def __hash__(self):
        return Value.__hash__(self)

    def __eq__(self, other):
        return Value.__eq__(self, other)
        
    def __str__(self):
        return self.get_value()
    
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.get_value())
