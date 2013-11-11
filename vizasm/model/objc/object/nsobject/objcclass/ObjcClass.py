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
from vizasm.model.objc.object.nsobject.NSObjectInterface import \
    NSObjectInterface
from vizasm.model.objc.function.MsgSendInterface import MsgSendInterface
from vizasm.hopper.HopperAnnotationInterface import HopperAnnotationInterface

class ObjcClass(NSObject, NSObjectInterface, MsgSendInterface, HopperAnnotationInterface):
    ''' 
    Represents an objective-c class 

    Attributes
    ----------
    nsobject: ObjcClass
        representative of the NSObject superclass 
    nil: ObjcClass
        the nil object
    
    Parameters
    ----------    
    superclass: ObjcClass
        superclass of the object (default NSObject (see nsobject))
    variables: list<Variable>
        variables of the class
    methods: list<Selector>
        methods of the class
    is_frameworkclass: boolean
        indicates if the class is part of a framework, recognized by a pattern like [ds:bind__OBJC_CLASS_$_NSUserDefaults] in the asm file
     '''
    
    # defined at end of file  
    nsobject = nil = not_initialized = None

    def __init__(self, name, superclass = None, is_static = False, is_frameworkclass = False, variables = None, methods = None):
        NSObject.__init__(self, name, is_static)
        if variables is None:
            variables = []
        if methods is None:
            methods = []
        if superclass is None:
            superclass = self.nsobject
            if superclass is None:
                superclass = self

        self.__superclass = superclass
        self.__variables = variables
        self.__methods = methods
        self.__is_frameworkclass = is_frameworkclass

    def __hash__(self):
        return hash((self.get_objc_name(), self.get_superclass().get_objc_name(), self.get_is_static(), self.get_is_frameworkclass(), tuple(self.get_variables()), tuple(self.get_methods())))

    def __eq__(self, other):
        if isinstance(other, ObjcClass):
            return self is other or ((
                    self.get_superclass().get_objc_name(),
                    self.get_is_frameworkclass()
                    ) == (
                    other.get_superclass().get_objc_name(),
                    other.get_is_frameworkclass()
                    ) and (
                    self.get_variables().__eq__(other.get_variables()) & 
                    self.get_methods().__eq__(other.get_methods()) 
                    )) and NSObject.__eq__(self, other)
        return False
  
    def __str__(self):
        if self.is_static or self.is_frameworkclass:
            return self.get_objc_name()
        variables = self.get_variables()
        
        if len(variables) > 0:
            return '%s.%s' % (self.get_objc_name(), variables[0])
        return self.get_objc_name()
    
    def __repr__(self):
        return '''%s(%s, superclass: %s, static: %s, retain count: %d, frameworkclass: %s, \nvariables: %s, \nmethods: %s) ''' % (self.__class__.__name__, self.get_objc_name(), self.get_superclass().get_objc_name(), self.get_is_static(),
                       self.get_retain_count(), self.get_is_frameworkclass(), self.get_variables(), self.get_methods())  
                 
    def get_is_frameworkclass(self):
        return self.__is_frameworkclass

    def set_is_frameworkclass(self, value):
        self.__is_frameworkclass = value

    def get_superclass(self):
        return self.__superclass

    def _set_superclass(self, value):
        self.__superclass = value

    def get_variables(self):
        return self.__variables

    def get_methods(self):
        return self.__methods

    def set_variables(self, value):
        self.__variables = value

    def set_methods(self, value):
        self.__methods = value

    def get_first_variable(self):
        ''' Get the first variable. If not found return None '''
        variables = self.get_variables()
        if variables:
            return variables[0]
        return None
    
    variables = property(get_variables, set_variables, None, "variables(list) -- variables of the class")
    methods = property(get_methods, set_methods, None, "methods(list) -- methods of the class")
    superclass = property(get_superclass, _set_superclass, None, "superclass(ObjcClass) -- superclass of the object (default NSObject)")
    is_frameworkclass = property(get_is_frameworkclass, set_is_frameworkclass, None, "is_frameworkclass(boolean) -- indicates if the class is part of a framework, recognized by a pattern like [ds:bind__OBJC_CLASS_$_NSUserDefaults] in the asm file")
    
#####################################################################################
# MsgSendInterface                                                                  #
#####################################################################################
    def create_msg_send(self, selector, *args, **kwargs):
        from vizasm.model.objc.function.MsgSend import MsgSend
        return MsgSend(self, [selector])


#####################################################################################
# HopperAnnotationInterface                                                         #
#####################################################################################

    def hopper_str(self):
        return '%s(%s)' % (self.__class__.__name__, self.get_objc_name())

ObjcClass.nsobject = ObjcClass('NSObject', superclass = None)
ObjcClass.nil = ObjcClass('nil')
ObjcClass.not_initialized = ObjcClass('&var')

