'''
VizAsm

Created on 27.03.2013

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

from vizasm.model.objc.function.MsgSendInterface import MsgSendInterface
from vizasm.model.objc.object.Object import Object
from vizasm.model.objc.object.nsobject.NSObjectInterface import \
    NSObjectInterface

class NSObject(Object, NSObjectInterface, MsgSendInterface):
    ''' 
    Superclass of all objective-c stuff. Represents an NSObject in objective-c. 
    '''
    
    def __init__(self, name, is_static = False):
        Object.__init__(self, name)
        self.__retain_count = 0
        self.__is_static = is_static

    def __str__(self):
        return self.get_objc_name()
    
    def __repr__(self):
        return '%s(%s, retain count: %d)' % (self.__class__.__name__, self.get_obj_name(), self.get_retain_count())
    
    def __hash__(self):
        return hash((self.get_objc_name(), self.get_is_static(), Object.__hash__(self)))
    
    def __eq__(self, other):
        if isinstance(other, NSObject):
            return self is other or (
                    (self.get_objc_name(), self.get_is_static()) == 
                    (other.get_objc_name(), other.get_is_static())) and Object.__eq__(self, other)
        return False
                
    def get_is_static(self):
        return self.__is_static

    def set_is_static(self, value):
        self.__is_static = value

    def get_retain_count(self):
        return self.__retain_count
    
    def retain(self):
        ''' Retain object -- increment retain count '''
        self.__retain_count += 1

    def release(self):
        ''' Release object -- decrement retain count '''
        self.__retain_count -= 1    
        
    def get_objc_name(self):
        return self.get_obj_name()

    def set_objc_name(self, value):
        self.set_obj_name(value)
        
#####################################################################################
# NSObjectInterface                                                                 #
#####################################################################################
    def get_nsobject(self):
        return self

#####################################################################################
# MsgSendInterface                                                                  #
#####################################################################################    
    def create_msg_send(self, selector, *args, **kwargs):
        ''' Create a `MsgSend` with the specified `selector`.
        
        Parameters
        ----------
        selector: Selector
            the `Selector` with which the `MsgSend` shall be created.
            
        Returns
        -------
        MsgSend
            the created `MsgSend` 
        ''' 
        from vizasm.model.objc.function.MsgSend import MsgSend
        return MsgSend(self, [selector])
            
    retain_count = property(get_retain_count, None, None, "retain_count(int) -- retain count")
    is_static = property(get_is_static, set_is_static, None, 'is_static(bool) -- tells whether the object is static')
        
if __name__ == '__main__':
    obj = NSObject('objectForKey:', True)
    print obj 
    print obj.__repr__()
    print obj.get_nsobject()

