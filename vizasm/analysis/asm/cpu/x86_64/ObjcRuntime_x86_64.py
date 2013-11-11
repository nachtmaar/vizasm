'''
VizAsm

Created on 18.09.2013

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

from vizasm.analysis.asm.cpu.objcruntime.ObjectiveCRuntime import \
    ObjectiveCRuntime
from vizasm.model.asm.StackVar import StackVar
from vizasm.util import Util
from vizasm.util.Log import log


class ObjcRuntime_x86_64(ObjectiveCRuntime):
    ''' Objective-C runtime for x86_64 arch '''
    
    def create_and_store_method_selector_arguments(self, method_selector):
        '''
        Create and store the arguments for the `method_selector`.
        There will be as many arguments created as the `Selector` needs.
        But at most as many as the `selector_arg_registers` specifies.
        This also specifies the registers in which the arguments will be stored.
        
        The other ones have to be taken from the stack!
        
        Parameters
        ----------
        method_selector: Selector
            the `Selector` describing the method that is currently being read by the `Cpu`
        
        Raises
        ------
        SelectorOverloadedException
            if selector has more arguments than it needs
        '''
        cur_method_sel_args = 0
        if method_selector is not None:
            method_selector_cnt_needs_args = method_selector.cnt_needs_arguments() 
            cpu = self.cpu
            for i, reg in enumerate(cpu.selector_arg_registers(), 1):
                if i > method_selector_cnt_needs_args:
                    return
                method_selector_arg = ObjectiveCRuntime.create_method_selector_arg(i)
                method_selector.add_argument(method_selector_arg)
                cpu.memory.registers.set_value_for_register_ann_method_ead(reg, method_selector_arg)         
                cur_method_sel_args += 1
            # store remaining args as `StackVar`
            return self.create_and_store_remaining_method_selector_arguments(0, method_selector)
        
    def create_and_store_remaining_method_selector_arguments(self, start_addr, method_selector):
        '''
        Create and store the remaining arguments for the `method_selector`.
        There will be as many arguments created as the `Selector` still needs
        and stored as `StackVar`.
        
        Parameters
        ----------
        start_addr: int
            the suffix for the first `StackVar` argument (e.g. arg_4) 
        method_selector: Selector
            the `Selector` describing the method that is currently being read by the `Cpu`
        
        Raises
        ------
        SelectorOverloadedException
            if selector has more arguments than it needs
        '''
        cpu = self.cpu
        if method_selector is not None:
            STACKVAR_PREFIX = 'arg'
            addr = start_addr
            start = method_selector.cnt_has_arguments() + 1
            for i in range(start, method_selector.cnt_needs_arguments() + 1):
                method_sel_arg = ObjectiveCRuntime.create_method_selector_arg(i)
                # cut off the 0x prefix and use upper case for rest of address 
                stackvar_name = '%s_%s' % (STACKVAR_PREFIX, Util.hex_string_without_0x(addr).upper())
                # save argument as StackVar
                stackvar = StackVar(stackvar_name)
                cpu.memory.registers.set_value_for_register_ann_method_ead(stackvar, method_sel_arg)
                method_selector.add_argument(method_sel_arg)
                log.debug('method_selector arg %s = %s', method_sel_arg, stackvar)
                addr += cpu.pointer_size()        
