'''
VizAsm

Created on 09.05.2013

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

from vizasm.model.asm.ivar.IvarRefException import IvarRefException

class IvarRefCouldNotBeResolvedException(IvarRefException):
    ''' Exception for the case that the ivar_ref could not be resolved '''
    
    def __init__(self, ivar, ivar_ref_lookup):
        r'''
        Parameters
        ----------
        ivar_ref_lookup : IVarRefLookup
            the `ivar_ref_lookup` where the ivar_ref is looked up
        '''
        IvarRefException.__init__(self, ivar)
        self._ivar_ref_lookup = ivar_ref_lookup
    
    def __str__(self):
        return 'The type of the ivar_ref could not be resolved: %s\nIvarRefLookup: %s' % (self._ivar, self._ivar_ref_lookup)
    
