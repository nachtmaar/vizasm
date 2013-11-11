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

class VarAssignmentIvarRegisterWrongTypeException(Exception):
    ''' 
    Exception showing that the type of the resolved ivar register is not correct.
    Should be: IVar
        
    Parameters
    ---------
    _resolved_ivar_register: object
        the resolved ivar register
    _register_name: string
        the name of the register
    '''
    
    def __init__(self, resolved_ivar_register, register_name):
        self._resolved_ivar_register = resolved_ivar_register
        self._register_name = register_name
        return Exception.__init__(self)

    def __str__(self):
        return 'The type of the resolved value for the ivar register (%s) should be IVar, but is %s' % (self._register_name, self._resolved_ivar_register)
    
