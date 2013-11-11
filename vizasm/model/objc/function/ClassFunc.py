'''
VizAsm

Created on 21.04.2013

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

from vizasm.model.objc.function.Function import Function
from vizasm.model.objc.object.nsobject.NSObjectInterface import \
    NSObjectInterface
from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass

class ClassFunc(Function, NSObjectInterface):
    ''' 
    Represents a class function. 
    A `ClassFunc` has additionally a class to which it belongs.

    Parameters
    ----------
    __class_of_func: ObjcClass
        The class to which the function belongs.
    '''
    
    def __init__(self, class_of_func, function, func_arguments, is_static = False):
        Function.__init__(self, function, func_arguments, is_static = is_static)
        self.__class_of_func = class_of_func

    def get_class_of_func(self):
        return self.__class_of_func

    def set_class_of_func(self, value):
        self.__class_of_func = value

    def __str__(self):
        return '%s.%s' % (self.get_class_of_func(), Function.__str__(self))
    
    def __eq__(self, other):
        if isinstance(other, ClassFunc):
            return self is other or (Function.__eq__(self, other) and self.class_of_func == other.class_of_func)
        return False
    
    def __hash__(self):
        return hash((Function.__hash__(self), self.class_of_func))
    
    class_of_func = property(get_class_of_func, set_class_of_func, None, "__class_of_func(ObjcClass) -- the class to which the function belongs.")

    
#####################################################################################
# NSObjectInterface                                                                 #
#####################################################################################
    def get_nsobject(self):
        return self.get_class_of_func()
        
if __name__ == '__main__':
    class_of_func = ObjcClass('AppDelegate')
    function = 'function'
    args = ['1', '2', '3']
    classfunc = ClassFunc(class_of_func, function, args)
    print classfunc
