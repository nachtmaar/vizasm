'''
VizAsm

Created on 06.09.2013

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

from vizasm.model.objc.function.MsgSend import MsgSend

class MethodSelectorArgument(MsgSend):
    ''' 
    A `MethodSelectorArgument` is a `MsgSend` without any selectors and overwritten __str__ method..    
    It's used for the unknown arguments of a method implementations `Selector`
    '''
    
    def __init__(self, msg_send_class):
        MsgSend.__init__(self, msg_send_class, [])
        
    def __str__(self):
        return str(self.msg_receiver)

if __name__ == '__main__':
    from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass
    print MethodSelectorArgument(ObjcClass('arg1'))