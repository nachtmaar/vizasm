'''
VizAsm

Created on 23.08.2013

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
from vizasm.analysis.asm.cpu.x86_64.AsmRegEx_x86_64 import \
    AsmRegEx_x86_64 as regexp
from vizasm.model.asm.StackVar import StackVar
from vizasm.model.asm.imp.ImpGot import ImpGot
from vizasm.model.asm.imp.ImpStub import ImpStub
from vizasm.model.asm.ivar.IVar import IVar
from vizasm.model.asm.var_assignment.VarAssignment import VarAssignment
from vizasm.model.objc.object.nsobject.Variable import Variable
from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass
from vizasm.util import Util

class ParseUtil_x86_64(ParseUtil):
    ''' ParseUtil for the x86_64 architecture '''

    def parse_objc_class_from_classref(self, asmline):
        ''' Create ObjcClass from classref ([ds:objc_classref_Object1]) '''
        classsref_match = regexp.compiled_vre(regexp.RE_CLASSREF).search(asmline)                
        # is classref e.g. [ds:objc_classref_Object1]
        if classsref_match is not None:
            name = classsref_match.group(regexp.RE_CLASSREF_GR_CLASSREF)
            return ObjcClass(name, is_static = True)       
        return None  
    
    def parse_objc_class_from_framework_class(self, asmline):
        ''' Create ObjcClass from frameworkclass e.g. ([ds:bind__OBJC_CLASS_$_NSUserDefaults]) '''
        frameworkclass_match = regexp.compiled_vre(regexp.RE_FRAMEWORKCLASS).search(asmline)
        # is frameworkclass e.g. [ds:bind__OBJC_CLASS_$_NSUserDefaults]
        if frameworkclass_match is not None:
            name = frameworkclass_match.group(regexp.RE_FRAMEWORKCLASS_GR_FCLASS)
            return ObjcClass(name, is_frameworkclass = True)
        return None 
     
    def parse_ivar(self, asmline):
        '''Create a ObjcClass from e.g. [ds:_OBJC_IVAR_$_AppDelegate.obj3] 
            and set AppDelegate as the class with the attribute obj3 '''
        ivar_match = regexp.compiled_vre(regexp.RE_IVAR).search(asmline)
        if ivar_match is not None:
            ivar_class = ivar_match.group(regexp.RE_IVAR_GR_CLASS)
            ivar_name = ivar_match.group(regexp.RE_IVAR_GR_IVAR)
            var = Variable(ivar_name)
            ivar_class = ObjcClass(ivar_class, variables = [var])
            return IVar(ivar_class)
        return None 

    def parse_var_assignment_without_ivar_ref_from_asmline(self, asmline):
        ''' Create a VarAssignment from asmline like e.g. "[ds:rax+rcx]" 
        
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
        var_assignment_match = regexp.compiled_vre(regexp.RE_VAR_ASSIGNMENT).search(asmline)                
        if var_assignment_match is not None:
            selfref_register = var_assignment_match.group(regexp.RE_VAR_ASSIGNMENT_GR_SELF_REGISTER)
            ivar_register = var_assignment_match.group(regexp.RE_VAR_ASSIGNMENT_GR_IVAR_REG)
            reg1, reg2 = selfref_register, ivar_register
            if self.register_class is not None:
                reg1, reg2 = map(lambda x: self.register_class(x), [reg1, reg2])
            return VarAssignment(reg1, reg2, self.cpu)
        return None       
    
    def parse_var_assignment_with_ivar_ref_from_asmline(self, asmline):
        ''' Create a VarAssignment from asmline like e.g. "[ds:rdx+rsi], rax".
        Try to resolve the ivar_ref of the IVar from the register of the right side of the assignment.
        
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
    
    def parse_stackvar(self, asmline):
        '''Create an StackVar from asmline, match e.g. [ss:rbp-0x30+var_40] '''
        stackvar = regexp.compiled_vre(regexp.RE_STACKVAR).search(asmline)
        if stackvar is not None:
            name = stackvar.group(regexp.RE_STACKVAR_GR_STACKVAR)
            var = StackVar(name)
            return var
        return None   

    def parse_imp_stub(self, asmline):
        imp_stub_match = regexp.compiled_vre(regexp.RE_IMP_STUBS).search(asmline)
        if imp_stub_match is not None:
            imp_stub = imp_stub_match.group(regexp.RE_IMP_STUBS_GR_IMP_STUBS)
            return ImpStub(imp_stub)
        return None

    def parse_imp_got(self, asmline):
        imp_got_match = regexp.compiled_vre(regexp.RE_IMP_GOT).search(asmline)
        if imp_got_match is not None:
            imp_got = imp_got_match.group(regexp.RE_IMP_GOT_GR_IMP_GOT)
            return ImpGot(imp_got)
        return None
    
    def parse_call_instruction(self, asmline):
        call_instr_match = regexp.compiled_vre(regexp.RE_CALL_INSTRUCTION).search(asmline)
        if call_instr_match is not None:
            return call_instr_match.group(regexp.RE_CALL_INSTRUCTION_GR_CALLED)
        return None
    
    def parse_register(self, register):
        '''
        Parse a register.
        
        Parameters
        ----------
        register: string
        
        Returns
        --------
        register: `register_type`
            the register wrapped in `register_type` 
        None
            if regular expression did not classify as register  
        '''
        register_match = regexp.compiled_vre(regexp.RE_REGISTER).search(register)
        if register_match is not None:
            ds_reg = register_match.group(regexp.RE_REGISTER_GR_DS_REG)
            reg = register_match.group(regexp.RE_REGISTER_GR_REG)
            qword_reg = register_match.group(regexp.RE_REGISTER_GR_QWORD_REG)
            return self.register_class(Util.filter_not_none((ds_reg, reg, qword_reg))[0])
        return None

    def parse_stack_access(self, asmline):
        ''' Parse a stack access like e.g. "[ss:rsp+0x8]" or "[ss:rsp]".
        The latter leads to an address of 0x0.
        
        Returns
        -------
        tuple<string, string>
            Return the stack pointer name as well as the stack address as hex string.
        '''
        stack_access_match = regexp.compiled_re_stack(self.cpu.stack_pointer_register().register).search(asmline)
        if stack_access_match is not None:
            addr = stack_access_match.group(regexp.RE_STACK_GR_ADDRESS)
            if addr is None:
                addr = '0x0'
            sp_name = stack_access_match.group(regexp.RE_STACK_GR_REG)
            return sp_name, addr
        return None

#####################################################################################
# Non ParseUtil stuff                                                               #
#####################################################################################
    
    @staticmethod
    def parse_additional_method_argument_stack(asmline):
        ''' Parse an additional argument that lies on the stack. Prefix is "arg_".
        Returns the prefix of the argument (value after "_") as string '''
        additional_method_argument_stack_match = regexp.compiled_vre(regexp.RE_ADD_METHOD_ARG_STACK).search(asmline)
        if additional_method_argument_stack_match is not None:
            return additional_method_argument_stack_match.group(regexp.RE_ADD_METHOD_ARG_STACK_GR_ARG_NR)
        return None
    
if __name__ == '__main__':
    from vizasm.analysis.asm.cpu.x86_64.Register_x86_64 import Register_x86_64 as reg
    from vizasm.analysis.asm.cpu.x86_64.Cpu_x86_64 import Cpu_x86_64
    from vizasm.model.objc.arguments.Selector import Selector
    from vizasm.model.objc.function.MsgSend import MsgSend
    cpu = Cpu_x86_64({})
    pu = ParseUtil_x86_64(cpu, reg)
    
    fclass = pu.parse_objc_class_from_framework_class('[ds:bind__OBJC_CLASS_$_NSUserDefaults]')
    classref = pu.parse_objc_class_from_classref('[ds:objc_classref_Object1]')
    ivar = pu.parse_ivar('[ds:_OBJC_IVAR_$_AppDelegate.obj3]')
    sel = pu.parse_selector('qword [ds:objc_sel_selfMethod] ; @selector(selfMethod)')
    nsstring_asm = pu.parse_string('@"Defaults"')
    format_string_asm = pu.parse_format_string('@"Defaults%s"')
    stackvar = pu.parse_stackvar('[ss:rbp-0x30+var_40]')
    # var_assign = pu.parse_var_assignment(' qword [ds:rax+rcx]')
    imp_stub = pu.parse_imp_stub('call       imp___stubs__objc_msgSend')
    imp_got = pu.parse_imp_got('imp___got__objc_msgSend')
    imp = pu.parse_imp('qword [ds:imp___got__objc_msgSend]')
    ds_reg = pu.parse_register('ds:[rdx]')
    ss_reg = pu.parse_stack_access('qword [ss:rsp+0x8]')
    reg = pu.parse_register('r8')
    qword_reg = pu.parse_register('qword [ds:rdi]')
    stack = regexp.compiled_re_stack(cpu.stack_pointer_register()).search('qword [ss:rsp+0xc]')
    print 'fclass: %s' % (fclass)
    print 'classref: %s' % (classref)
    print 'ivar: %s' % (ivar)   
    print 'sel: %s' % (sel)
    print 'nsstring: %s' % (nsstring_asm)
    print 'format string: %s' % (format_string_asm)
    print 'stackvar: %s' % (stackvar)
    # print 'var_assign: %s' % (var_assign)
    print 'imp_stub: %s' % (imp_stub)
    print 'imp_got: %s' % (imp_got)
    print 'register ds : %s' % (ds_reg)
    print 'register ss : %s' % (str(ss_reg))
    print 'register: %s' % (reg)
    print 'register: %s' % (qword_reg)
    print imp
    print pu.parse_selector('00003b78 8B0D58A61B00                    mov        ecx, dword [ds:objc_msg_currentHandler] ; @selector(currentHandler)')
    print stack.groupdict()
    
    print 'IVar'
    print 'Dictionary Key Test:'
    d = {ivar : 'test'}
    ivar2 = pu.parse_ivar('[ds:_OBJC_IVAR_$_AppDelegate.obj3] ')
    d[ivar2] = 'test2'
    # this should not overwrite ivar2 but add an additional entry in the dict, cause ivar3 is not equal to ivar2
    ivar3 = pu.parse_ivar('[ds:_OBJC_IVAR_$_AppDelegate.obj2] ')
    d[ivar3] = 'test3'
    print d
    
    print 'list equal test: should be true'
    x = [ivar]
    y = [ivar]
    print '[ivar] equals [ivar]: %s' % (x == y)
    print '[ivar] equals [ivar2]: %s' % (x == [ivar2])
    
    print '\nivar without ref: %s' % (ivar)
    ivar.set_ivar_ref(MsgSend(ObjcClass('Object3'), [Selector('alloc'), Selector('init')]))
    print 'ivar with ref: %s' % (ivar)
    
    print 'StackVar'
    print pu.parse_stackvar('dword [ss:rbp-0x60+arg_0]')
    print pu.parse_stackvar('[ss:rbp-0x30+var_41]')
   
    '''
    print 'ObjcClass'
    fclass = ObjcClass.create_from_asm_line('[ds:bind__OBJC_CLASS_$_NSUserDefaults]')
    fclass2 = ObjcClass.create_from_asm_line('[ds:bind__OBJC_CLASS_$_NSUserDefaults]')
    classref = ObjcClass.create_from_asm_line('[ds:objc_classref_Object1]')
    print 'fclass: %s' % (fclass)
    print 'classref: %s' % (classref)
    
    print fclass.__hash__() == fclass2.__hash__()
    
    ivar = IVar.create_from_asm_line('[ds:_OBJC_IVAR_$_AppDelegate.obj3]')
    print 'ivar: %s' % (ivar)
    
    FormatString:
    fs1 = FormatString.create_from_asm_line('@"%@%d"')
    fs2 = FormatString.create_from_asm_line('@"f%%oo"')
    fs3 = FormatString.create_from_asm_line('@"f%%o%d"')
    
    print fs1
    print 'Should not be a format string: %s' % (fs2)
    print fs3
    
    NSString:
    nsstring_asm = NSString.create_from_asm_line('@"Defaults"')
    print nsstring_asm
    
    StackVar:
    var1 = StackVar.create_from_asm_line('[ss:rbp-0x30+var_40]')
    print var1
    var2 = StackVar.create_from_asm_line('[ss:rbp-0x30+var_41]')
    vareq1 = StackVar.create_from_asm_line('[ss:rbp-0x30+var_40]')
    print 'same vars equal: %s' % (var1.__eq__(var1))
    print 'equal vars equal: %s' % (var1.__eq__(vareq1))
    print 'unequal vars equal: %s' % (var1.__eq__(var2))
    
    ImpStub:
    imp_stub = ImpStub.create_from_asm_line('000000010000197b E8A4070000                      call       imp___stubs__objc_msgSend')
    print imp_stub.__repr__()
    print imp_stub
    print 'is msgSend: %s' % (imp_stub.is_msg_send())
    
    ImpGot:
    imp_got = ImpGot.create_from_asm_line('0000000100001cc7 488B0542230000                  mov        rax, qword [ds:imp___got__NSStreamSocketSecurityLevelKey]')
    print imp_got.__repr__()
    print imp_got 
    ''' 
