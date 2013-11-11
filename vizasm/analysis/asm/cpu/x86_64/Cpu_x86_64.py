'''
VizAsm

Created on 26.03.2013

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
from vizasm.analysis.asm.cpu.x86.ParseUtil_x86 import ParseUtil_x86
from vizasm.analysis.asm.cpu.x86_64.ASM_x86_64 import ASM_x86_64
from vizasm.analysis.asm.cpu.x86_64.ObjcRuntime_x86_64 import ObjcRuntime_x86_64
from vizasm.analysis.asm.cpu.x86_64.ParseUtil_x86_64 import ParseUtil_x86_64
from vizasm.analysis.asm.cpu.x86_64.Register_x86_64 import \
    Register_x86_64 as reg


class  Cpu_x86_64(Cpu):
    ''' Cpu subclass for the x86_64 architecture. '''
    
    def __init__(self, superclasses_dict = None):
        parse_util = ParseUtil_x86_64(self, reg)
        objc_runtime = ObjcRuntime_x86_64(self, superclasses_dict)
        Cpu.__init__(self, ASM_x86_64(self, parse_util), parse_util, reg, superclasses_dict, objc_runtime)

#####################################################################################
# CallingConventionsInterface                                                       #
#####################################################################################    
     
    def destination_register(self):
        return reg('rdi')
    
    def selector_register(self):
        return reg('rsi')

    def fetches_all_arguments_from_stack(self):
        return False
        
    def selector_arg_registers(self):
        return self.reg_list(['rdx', 'rcx', 'r8', 'r9'])
    
    def return_register(self):
        return reg('rax')
    
    def nslog_arg_registers(self):
        return self.reg_list(['rsi', 'rdx', 'rcx', 'r8', 'r9'])
    
    def stack_pointer_register(self):
        return reg('rsp')
    
    def frame_pointer_register(self):
        return reg('rbp')
    
    def floating_arg_registers(self):
        return self.reg_list(['xmm0', 'xmm1', 'xmm2', 'xmm3', 'xmm4', 'xmm5', 'xmm6', 'xmm7'])
    
    def reg_list(self, regs):
        return self._reg_list(regs, reg)
    
#####################################################################################
# Overwritten Cpu Behavior                                                          #
#####################################################################################
    def pointer_size(self):
        return 8
                
    def ignore_hex_addr_call(self):
        return True
    
if __name__ == '__main__':
    cpu = Cpu_x86_64()
    print cpu
    pu = ParseUtil_x86(cpu, reg)
    print 'objc_msgSend_spret destination register: %s' % (cpu.next_reg_for_spret(cpu.destination_register()))
    print 'objc_msgSend_spret selector register: %s' % (cpu.next_reg_for_spret(cpu.selector_register()))
    print 'objc_msgSend_spret selector arg registers: %s' % (cpu.next_regs_for_spret(cpu.selector_arg_registers()))
        
