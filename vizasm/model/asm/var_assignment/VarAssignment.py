'''
VizAsm

Created on 31.03.2013

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

from copy import deepcopy
from vizasm.model.asm.ivar.IVar import IVar
from vizasm.model.asm.var_assignment.VarAssignmentIvarRegisterWrongTypeException import \
    VarAssignmentIvarRegisterWrongTypeException
from vizasm.model.asm.var_assignment.VarAssignmentResolveIvarRegisterException import \
    VarAssignmentResolveIvarRegisterException
from vizasm.model.asm.var_assignment.VarAssignmentResolveSelfrefRegisterException import \
    VarAssignmentResolveSelfrefRegisterException
    
class VarAssignment(object):
    ''' 
    Represents a variable assignment in assembler code created e.g. from the assembler line "[ds:rdx+rsi]" 
    
    In this line rdx is the selfref_register and rsi the ivar_dest which holds the ivar (e.g. asmline "[ds:_OBJC_IVAR_$_AppDelegate.obj3]")
    
    Parameters
    ----------
    __selfref_register: String
        this register stores the self reference of the current instance from which the method is acting
    __selfref_value: ObjcClass
        the value of the selfref register (None if no cpu has been given at init or cannot be resolved)
    __ivar_dest: classobj<Register> or x86: hex address as string
        the destination to which the ivar will be assigned 
    __ivar_value: IVar
        the value of the ivar register (None if no cpu has been given at init or cannot be resolved)
    '''
    
    def __init__(self, selfref_register, ivar_dest, cpu = None, resolve_selfref_value = True, resolve_ivar_value = True):
        '''
        Init and resolve the `selfref_value` as well as the `ivar_value` (optional).
        
        If no `Cpu` is given, nothing will be resolved at all.
        
        Parameters
        ----------
        resolve_selfref_value: bool
            if true resolve the `__selfref_value` at init
        resolve_ivar_value: bool
            if true resolve the `ivar_value` at init
            
        Raises
        ------
        VarAssignmentResolveSelfrefRegisterException
            if the value cannot be resolved
        VarAssignmentResolveIvarRegisterException
            if the value cannot be resolved and `resolve_ivar_value` is true
        VarAssignmentIvarRegisterWrongTypeException
            if the type of the ivar_reg is not `IVar and `resolve_ivar_value` is true
        '''
        self.__selfref_register = selfref_register
        self.__ivar_dest = ivar_dest
        self.__selfref_value = None
        self.__ivar_value = None
        if cpu is not None:
            if resolve_selfref_value:
                self.__selfref_value = self.__resolve_selfref_reg(cpu)
            if resolve_ivar_value:
                self.__ivar_value = self.__resolve_ivar_dest(cpu)

    def __str__(self):
        return '*(%s + %s) = *(%s + %s)' % (self.get_selfref_register(), self.get_ivar_dest(), self.get_selfref_value(), self.get_ivar_value())
    
    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.get_selfref_register(), self.get_ivar_dest())
    
    def set_selfref_register(self, value):
        self.__selfref_register = value

    def set_ivar_dest(self, value):
        self.__ivar_dest = value

    def set_selfref_value(self, value):
        self.__selfref_value = value

    def set_ivar_value(self, value):
        self.__ivar_value = value

    def get_selfref_register(self):
        return self.__selfref_register

    def get_ivar_dest(self):
        return self.__ivar_dest

    def get_selfref_value(self):
        return self.__selfref_value

    def get_ivar_value(self):
        return self.__ivar_value

    selfref_register = property(get_selfref_register, set_selfref_register, None, "__selfref_register(string) -- this register stores the self reference of the current instance from which the method is acting")
    ivar_dest = property(get_ivar_dest, set_ivar_dest, None, "__ivar_dest(classobj<Register> or x86: hex address as string) -- the destination to which the ivar will be assigned")
    selfref_value = property(get_selfref_value, set_selfref_register, None, "__selfref_value(ObjcClass) -- the value of the selfref register (None if no cpu has been given at init or cannot be resolved)")
    ivar_value = property(get_ivar_value, set_ivar_value, None, "__ivar_value(IVar) -- the value of the ivar register (None if no cpu has been given at init or cannot be resolved)")
    
    def __resolve_selfref_reg(self, cpu):
        ''' Resolve the value of the selfreg register.

        Raises
        ------
        VarAssignmentResolveSelfrefRegisterException
            if the value cannot be resolved
        '''
        selfref_reg = self.get_selfref_register()
        # x86 references always the same self reference -> need to copy to not change the existing one on modification
        selfref_reg_resolved = deepcopy(cpu.memory.registers.get_value_for_register(selfref_reg))
        if selfref_reg_resolved is not None:
            return selfref_reg_resolved
        raise VarAssignmentResolveSelfrefRegisterException(selfref_reg, cpu)
        
    def __resolve_ivar_dest(self, cpu):
        ''' Resolve the value of the ivar destination.
        This should be an IVar. 
            
        Raises
        ------
        VarAssignmentResolveIvarRegisterException
            if the value cannot be resolved
        VarAssignmentIvarRegisterWrongTypeException
            if the type of the ivar_reg is not Ivar
        '''
        ivar_reg = self.get_ivar_dest()
        ivar_reg_resolved = cpu.memory.registers.get_value_for_register(ivar_reg)
        if ivar_reg_resolved is not None:
            if isinstance(ivar_reg_resolved, IVar):
                return ivar_reg_resolved
            else:
                raise VarAssignmentIvarRegisterWrongTypeException(ivar_reg_resolved, ivar_reg)
        raise VarAssignmentResolveIvarRegisterException(ivar_reg, cpu)
    
    selfref_register = property(get_selfref_register, set_selfref_register, None, None)
    ivar_dest = property(get_ivar_dest, set_ivar_dest, None, None)
    selfref_value = property(get_selfref_value, set_selfref_value, None, None)
    ivar_value = property(get_ivar_value, set_ivar_value, None, None)

if __name__ == '__main__':
    from vizasm.analysis.asm.cpu.x86_64.Cpu_x86_64 import Cpu_x86_64
    from vizasm.analysis.asm.cpu.x86_64.Register_x86_64 import Register_x86_64 as reg
    cpu = Cpu_x86_64()
    cpu.read_line(' ; Basic Block Input Regs: rax rdx rsi rdi -  Killed Regs: rax rcx rdx rsp rbp rsi rdi r8')
    cpu.read_line('methImpl_AppDelegate_applicationDidFinishLaunching_:')
    cpu.read_line('0000000100001ca0 488B0D99230000                  mov        rax, rdi')
    cpu.read_line('0000000100001ca0 488B0D99230000                  mov        rcx, qword [ds:_OBJC_IVAR_$_AppDelegate.command]')
    va = VarAssignment(reg('rax'), reg('rcx'), cpu)
    print va
    
    
