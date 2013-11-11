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

from vizasm.model.objc.object.nsobject.NSObject import NSObject
class Variable(NSObject):
    ''' 
    Represents an objective-c variable.
    Has in contrast to Value a real value attribute, and not just a mapping to objc_name.
 
    Parameters
    ----------
    value: string
        The value of the variable.
      ''' 

    def __init__(self, name, value = None, is_static = False):   
        NSObject.__init__(self, name, is_static)
        self.__value = value
        
    def __str__(self):
        return self.get_objc_name()
    
    def __repr__(self):
        return '%s(%s, value: %s, static: %s)' % (self.__class__.__name__, self.get_objc_name(), self.get_value(), self.get_is_static())
    
    def __hash__(self):
        return hash((NSObject.__hash__(self), self.get_value()))
    
    def __eq__(self, other):
        ''' Variables are equal if ObjcClass and value are equal '''
        if isinstance(other, Variable):
            return self is other or NSObject.__eq__(self, other) and self.get_value() == other.get_value()
        return False
    
    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value

    value = property(get_value, set_value, None, "value(string) -- value of the variable")
    
