'''
VizAsm

Created on 10.04.2013

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
from vizasm.model.objc.function.MsgSend import MsgSend

class IvarRefWrongTypeException(IvarRefException):
    ''' Exception for the case that the ivar_ref has the wrong type. Should be MsgSend '''
    
    def __init__(self, ivar, ivar_ref):
        r'''
        Parameters
        ----------
        ivar: IVar
        ivar_ref: MsgSend
        '''
        IvarRefException.__init__(self, ivar)
        self._ivar_ref = ivar_ref

    def __str__(self):
        return 'The type of the ivar_ref has to be %s, but is: %s\nIvar: %s' % (MsgSend.__class__.__name__, self._ivar_ref, self._ivar)
    
