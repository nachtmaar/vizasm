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

from vizasm.analysis.asm.cpu.x86_64.ObjcRuntime_x86_64 import ObjcRuntime_x86_64
from vizasm.model.asm.StackVar import StackVar
from vizasm.util.Log import log


class ObjcRuntime_x86(ObjcRuntime_x86_64):
    ''' Objective-C runtime for x86 arch '''

    def store_self_cmd_for_stack_fetching_cpu(self, objc_class, selector):
        ''' Store self and _cmd in the appropriate place ''' 
        # self and _cmd are the first arguments on the stack -> push it
        cpu = self.cpu
        cpu.memory.registers.set_value_for_register_ann_method_ead(StackVar('arg_0'), objc_class)
        cpu.memory.registers.set_value_for_register_ann_method_ead(StackVar('arg_4'), selector)
        log.debug('added self and _cmd as StackVar: %s', cpu.memory.registers)
        
    def create_and_store_method_selector_arguments(self, method_selector):
        '''
        Create and store the arguments for the `method_selector`.
        There will be as many arguments created as the `Selector` needs
        and stored as `StackVar`.
        
        Parameters
        ----------
        method_selector: Selector
            the `Selector` describing the method that is currently being read by the `Cpu`
        
        Raises
        ------
        SelectorOverloadedException
            if selector has more arguments than it needs
        '''
        # start address is 0x8 (var_0 -> self, var_4 _> _cmd)
        return self.create_and_store_remaining_method_selector_arguments(0x8, method_selector)
                
