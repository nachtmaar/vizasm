'''
VizAsm

Created on 19.06.2013

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

from vizasm.analysis.asm.cpu.AsmRegEx import AsmRegEx
from vizasm.analysis.asm.cpu.AssignmentMatchingSystem import \
    AssignmentMatchingSystem
from vizasm.analysis.asm.cpu.ParseUtil import ParseUtil
from vizasm.analysis.asm.cpu.x86_64.AsmRegEx_x86_64 import \
    AsmRegEx_x86_64 as regexp
from vizasm.model.asm.Register import Register
from vizasm.model.asm.StackVar import StackVar
from vizasm.util.Log import log
from vizasm.analysis.asm.cpu.objcruntime.ObjectiveCRuntime import ObjectiveCRuntime
from vizasm.util.Util import hex2int

class ASM_x86_64(AssignmentMatchingSystem):
    ''' AssignmentMatchingSystem for the x86_64 architecture.
    
    If a stack fetch is read, the  `_stack_address` will not be set.
    However the object will be fetched from stack and stored in `lobject`.
    '''
    
    def __init__(self, cpu, parse_util):
        AssignmentMatchingSystem.__init__(self, cpu, parse_util)
        
    def get_stack_push_objects(self):
        ''' If `is_stack_push`, the stored object is a single register -> wrap into list.
        Otherwise return `robject` '''
        if self.get_is_stack_push():
            return [self.robject]
        return None
    
    def read_assignment(self, asmline):
        '''
        Read an assigment and try to split it.
        
        Parameters
        ----------
        asmline : string
            line of assembler
        '''
        AssignmentMatchingSystem.reset(self)
        assignment_match = AsmRegEx.compiled_vre(regexp.RE_ASSINGMENT_SPLIT).search(asmline)
        if assignment_match is not None:
            self.is_assignment = True
            val1 = assignment_match.group(regexp.RE_ASSINGMENT_SPLIT_GR_VAL1)
            val2 = assignment_match.group(regexp.RE_ASSINGMENT_SPLIT_GR_VAL2)            
            pu = self.parse_util
            
            # stack push
            stack_access = pu.parse_stack_access(val1)
            if stack_access is not None:
                _, addr = stack_access
                self.is_stack_push = True
                self.stack_address = addr
                # save stack access in args_since_last_call to determine number of stack arguments needed for next call 
                self.stack_usage_since_last_call.add(stack_access)
            
            self._log_assignment_split(val1, val2)
            
            stackvar1 = pu.parse_stackvar(val1)
            var_assign1 = pu.parse_var_assignment_without_ivar_ref_from_asmline(val1)
            
            # assume classref, frameworkclass, ivar, selector and string cannot exist on the left side
            var_assign2 = pu.parse_var_assignment_without_ivar_ref_from_asmline(val2)
            
            val2_remaining_types = [pu.parse_ivar, pu.parse_objc_class,
                                   pu.parse_selector, pu.parse_string, pu.parse_imp]
            
            # stack fetch
            stackvar2 = pu.parse_stackvar(val2)
            if stackvar2 is not None:
                self.is_stack_fetch = True
                # replace arg_ with method argument for c function definition
                self._try_replace_argument_stack_var_c_method(stackvar2, val2)
                
            lobject = self._get_val1_value(val1, stackvar1, var_assign1)
            self.lobject = lobject
            robject = self._get_val2_value(val2, stackvar2, var_assign2, val2_remaining_types)
            self.robject = robject
            
            # save register in args_since_last_call to determine number of register arguments needed for next call
            self.add_reg_arg_since_last_call(lobject, robject)

    def _try_replace_argument_stack_var_c_method(self, stackvar2, val2):
        ''' Replace `StackVar` named arg_ with method argument for c function definition '''
        if stackvar2 is not None:
            additional_method_argument_stack_nr_str = self.parse_util.parse_additional_method_argument_stack(val2)
            # additional method argument via stack ("arg_")
            if additional_method_argument_stack_nr_str is not None:
                cpu = self.cpu
                method = cpu.method
                if method is not None and method.is_c_function():
                    # all other method arguments went over available argument register
                    # other arguments are arg_0, arg_8, ...
                    additional_method_argument_stack_nr = hex2int(additional_method_argument_stack_nr_str)
                    if additional_method_argument_stack_nr is not None:
                        # e.g. arg_0 -> 1, arg_8 -> 2
                        add_arg_nr = additional_method_argument_stack_nr / cpu.pointer_size() + 1
                        method_arg_nr = len(cpu.arguments_registers()) + add_arg_nr
                        method_arg = ObjectiveCRuntime.create_method_selector_arg(method_arg_nr)
                        # setting method argument for `StackVar`
                        cpu.memory.registers.set_value_for_register_ann_method_ead(stackvar2, method_arg)
    
    def _get_val1_value(self, val1, stackvar1, var_assign1):
        ''' Get the proper value for val1 and return it '''
        val1_value = None
        # val1 is stackvar (qword [ss:rbp-0x70+var_104], .*)
        if stackvar1 is not None:
            val1_value = stackvar1
        elif var_assign1 is not None:
            tmp = var_assign1.get_ivar_dest()  
            if isinstance(tmp, Register):
                val1_value = tmp
            else:
                # do not store value
                val1_value = None
        # check if is register
        else:
            val1_value = self.parse_util.parse_register(val1)
        if val1_value is None:
            log.warn('Error: Seems like a value has not been mapped to a type appeared on the left side: %s', val1_value)
        return val1_value  
    
    def _get_val2_value(self, val2, stackvar2, var_assign2, remaining_types):
        ''' 
        Determine the class which belongs to val2 and return it.
        If the class is register or StackVar try to resolve the value from the registers dictionary
        '''
        res = None
        pu = self.parse_util
        if stackvar2 is not None:
            # resolve stackvar2
            res = self.cpu.memory.registers.resolve_current_register_value(stackvar2)
        elif var_assign2 is not None:
            res = self._var_assignment_action(var_assign2)
        # val2 is not register, has to be a different type
        else:
            res = ParseUtil.get_fst_match(val2, remaining_types)
        # no match found
        if res is None:
            # check for register
            res = pu.parse_register(val2)
            # not register
            if res is None:
                # try to match as hex
                int_val_of_hex = pu.parse_hex(val2)
                if int_val_of_hex is not None:
                    res = int_val_of_hex
                else:
                    # nothing at all matched
                    log.warn('Error: Seems like a value has not been mapped to a type appeared on the right side: %s', val2)
                    # use string representation of val2
                    res = val2
            # is register
            else:
                # resolve register
                res = self.cpu.memory.registers.resolve_current_register_value(res)
                # double resolution needed, register can point to a stack variable pointing anywhere else
                if isinstance(res, StackVar):
                    res = self.cpu.memory.registers.resolve_current_register_value(res)
                
        return res 

    def _var_assignment_action(self, var_assign):
        ''' Defines how to handle the `VarAssignment`
         
        Parameters
        ----------
        var_assign: VarAssignment
        '''
        return var_assign
