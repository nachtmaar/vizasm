'''
VizAsm

Created on 31.08.2013

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

from vizasm.analysis.asm.cpu.ParseUtil import ParseUtil
from vizasm.analysis.asm.cpu.arm.AsmRegEx_arm import AsmRegEx_arm as regexp
from vizasm.model.asm.imp.ImpGot import ImpGot
from vizasm.model.asm.imp.ImpStub import ImpStub
from vizasm.model.asm.ivar.IVar import IVar
from vizasm.model.asm.var_assignment.VarAssignment import VarAssignment
from vizasm.model.objc.object.nsobject.Variable import Variable
from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass
from vizasm.util import Util

class ParseUtil_arm(ParseUtil):
    ''' `ParseUtil` for arm arch '''
    
    @staticmethod
    def parse_add(asmline):
        ''' Parse an add statement like e.g. "add r7, sp, #0xc"
        and return tuple(destination, operand1, operand2).
        Operand2 can be empty (None).
        '''
        add_match = regexp.compiled_vre(regexp.RE_ADD).search(asmline)
        if add_match is not None:
            destination = add_match.group(regexp.RE_ADD_GR_DEST)
            operand1, operand2 = add_match.group(regexp.RE_ADD_GR_OPERAND1), add_match.group(regexp.RE_ADD_GR_OPERAND2)
            return destination, operand1, operand2
        return None
        
    @staticmethod
    def parse_assignment_split(asmline):
        ''' Parse an assignment and split to operation, value before and after comma
        See `RE_ASSINGMENT_SPLIT` for details.
        
        Returns
        -------
        tuple<string, string, string>
            tuple containing operation, value1, value2
        '''
        assignment_match = regexp.compiled_vre(regexp.RE_ASSINGMENT_SPLIT).search(asmline)
        op = val1 = val2 = None
        if assignment_match is not None:
            op = assignment_match.group(regexp.RE_ASSINGMENT_SPLIT_GR_OP)
            val1 = assignment_match.group(regexp.RE_ASSINGMENT_SPLIT_GR_VAL1)
            val2 = assignment_match.group(regexp.RE_ASSINGMENT_SPLIT_GR_VAL2)   
        return op, val1, val2
    
    def parse_stack_push_via_stm(self, asmline, stack_pointer_name):
        ''' Parse a stack push via "stm" command like e.g. ""stm.w      sp, {r3, r11}".
        
        Parameters
        ----------
        stack_pointer_name: string
            name of the stack pointer register
            
        Returns
        -------
        list<Register>
            list of pushed registers.
        '''
        reg_list_match = regexp.compiled_re_stack_push_via_stm(stack_pointer_name, asmline)
        if reg_list_match is not None:
            reg_list = reg_list_match.group(regexp.RE_STACK_PUSH_GR_REGISTERS).split(',')
            reg_list = [self.register_class(x.strip()) for x in reg_list]
            return reg_list
        return None
    
    @staticmethod
    def parse_offset_addring_offset_needed(asmline):
        ''' Parse arm offset addressing like e.g. "[sp, #0x8]" and return the values as a tuple<string>
        Without an offset (meaning a second value seperated by ",") this will not match!
        -> "[r5] does not match! 
        '''
        offset_addr_match = regexp.compiled_vre(regexp.RE_OFFSET_ADDRESSING).search(asmline)
        if offset_addr_match is not None:
            offset_addr = offset_addr_match.group(regexp.RE_OFFSET_ADDRESSING_GR_OFFSET)
            # offset is needed! if not given return None
            if offset_addr is not None:
                return offset_addr_match.group(regexp.RE_OFFSET_ADDRESSING_GR_BASE_REGISTER), offset_addr
        return None
    
    @staticmethod
    def parse_offset_addressing(asmline):
        ''' Parse arm offset addressing like e.g. "[sp, #0x8]" and return the values as a tuple<string>
        If no offset given, assume 0x0 is offset (e.g. "[sp, #0x8]") 
        '''
        assgn_split = None
        offset_addr_match = regexp.compiled_vre(regexp.RE_OFFSET_ADDRESSING).search(asmline)
        if offset_addr_match is not None:
            offset_addr = offset_addr_match.group(regexp.RE_OFFSET_ADDRESSING_GR_OFFSET)
            assgn_split = offset_addr_match.group(regexp.RE_OFFSET_ADDRESSING_GR_BASE_REGISTER), offset_addr
            oa_base_reg, oa_offset_addr = assgn_split
            if oa_offset_addr is None:
                oa_offset_addr = '0x0'
                return oa_base_reg, oa_offset_addr
        return None
        
    def parse_stack_pointer_sub(self, asmline):
        '''
        Read a line like e.g. "sub sp, #0x14"
        and return the value that is being subtracted from the stack pointer as int.
        None if did not match. 
        '''
        subtracted_value = regexp.stack_pointer_sub(self.cpu.stack_pointer_register().register, asmline)
        if subtracted_value is not None:
            return int(subtracted_value, 16)
        return None
    
#####################################################################################
# ParseUtil                                                                         #
#####################################################################################
    def parse_objc_class_from_classref(self, asmline):
        classref_match = regexp.compiled_vre(regexp.RE_CLASSREF).search(asmline)
        if classref_match is not None:
            return ObjcClass(classref_match.group(regexp.RE_CLASSREF_GR_CLASSREF))
        return None

    def parse_objc_class_from_framework_class(self, asmline):
        return None
    
    def parse_var_assignment_without_ivar_ref_from_asmline(self, asmline):
        ''' Create a VarAssignment from asmline like e.g. "[r4, r5]" 
        
        Parameters
        ----------
        asmline: String
            
        Raises
        ------
        VarAssignmentResolveSelfrefRegisterException
            if the value cannot be resolved
        VarAssignmentResolveIvarRegisterException
            if the value cannot be resolved and `resolve_ivar_value` is true
        VarAssignmentIvarRegisterWrongTypeException
            if the type of the ivar_reg is not `IVar and `resolve_ivar_value` is true
                        
        Returns
        -------
        VarAssignment
            the VarAssignment without ivar_ref set (None if no VarAssignment)           
        '''
        offset_addressing = self.parse_offset_addring_offset_needed(asmline)
        if offset_addressing is not None:
            reg1, reg2 = offset_addressing
            reg1, reg2 = self.register_class(reg1), self.register_class(reg2)
            # check that this is no stack operation like e.g. "str r1, [sp, #0x4]"
            if reg1 != self.cpu.stack_pointer_register():
                return VarAssignment(reg1, reg2, self.cpu)
        return None       
    
    def parse_var_assignment_with_ivar_ref_from_asmline(self, asmline):
        ''' Create a VarAssignment from asmline like e.g. "r0, [r4, r5]".
        Try to resolve the ivar_ref of the IVar from the register of the left side of the assignment.
        
        Parameters
        ----------
        asmline: String
            the `asmline` should have the form of "r0, [r4, r5]" where the part before the comma is optional. 
            If left out, the ivar_ref cannot be resolved.
        cpu: Cpu
            the cpu which is needed for resolving the values of the registers
        register_class: class
            the class of the register to create. If non given, a string is used for the register representation.
            
        Raises
        ------
        VarAssignmentResolveSelfrefRegisterException
            if the value cannot be resolved
        VarAssignmentResolveIvarRegisterException
            if the value cannot be resolved and `resolve_ivar_value` is true
        VarAssignmentIvarRegisterWrongTypeException
            if the type of the ivar_reg is not `IVar and `resolve_ivar_value` is true
            
        Returns
        -------
        VarAssignment
            the VarAssignment with ivar_ref set (None if no VarAssignment)
        '''
        assignment_match = regexp.compiled_vre(regexp.RE_ASSINGMENT_SPLIT).search(asmline)
        var_assign = None
        if assignment_match is not None:
            op = assignment_match.group(regexp.RE_ASSINGMENT_SPLIT_GR_OP)
            if op.find('str') != -1:
                val1 = assignment_match.group(regexp.RE_ASSINGMENT_SPLIT_GR_VAL1)
                val2 = assignment_match.group(regexp.RE_ASSINGMENT_SPLIT_GR_VAL2)
                reg1 = self.register_class(val1)
                # conclude that is not any stack operation like e.g. "str        r1, [sp, #0x4]"
                if reg1 != self.get_cpu().stack_pointer_register():
                    var_assign = self.parse_var_assignment_without_ivar_ref_from_asmline(val2)
                    ivar_ref = self.cpu.memory.registers.get_value_for_register(reg1)
                    # just an assignment? check if var_assign is None to conclude that pattern really is a var assignment
                    if var_assign is not None and ivar_ref is not None:
                        ivar_val = var_assign.get_ivar_value()
                        if ivar_val is not None:
                            ivar_val.set_ivar_ref(ivar_ref)            
                    return var_assign
        return None
    
    def parse_ivar(self, asmline):
        '''Create a ObjcClass from e.g. "IVAR_0x291c" ''' 
        ivar_match = regexp.compiled_vre(regexp.RE_IVAR).search(asmline)
        if ivar_match is not None:
            ivar_name = ivar_match.group(regexp.RE_IVAR_GR_NAME)
            var = Variable(ivar_name)
            ivar_class = ObjcClass('IVAR', variables = [var])
            return IVar(ivar_class)
        return None 

    def parse_imp_stub(self, asmline):
        ''' Parse an imp stub like e.g. "imp___symbolstub1__objc_msgSend" '''
        imp_symbolstub_match = regexp.compiled_vre(regexp.RE_IMP_SYMBOLSTUB).search(asmline)
        if imp_symbolstub_match is not None:
            return ImpStub(imp_symbolstub_match.group(regexp.RE_IMP_STUBS_GR_IMP_SYMBOLSTUB))
        return None
    
    def parse_imp_got(self, asmline):
            imp_nl_symbol_ptr_match = regexp.compiled_vre(regexp.RE_IMP_NL_SYMBOL_PTR).search(asmline)
            if imp_nl_symbol_ptr_match:
                return ImpGot(imp_nl_symbol_ptr_match.group(regexp.RE_IMP_NL_SYMBOL_PTR_GR_NAME))
            return None
        
    def parse_register(self, register):
        ''' Parse a register and wrap it into the `Register` class.
        Use this to match as last, cause it will match nearly everything! '''
        register_match = regexp.compiled_vre(regexp.RE_REGISTER).search(register)
        if register_match is not None:
            return self.register_class(register_match.group(regexp.RE_REGISTER_GR_NAME))
        return None
    
    def parse_call_instruction(self, asmline):
        ''' Read a call instruction like e.g. "blx imp___symbolstub1__objc_msgSend" '''
        call_instr_match = regexp.compiled_vre(regexp.RE_CALL_INSTRUCTION).search(asmline)
        if call_instr_match is not None:
            return call_instr_match.group(regexp.RE_CALL_INSTRUCTION_GR_CALLED)
        return None

    def parse_stack_access(self, asmline):
        ''' Parse a stack access like e.g. "[sp, #0x8]" or "[r7, #0x8]" or "[sp] or "[sp], #0x4".
        The latter leads to an address of 0x0.
        
        Returns
        -------
        tuple<string, string>
            Return the stack pointer name as well as the stack address as hex string.
        '''
        cpu = self.cpu
        frame_reg, stack_reg = cpu.stack_pointer_register().register, cpu.frame_pointer_register().register
        stack_access_match = regexp.compiled_re_stack(frame_reg, stack_reg).search(asmline)
        if stack_access_match is not None:
            stack_addr = Util.get_fst_not_none((stack_access_match.group(regexp.RE_STACK_GR_ADDRESS), stack_access_match.group(regexp.RE_STACK_GR_OFFSET)))
            stack_pointer_name = stack_access_match.group(regexp.RE_STACK_GR_STACK_POINTER)
            if stack_addr is None:
                stack_addr = '0x0'
            return stack_pointer_name, stack_addr
        return None
    

if __name__ == '__main__':
    from vizasm.analysis.asm.cpu.arm.Register_Arm import Register_arm as reg
    from vizasm.analysis.asm.cpu.arm.Cpu_arm import Cpu_arm
    from vizasm.model.objc.arguments.Selector import Selector
    from vizasm.model.objc.function.MsgSend import MsgSend
 
    cpu = Cpu_arm(superclasses_dict = None)
    pu = ParseUtil_arm(cpu, reg)
    print pu.parse_imp_stub('00002708 01F068EC                        blx        imp___symbolstub1__objc_msgSend')
    print pu.parse_objc_class('000026c0 1068                            ldr        r0, [r2]                              ; @bind__OBJC_CLASS_$_UIScreen')
    print pu.parse_imp('@imp___nl_symbol_ptr__objc_retain')
    print pu.parse_imp('@imp___nl_symbol_ptr___NSConcreteStackBlock')
    print pu.parse_imp('0000a71c 0668                            ldr        r6, [r0]                              ; @imp___nl_symbol_ptr__NSFileProtectionKey')
    print pu.parse_ivar('add        r1, pc ; IVAR_0x291c')
    print pu.parse_assignment_split('add        r7, sp, #0x8')
    print pu.parse_assignment_split('add        r7, sp')
    print pu.parse_assignment_split('str r0, [r4, r5]')
    print 'register: %s' % pu.parse_register(' r2                                ; XREF=0x31ae')
    print pu.parse_stack_push_via_stm('stm.w      sp, {r3, r11}', cpu.stack_pointer_register())
    print pu.parse_stack_push_via_stm('stm.w      sp, {r2, r9}', cpu.stack_pointer_register().register)
    print pu.parse_stack_access('[sp, #0x8]')
    print pu.parse_stack_access('[sp]')
    print pu.parse_offset_addring_offset_needed('[r0, r4]')
    print pu.parse_offset_addressing('[r0]')
       
    # VarAssignment test
    cpu.memory.registers.set_value_for_register(reg('r5'), IVar(ObjcClass('SelfClass'), MsgSend(ObjcClass('Foo'), [Selector('alloc'), Selector('init')])))
    cpu.memory.registers.set_value_for_register(reg('r0'), ObjcClass('Foo'))
    cpu.memory.registers.set_value_for_register(reg('r4'), ObjcClass('SelfClass'))
    print pu.parse_var_assignment_with_ivar_ref_from_asmline('str r0, [r4, r5]')
    print pu.parse_var_assignment_without_ivar_ref_from_asmline('[sp, r5]')
    print pu.parse_var_assignment_with_ivar_ref_from_asmline('str r0, [sp, r5]')
    print 'stack access: %s' % str(pu.parse_stack_access('[sp, #0x4]'))
    print 'stack access: %s' % str(pu.parse_stack_access('[sp], #0x4'))
    print 'stack access: %s' % str(pu.parse_stack_access('[sp]'))
     
    print pu.parse_add('add        r7, sp, #0xc')
    print pu.parse_add('add        r7, sp')
    print pu.parse_add('add        r7, #0xc')
    print pu.parse_stack_pointer_sub('sub        sp, #0x14')
    print pu.parse_call_instruction('00002c50 01F0B2E9                        blx        imp___symbolstub1__NSSearchPathForDirectoriesInDomains ; XREF=0x310e')
    print 'call instr: %s' % pu.parse_call_instruction('bl sub_7183c')
    print pu.parse_stack_access('[r7, #0x8]')
    
    print pu.parse_assignment_split('add r2, pc   ; 0xe5d0c')
    print pu.parse_assignment_split('ldr        r1,=0xfff')
    print pu.parse_assignment_split('0000a56c 0546                            mov        r5, r0')
    
    print pu.parse_register('[ro]')
    print pu.parse_register('ro')
    
    
