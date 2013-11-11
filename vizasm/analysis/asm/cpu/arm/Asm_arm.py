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

from vizasm.analysis.asm.cpu.AssignmentMatchingSystem import \
    AssignmentMatchingSystem
from vizasm.analysis.asm.cpu.ParseUtil import ParseUtil
from vizasm.model.asm.Register import Register
from vizasm.util.Log import log

class Asm_arm(AssignmentMatchingSystem):
    '''
    The `AssignmentMatchingSystem` for the arm architecture.
     
     
    A stack fetch as well as a stack pop set the `stack_address`.
    However a fetch from stack will be read and stored in `robject`.
    
    Parameters
    ----------
    __stack_push_via_str: bool (default is False)
        indicates if read line is a stack push via "str" (store)
    __stack_push_via_stm: bool (default is False)
        indicates if read line is a stack push via "stm" (store multiple)
    __stack_fetch_via_prev_sf: bool, (default is True)
        if True, the argument is located on `prev_stack_frame` rather than on `stack`
    '''
    
#####################################################################################
# Resetable                                                                         #
#####################################################################################
    def reset(self):
        ''' Clear the system. '''
        AssignmentMatchingSystem.reset(self)
        self.__init_defaults()

#####################################################################################
# Implementation                                                                    #
#####################################################################################    

    def __init__(self, cpu, parse_util):
        AssignmentMatchingSystem.__init__(self, cpu, parse_util)
        self.__init_defaults()

    def __init_defaults(self):
        self.__stack_push_via_str = self.__stack_push_via_stm = False
        self.stack_address = 0
        self.__stack_fetch_via_prev_sf = True
    
    def clear_usage_since_last_call(self):
        ''' r0 seems to always keep an argument. Add it to the args if they get cleared '''
        if self.cpu.c_func_heuristic:
            # TODO: CHECK WHAT IF FUNCTION HAS NO ARG! DOES R0 GET CLEARED IN ANY WAY?
            AssignmentMatchingSystem.clear_usage_since_last_call(self)
            self.reg_usage_since_last_call.add(self.get_cpu().return_register())
                
    def get_stack_fetch_via_prev_sf(self):
        return self.__stack_fetch_via_prev_sf

    def set_stack_fetch_via_prev_sf(self, value):
        self.__stack_fetch_via_prev_sf = value

    def get_stack_push_via_str(self):
        return self.__stack_push_via_str

    def get_stack_push_via_stm(self):
        return self.__stack_push_via_stm

    def set_stack_push_via_str(self, value):
        self.__stack_push_via_str = value

    def set_stack_push_via_stm(self, value):
        self.__stack_push_via_stm = value

    def get_is_stack_push(self):
        return self.stack_push_via_stm or self.stack_push_via_str
        
    stack_push_via_str = property(get_stack_push_via_str, set_stack_push_via_str, None, '__stack_push_via_str(bool (default is False)) -- indicates if read line is a stack push via "str" (store)')
    stack_push_via_stm = property(get_stack_push_via_stm, set_stack_push_via_stm, None, '__stack_push_via_stm(bool (default is False)) -- indicates if read line is a stack push via "stm" (store multiple)')
    # already in base class, but needed to overwrite get_is_stack_push
    is_stack_push = property(get_is_stack_push, AssignmentMatchingSystem.set_is_stack_push, None, '_is_stack_push: bool (default is False) -- indicates if the assignment is a stack push operation. x86_64 example: "mov dword [ss:rsp], 0x7".')
    stack_fetch_via_prev_sf = property(get_stack_fetch_via_prev_sf, set_stack_fetch_via_prev_sf, None, "__stack_fetch_via_prev_sf(bool, (default is True)) -- if True, the argument is located on `prev_stack_frame` rather than on `stack`")
        
    def get_current_stackframe_for_fetch(self):
        ''' Depending on `stack_fetch_via_prev_sf` get the appropriate `StackFrame`
        which you can use to get an argument from.
        Do not use this method to get the `StackFrame` and read a push '''
        if not self.stack_fetch_via_prev_sf:
            return self.cpu.memory.stack
        return self.cpu.prev_stack_frame
            
    def read_assignment(self, asmline):
        '''
        Read an assignment and try to split it.
        
        Parameters
        ----------
        asmline : string
            line of assembler
        '''
        self.reset()
        sp_sub_val = self.parse_util.parse_stack_pointer_sub(asmline)
        # do not read e.g. "sub sp, #0x14"
        if sp_sub_val is None:
            op, val1, val2 = self.parse_util.parse_assignment_split(asmline)
            
            if None not in (op, val1, val2):
                
                # switch sides if "str" command
                # "str r0, [r4, r5]" -> "str [r4, r5], r0"
                # "str r0, [r4, r5]" means r4.r5 = r0
                if op.find('str') != -1:
                    val1, val2 = val2, val1
                
                self._log_assignment_split(val1, val2)

                # stack push and fetch                
                self._process_stack_push_via_stm(asmline)
                self._process_stack_push_via_str(val1)
                self._process_stack_fetch(val2)
                
                var_assign1 = self.parse_util.parse_var_assignment_without_ivar_ref_from_asmline(val1)
                
                pu = self.parse_util
                val2_remaining_types = [pu.parse_ivar, pu.parse_objc_class,
                                       pu.parse_selector, pu.parse_string,
                                       pu.parse_imp, pu.parse_var_assignment_without_ivar_ref_from_asmline]
                
                lobject = self._get_val1_value(val1, var_assign1)
                self.lobject = lobject
                robject = None
                if not self.is_stack_fetch:
                    robject = self._get_val2_value(val2, val2_remaining_types)
                else:
                    robject = self.get_current_stackframe_for_fetch()[self.stack_address]
                    log.debug('fetched %s from stack at address: %s', robject, hex(self.stack_address))
                self.robject = robject
                
                # save register in args_since_last_call to determine number of register arguments needed for next call
                if self.cpu.c_func_heuristic:
                    self.add_reg_arg_since_last_call(lobject, robject)    
                
                # set pushed objects
                if self.stack_push_via_str:
                    # pushed object is right object
                    # consider e.g. "str        r5, [sp]", val2 = r5 and val1 = sp (due to reordering) 
                    self.stack_push_objects = [self.robject]
        
    def _process_stack_fetch(self, val2):
        ''' Process a steck fetch via "ldr" command.
        
        Check if stack fetch must be done via the previous frame pointer.
        "00065180 F0B5                            push       {r4, r5, r6, r7, lr}
         00065182 03AF                            add        r7, sp, #0xc"
        -> sets r7 to the stored value of r7 (previous frame pointer) 
        '''
        stack_access_tup = self.parse_util.parse_stack_access(val2)
        if stack_access_tup is not None:
            sp_name, stack_access_addr2 = stack_access_tup
            if stack_access_addr2 is not None:
                # stack fetch via e.g. "ldr        r0, [r7, #0xc]"
                self.is_stack_fetch = True
                # first convert to int
                self.stack_address = stack_access_addr2
                if sp_name == self.cpu.stack_pointer_register().register:
                    self.stack_fetch_via_prev_sf = False        
                    
    def _process_stack_push_via_str(self, val1):
        ''' Process a stack push via "str" command '''
        stack_access_tup = self.parse_util.parse_stack_access(val1)
        if stack_access_tup is not None:
            _, stack_access_addr1 = stack_access_tup
            if stack_access_addr1 is not None:
                # stack push via str e.g. ("str        r6, [sp, #0x8])
                self.stack_push_via_str = True
                # first convert to int
                self.stack_address = stack_access_addr1
                if self.cpu.c_func_heuristic:
                    self.stack_usage_since_last_call.add(stack_access_addr1)
                        
    def _process_stack_push_via_stm(self, asmline):
        ''' Process a stack push via "stm" command and set the `stack_push_objects` '''
        # stack push via stm (store multiple) e.g. "stm.w      sp, {r0, r3}"
        stack_regs_list = self.parse_util.parse_stack_push_via_stm(asmline, self.cpu.stack_pointer_register())
        if stack_regs_list is not None:
            self.stack_push_via_stm = True
            self.stack_push_objects = stack_regs_list
            
    def _get_val1_value(self, val1, var_assign1):
        ''' Get the proper value for val1 and return it '''
        val1_value = None
        if var_assign1 is not None:
            tmp = var_assign1.get_ivar_dest()  
            if isinstance(tmp, Register):
                val1_value = tmp
        if val1_value is None:
            val1_value = self.parse_util.register_class(val1)
        return val1_value
    
    def _get_val2_value(self, val2, remaining_types):
        ''' 
        Determine the class which belongs to val2 and return it.
        If the class is `Register` try to resolve the value from the registers dictionary.
        '''
        res = None
        # stack fetch
        if self.is_stack_fetch:
            res = self.get_cpu().get_stack()[self.stack_address]
        if res is None:
            # check for other types
            res = ParseUtil.get_fst_match(val2, remaining_types)
            # no match found
            if res is None:
                # wrap into register
                res = self.parse_util.parse_register(val2)
                # resolve register
                res_resolved = self.cpu.memory.registers.get_value_for_register(res)
                if res_resolved is None:
                    # try to match as hex
                    int_val_of_hex = self.parse_util.parse_hex(val2)
                    if int_val_of_hex is not None:
                        res = int_val_of_hex
                # could not resolve register and match as hex, use register
                else:
                    res = res_resolved
        return res 
