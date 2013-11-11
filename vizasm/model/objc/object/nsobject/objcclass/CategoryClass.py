'''
VizAsm

Created on 14.04.2013

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

from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass

class CategoryClass(ObjcClass):
    ''' 
    Represents an objective-c category.
    
    Parameters
    ----------
    category_on_class: ObjcClass
        the class on which the category is added
    '''
    
    def __init__(self, name, category_on_class, superclass = None, is_static = False, is_frameworkclass = False, variables = None, methods = None):
        ObjcClass.__init__(self, name, superclass, is_static, is_frameworkclass, variables, methods)
        self.__category_on_class = category_on_class

    def get_category_on_class(self):
        return self.__category_on_class

    def set_category_on_class(self, value):
        self.__category_on_class = value

    def __hash__(self):
        return hash((ObjcClass.__hash__(self), self.get_category_on_class()))
    
    def __eq__(self, other):
        if isinstance(other, CategoryClass):
            return self is other or ObjcClass.__eq__(self, other) and (self.get_category_on_class()) == (other.get_category_on_class())
        return False
    
    def __str__(self):
        return '%s(%s)' % (self.get_category_on_class(), self.get_objc_name())
    
    def __repr__(self):
        return '''%s(%s, category_on_class: %s\nsuperclass: %s, static: %s, frameworkclass: %s, \nvariables: %s, \nmethods: %s) ''' % (self.__class__.__name__, self.get_objc_name(), self.get_category_on_class(), self.get_superclass().get_objc_name(), self.get_is_static(),
                       self.get_is_frameworkclass(), self.get_variables(), self.get_methods())  
        
    def __static_str(self):
        is_static = self.is_static
        return '+' if is_static else '-'
    
    category_on_class = property(get_category_on_class, set_category_on_class, None, "category_on_class(ObjcClass) -- the class on which the category is added")
        
#####################################################################################
# HopperAnnotationInterface                                                         #
#####################################################################################

    def hopper_str(self):
        return '%s(%s(%s))' % (self.__class__.__name__, self.get_category_on_class(), self.get_objc_name())

if __name__ == '__main__':
    category_on_class = ObjcClass('NSURLRequest')
    cclass = CategoryClass('AnyHttpsCert', category_on_class = category_on_class)
    print cclass    
