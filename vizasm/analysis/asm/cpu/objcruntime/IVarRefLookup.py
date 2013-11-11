'''
VizAsm

Created on 10.04.2013

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

from vizasm.analysis.asm.cpu.Resetable import Resetable
from vizasm.analysis.asm.cpu.x86.ParseUtil_x86 import ParseUtil_x86
from vizasm.model.objc.arguments.Selector import Selector
from vizasm.model.objc.function.MsgSend import MsgSend
from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass
from vizasm.util import Util


class IVarRefLookup(object, Resetable):
    ''' 
    Models the instance variable cache of a class.
    
    A dictionary helper for the `IVar` class to look up the `ivar_ref` from an `ivar_class`.
    
    Cause every time a message is sent to an ivar_ref like Object3, an ivar_class like AppDelegate.obj3 is read,
    
    but this will create a new ivar_class and the ivar_ref has to be looked up in this class.
    
    The ivar_ref will be stored after a VarAssignment is read which links to an ivar_class. At this moment, the ivar_ref
     
    seems to be stored in the return register.

    Parameters
    ----------
    __ivar_ref_dict: dict
        dictionary to look up the ivar_ref from an ivar_class (see IVar) 
    '''

#####################################################################################
# Resetable                                                                         #
#####################################################################################    

    def reset(self):
        self.__ivar_ref_dict = {}
        
#####################################################################################
# Implementation                                                                    #
#####################################################################################

    def __init__(self):
        self.reset()
        
    def __str__(self):
        return '%s' % Util.pretty_format_dict(self.ivar_ref_dict)
    
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, Util.pretty_format_dict(self.ivar_ref_dict, True))
    
    def get_ivar_ref_dict(self):
        return self.__ivar_ref_dict

    def set_ivar_ref_dict(self, value):
        self.__ivar_ref_dict = value

    ivar_ref_dict = property(get_ivar_ref_dict, set_ivar_ref_dict, None, "__ivar_ref_dict(dict) -- dictionary to look up the ivar_ref from an ivar_class (see IVar)")
    
    def set_ivar_ref(self, ivar_class, ivar_ref):
        ''' Link ivar_class to ivar_ref '''
        self.get_ivar_ref_dict()[ivar_class] = ivar_ref
        
    def get_ivar_ref(self, ivar_class):
        ''' Get the ivar_ref for the ivar_class 
        '''
        for key, value in self.get_ivar_ref_dict().items():
            if key == ivar_class:
                return value
        return None
        
if __name__ == '__main__':
    from vizasm.analysis.asm.cpu.x86.Cpu_x86 import Cpu_x86
    from vizasm.analysis.asm.cpu.x86.Register_x86 import Register_x86 as reg
    cpu = Cpu_x86({})
    pu = ParseUtil_x86(cpu, reg)
    il = IVarRefLookup()
    ivar_class = pu.parse_ivar('[ds:_OBJC_IVAR_$_AppDelegate.obj3] ')
    ivar_ref = MsgSend(ObjcClass('Object3'), [Selector('alloc'), Selector('init')])
    il.set_ivar_ref(ivar_class, ivar_ref)
    ivar_class2 = pu.parse_ivar('[ds:_OBJC_IVAR_$_AppDelegate.obj3] ')
    
    print 'an equal key should get the same ivar_ref'
    print il.get_ivar_ref(ivar_class2) 
    
    print 'hashes should be equal: %s' % (ivar_class.__hash__() == ivar_class2.__hash__())
    
    print 'ivar lookup: %s' % (il)
