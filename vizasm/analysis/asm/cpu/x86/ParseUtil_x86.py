'''
VizAsm

Created on 24.08.2013

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

from vizasm.analysis.asm.cpu.x86.AsmRegEx_x86 import AsmRegEx_x86 as regexp
from vizasm.analysis.asm.cpu.x86_64.ParseUtil_x86_64 import ParseUtil_x86_64
from vizasm.model.asm.imp.ImpGot import ImpGot
from vizasm.model.asm.imp.ImpStub import ImpStub
from vizasm.model.asm.ivar.IVar import IVar
from vizasm.model.asm.var_assignment.VarAssignment import VarAssignment
from vizasm.model.objc.arguments.Selector import Selector
from vizasm.model.objc.function.MsgSend import MsgSend
from vizasm.model.objc.object.nsobject.Variable import Variable
from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass

class ParseUtil_x86(ParseUtil_x86_64):
    ''' The `ParseUtil` for the x86 architecture is nearly the same as for x86_64. '''

    def parse_objc_class_from_classref(self, asmline):
        ''' Create ObjcClass from classref ([ds:cls_NSAssertionHandler]) '''
        classsref_match = regexp.compiled_vre(regexp.RE_CLASSREF).search(asmline)                
        if classsref_match is not None:
            name = classsref_match.group(regexp.RE_CLASSREF_GR_CLASSREF)
            return ObjcClass(name, is_static = True)       
        return None 

    def parse_imp_stub(self, asmline):
        imp_stub_match = regexp.compiled_vre(regexp.RE_IMP_STUB).search(asmline)
        if imp_stub_match is not None:
            imp_stub = imp_stub_match.group(regexp.RE_IMP_STUB_GR_IMP_STUB)
            return ImpStub(imp_stub)
        return None
    
    def parse_imp_got(self, asmline):
        imp_nl_symbol_ptr_match = regexp.compiled_vre(regexp.RE_IMP_NL_SYMBOL_PTR).search(asmline)
        if imp_nl_symbol_ptr_match:
            return ImpGot(imp_nl_symbol_ptr_match.group(regexp.RE_IMP_NL_SYMBOL_PTR_GR_NAME))
        return None
        
    def parse_var_assignment_without_ivar_ref_from_asmline(self, asmline):
        ''' Create a VarAssignment from asmline like e.g. "mov dword [ds:ecx+0x8]".
        
        The difference to x86_64 is that  the `ivar_dest` of the `VarAssignment` is no register and cannot be resolved.
        
        Parameters
        ----------
        asmline: String
            
        Raises
        ------
        VarAssignmentResolveSelfrefRegisterException
                        
        Returns
        -------
        VarAssignment
            the VarAssignment without ivar_ref set (None if no VarAssignment)           
        '''
        var_assignment_match = regexp.compiled_vre(regexp.RE_VAR_ASSIGNMENT).search(asmline)                
        if var_assignment_match is not None:
            selfref_register = var_assignment_match.group(regexp.RE_VAR_ASSIGNMENT_GR_SELF_REGISTER)
            ivar_addr = var_assignment_match.group(regexp.RE_VAR_ASSIGNMENT_GR_IVAR_ADDR)
            reg1 = self.register_class(selfref_register)
            var_assignemnt = VarAssignment(reg1, ivar_addr, self.cpu, resolve_ivar_value = False)
            # set the variable of the `ObjcClass` (use the hex address as string for the instance variable name) 
            # needed to successfully lookup the `Ivar` in `IVarRefLookup` (makes `Ivar` unique for this instance variable) 
            selfref_value = var_assignemnt.selfref_value
            if isinstance(selfref_value, ObjcClass):
                selfref_value.variables = [Variable(str(var_assignemnt.ivar_dest))]
            # do not set `ivar_ref` (but `parse_var_assignment_with_ivar_ref_from_asmline` does it)
            var_assignemnt.set_ivar_value(IVar(var_assignemnt.selfref_value, ivar_ref = None))
            return var_assignemnt
        return None       
    
    def parse_var_assignment_with_ivar_ref_from_asmline(self, asmline):
        ''' Create a VarAssignment from asmline like e.g. "mov dword [ds:ecx+0x8], eax".
        Try to resolve the ivar_ref of the IVar from the register of the right side of the assignment.
        
        The difference to x86_64 is that  the `ivar_dest` of the `VarAssignment` is no register and cannot be resolved.

        Parameters
        ----------
        asmline: String
            the `asmline` should have the form of "[ds:rdx+rsi], rax" where the part after the comma is optional. 
            If left out, the ivar_ref cannot be resolved.
        cpu: Cpu
            the cpu which is needed for resolving the values of the registers
            
        Raises
        ------
        VarAssignmentResolveSelfrefRegisterException
        
        Returns
        -------
        VarAssignment
            the VarAssignment with ivar_ref set (None if no VarAssignment)
        '''
        assignment_match = regexp.compiled_vre(regexp.RE_ASSINGMENT_SPLIT).search(asmline)
        var_assign = None
        if assignment_match is not None:
            val2 = assignment_match.group(regexp.RE_ASSINGMENT_SPLIT_GR_VAL2)
            reg2 = val2
            if self.register_class is not None:
                reg2 = self.register_class(val2)
            var_assign = self.parse_var_assignment_without_ivar_ref_from_asmline(asmline)
            ivar_ref = self.cpu.memory.registers.get_value_for_register(reg2)
            # just an assignment? check if var_assign is None to conclude that pattern really is a var assignment
            if var_assign is not None and ivar_ref is not None:
                ivar_val = var_assign.get_ivar_value()
                if ivar_val is not None:
                    ivar_val.set_ivar_ref(ivar_ref)            
                    return var_assign
        return None
        
if __name__ == '__main__':
    from vizasm.analysis.asm.cpu.x86.Cpu_x86 import Cpu_x86
    from vizasm.analysis.asm.cpu.x86.Register_x86 import Register_x86 as reg
    cpu = Cpu_x86({})
    pu = ParseUtil_x86(cpu, reg)
    imp_stub_x86 = pu.parse_imp('call       imp___symbol_stub__objc_setProperty')
    stackvar = pu.parse_stackvar('00002caf 8B4D14                          mov        ecx, dword [ss:ebp-0x48+arg_4]')
    cls_ref = pu.parse_objc_class_from_classref('[ds:cls_NSAssertionHandler]') 
    cls_ref2 = pu.parse_objc_class_from_classref('dword [ds:eax-0x25e1+cls_Object1]')
    
    cpu.read_line('mov        ecx, dword [ds:eax-0x25e1+cls_Object1]')
    var_assignment_without_ivar_ref = pu.parse_var_assignment_without_ivar_ref_from_asmline('dword [ds:ecx+0x8]')
    cpu.memory.registers.set_value_for_register(reg('eax'), MsgSend(ObjcClass('Object1'), [Selector('alloc'), Selector('init')]))
    var_assignment_with_ivar_ref = pu.parse_var_assignment_with_ivar_ref_from_asmline('mov dword [ds:ecx+0x8], eax')
    print imp_stub_x86
    print cls_ref
    print cls_ref2
    print stackvar
    print var_assignment_without_ivar_ref
    print var_assignment_with_ivar_ref
    print pu.parse_imp('[ds:eax-0x221e+imp___nl_symbol_ptr__NSStreamSocketSecurityLevelKey]')

