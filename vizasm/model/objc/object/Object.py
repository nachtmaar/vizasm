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

class Object(object):
    ''' 
    Represents an object with a name. 
 
    Parameters
    ----------
    _obj_name: string
        name of the object
    '''
    
    def __init__(self, name):
        self._obj_name = name

    def __str__(self):
        return self.get_obj_name()
    
    def __repr__(self):
        return '%s' % (self.__class__.__name__)
    
    def __hash__(self):
        return hash((self.get_obj_name()))
    
    def __eq__(self, other):
        if isinstance(other, Object):
            return self is other or (
                    (self.get_obj_name()) == 
                    (other.get_obj_name()))
        return False
    
    def __ne__(self, other):
        return not self == other
    
    def get_obj_name(self):
        return self._obj_name

    def set_obj_name(self, value):
        self._obj_name = value
        
    obj_name = property(get_obj_name, set_obj_name, None, "_obj_name(string) -- name of the object")
        
if __name__ == '__main__':
    obj = Object('objectForKey:')
    print obj 
    print obj.__repr__()

