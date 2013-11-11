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

from vizasm.analysis.asm.cpu.Cpu import Cpu
from vizasm.analysis.asm.cpu.arm.Asm_arm import Asm_arm
from vizasm.analysis.asm.cpu.arm.ObjcRuntime_arm import ObjcRuntime_arm
from vizasm.analysis.asm.cpu.arm.ParseUtil_arm import ParseUtil_arm
from vizasm.analysis.asm.cpu.arm.Register_Arm import Register_arm as reg
from vizasm.analysis.asm.cpu.memory.StackFrame import StackFrame


class Cpu_arm(Cpu):
    '''
    Cpu for the arm architecture.
    
    Parameters
    ----------
    __prev_stack_frame: StackFrame
        Use to read method arguments, cause they are stored in the previous stack frame.
        See `https://developer.apple.com/library/ios/documentation/Xcode/Conceptual/iPhoneOSABIReference/Articles/ARMv6FunctionCallingConventions.html`
        for the stack layout. 
    '''
    def __init__(self, superclasses_dict = None):
        parse_util = ParseUtil_arm(self, reg)
        objc_runtime = ObjcRuntime_arm(self, superclasses_dict)
        Cpu.__init__(self, None, parse_util, reg, superclasses_dict, objc_runtime)
        # init asm after cpu! because it used the cpu and at this time 
        # the cpu is still uninitialized if self used as parameter
        asm_arm = Asm_arm(self, parse_util)
        self.assignment_matching_system = asm_arm
        self.__prev_stack_frame = StackFrame(self)

    def get_prev_stack_frame(self):
        return self.__prev_stack_frame

    def set_prev_stack_frame(self, value):
        self.__prev_stack_frame = value

    prev_stack_frame = property(get_prev_stack_frame, set_prev_stack_frame, None, "__prev_stack_frame(StackFrame) -- Use to read method arguments, cause they are stored in the previous stack frame.")
    
#####################################################################################
# CallingConventionsInterface                                                       #
#####################################################################################    

    def destination_register(self):
        return reg('r0')
    
    def selector_register(self):
        return reg('r1')
    
    def selector_arg_registers(self):
        return self.reg_list(['r2', 'r3'])
    
    def return_register(self):
        return reg('r0')
    
    def nslog_arg_registers(self):
        return self.reg_list(['r1', 'r2', 'r3'])
    
    def stack_pointer_register(self):
        return reg('sp')
    
    def frame_pointer_register(self):
        return reg('r7')
    
    def floating_arg_registers(self):
        return []    
    
    def fetches_all_arguments_from_stack(self):
        return False

    def reg_list(self, regs):
        return self._reg_list(regs, reg)
    
#####################################################################################
# Overwritten Cpu Behavior                                                          #
#####################################################################################

    def pointer_size(self):
        return 4
    
    def ignore_hex_addr_call(self):
        return True
    
