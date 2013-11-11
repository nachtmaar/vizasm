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

from vizasm.model.asm.var_assignment.VarAssignmentResolveRegisterException import \
    VarAssignmentResolveRegisterException

class VarAssignmentResolveSelfrefRegisterException(VarAssignmentResolveRegisterException):
    ''' VarAssignmentResolveRegisterException for resolving the selfref '''
    
    def __init__(self, unresolved_register, cpu = None):
        return VarAssignmentResolveRegisterException.__init__(self, unresolved_register, 'selfref', cpu)
  
