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
from vizasm.model.objc.arguments.Selector import Selector
from vizasm.model.objc.function.MsgSend import MsgSend
from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass

class ObjcRuntime_arm(ObjectiveCRuntime):
    ''' Objective-C runtime for arm arch '''
    
    def create_and_store_method_selector_arguments(self, method_selector):
        '''
        Create the `method_selector` arguments.
        The first ones are stored in the registers specified by `selector_arg_registers`.
        The remaining ones are pushed onto the stack (beginning at address 0x8)
        '''
        if method_selector is not None:
            cpu = self.cpu
            method_selector_cnt_needs_args = method_selector.cnt_needs_arguments() 
            selector_arg_registers = cpu.selector_arg_registers()
            cnt_args_registers = len(selector_arg_registers)
            for i in xrange(1, method_selector_cnt_needs_args + 1):
                method_selector_arg = ObjcRuntime_arm.create_method_selector_arg(i)
                # set value for register
                if i <= cnt_args_registers:
                    cpu.memory.registers.set_value_for_register_ann_method_ead(selector_arg_registers[i - 1], method_selector_arg)
                # push rest on stack
                else:
                    # +2 for 0x8 as beginning address
                    cpu.get_prev_stack_frame().add_from_idx(method_selector_arg, 2 + i - 1 - cnt_args_registers)
                    
    # TODO: HOPPER_ARM: REMOVE IF HOPPER ANNOTATION GETS BETTER!
    def msg_send_from_destination(self, destination, selector):
        ''' Overwritten to accept other ints as destination.
        Currently annotation in Hopper is not so good, leading often to hex values (parsed to int) in the `destination_register`. '''
        # temporary workaround to read a msgSend even if destination is integer (transformed from hex)
        # because Hopper is currently not annotating all destinations!
        msg_send = ObjectiveCRuntime.msg_send_from_destination(self, destination, selector)
        if msg_send is None:
            arm_fix = isinstance(destination, int)
            if selector is not None and arm_fix:
                msg_send = MsgSend(ObjcClass(str(destination)), [selector])
        return msg_send        
    
    # TODO: HOPPER_ARM: REMOVE IF HOPPER ANNOTATION GETS BETTER!
    def get_current_selector_check_sel_type(self, objc_msgSend_stret = False):
        ''' 
        Overwritten to accept other types as Selector.
        Currently annotation in Hopper is not so good, leading often to hex values etc. in the `selector_register`. 
        '''
        res = self._get_current_selector(objc_msgSend_stret, raise_cpu_selector_wrong_type_exception = False)        
        if not isinstance(res, Selector):
            return Selector(str(res))
        return res    