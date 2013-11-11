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

from vizasm.model.objc.object.Object import Object

class Value(Object):
    ''' 
    Represents an objective-c value
 
    Parameters
    ----------
    value: object
        value of the variable (maps to objc_name)
    ''' 

    def __init__(self, value):   
        Object.__init__(self, value)
        
    def __str__(self):
        return '%s' % (self.get_value())
    
    def __repr__(self):
        return '%s(%s, static: %s)' % (self.__class__.__name__, self.get_value(), self.get_is_static())
    
    def __hash__(self):
        return hash((Object.__hash__(self), self.get_value()))
    
    def __eq__(self, other):
        if isinstance(other, Value):
            return self is other or self.get_value() == other.get_value() and Object.__eq__(self, other)
        return False
    
    def __ne__(self, other):
        return not self == other    
    
    def get_value(self):
        return self.get_obj_name()

    def set_value(self, value):
        self.set_obj_name(value)

    value = property(get_value, set_value, None, "value -- value of the variable")
    
