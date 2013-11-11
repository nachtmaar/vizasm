'''
VizAsm

Created on 26.07.2013

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

from vizasm.vizasm_networkx import NodeAttributes
from vizasm.vizasm_networkx.AttributeNodeInterface import AttributeNodeInterface

class MethodCallItem(object, AttributeNodeInterface):
    ''' 
    Item for `MethodCall`.
    
    Parameters
    ----------
    call: MsgSend or Function
    linenr: int, optional (default is -1)
        line number in the asm file where the call has been made
    address: int, optional (default is -1)
        the address where to find in the asm file
    '''
    
    def __init__(self, call, linenr = None, address = None):
        AttributeNodeInterface.__init__(self)
        self.__call = call
        if linenr is None:
            linenr = -1
        if address is None:
            address = -1
        self.__linenr = linenr
        self.__address = address

    def __str__(self):
        return ('%s %d %s\n' % (hex(self.address), self.linenr, str(self.call)))    
                
    def __repr__(self):
        return self.call.__repr__()
    
    def __eq__(self, other):
        if isinstance(other, MethodCallItem):
            return self is other or ((self.call, self.linenr, self.address)) == ((other.call, other.linenr, other.address))
        return False
    
    def __ne__(self, other):
        return not self == other    
    
    def __hash__(self):
        return hash((self.call, self.linenr, self.address))
    
    def __cmp__(self, other):
        return self.address < other.address
                      
    def get_call(self):
        return self.__call

    def get_linenr(self):
        return self.__linenr

    def set_call(self, value):
        self.__call = value

    def set_linenr(self, value):
        self.__linenr = value

    def get_address(self):
        return self.__address

    def set_address(self, value):
        self.__address = value
                    
    call = property(get_call, set_call, None, "call(MsgSend or Function)")
    linenr = property(get_linenr, set_linenr, None, "linenr(int, optional) -- line number in the asm file where the call has been made")
    address = property(get_address, set_address, None, "address(int, optional) -- the address where to find in the asm file")
    
#####################################################################################
# AttributeNodeInterface                                                            #
#####################################################################################

    def node_size(self):
        return NodeAttributes.NVAL_METHODCALL_SIZE_CALL
    
#####################################################################################
# MethodCallItem                                                                    #
#####################################################################################

METHODCALLITEM_PSEUDO = MethodCallItem('pseudo entry')