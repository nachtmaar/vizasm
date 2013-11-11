'''
VizAsm

Created on 29.03.2013

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
from vizasm.model.objc.object.nsobject.NSObjectInterface import \
    NSObjectInterface

class NSString(NSObject, NSObjectInterface):
    ''' 
    Represents a NSString.
    '''
    
    def __init__(self, name, is_static = False):
        NSObject.__init__(self, name, is_static)
        
    def __str__(self):
        return '@"%s"' % (self.get_objc_name())
    
    def __repr__(self):
        return '%s(@"%s", static: %s, retain count: %d)' % (self.__class__.__name__, self.get_objc_name(), self.get_is_static(), self.get_retain_count())
    
    def __hash__(self):
        return NSObject.__hash__(self)

    def __eq__(self, other):
        return NSObject.__eq__(self, other)

    def __len__(self):
        return len(self.get_objc_name())    

#####################################################################################
# NSObjectInterface                                                                 #
#####################################################################################
    def get_nsobject(self):
        return self
    
if __name__ == '__main__':
    nsstring = NSString('Defaults')
    print nsstring
