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
from vizasm.analysis.asm.cpu.x86.ASM_x86 import ASM_x86
from vizasm.analysis.asm.cpu.x86.ParseUtil_x86 import ParseUtil_x86
from vizasm.analysis.asm.cpu.x86.Register_x86 import Register_x86 as reg
from vizasm.analysis.asm.cpu.x86.ObjcRuntime_x86 import ObjcRuntime_x86

class  Cpu_x86(Cpu):
    ''' Cpu subclass for the x86_64 architecture. '''
    
    def __init__(self, superclasses_dict = None):
        parse_util = ParseUtil_x86(self, reg)
        objc_runtime = ObjcRuntime_x86(self, superclasses_dict)
        Cpu.__init__(self, ASM_x86(self, parse_util), parse_util, reg, superclasses_dict, objc_runtime)
    
#####################################################################################
# CallingConventionsInterface                                                       #
#####################################################################################    
     
    def destination_register(self):
        return None
    
    def selector_register(self):
        return None
    
    def fetches_all_arguments_from_stack(self):
        return True
    
    def selector_arg_registers(self):
        return []
    
    def return_register(self):
        return reg('eax')
    
    def nslog_arg_registers(self):
        return []
    
    def stack_pointer_register(self):
        return reg('esp')
    
    def frame_pointer_register(self):
        return reg('ebp')
    
    def floating_arg_registers(self):
        return None
    
#####################################################################################
# Overwritten Cpu Behavior                                                          #
#####################################################################################
    def pointer_size(self):
        return 4
    
    def ignore_hex_addr_call(self):
        ''' x86 disassemblies often call the next line -> ignore it
        Example: 
        00002d09 E800000000                      call       0x2d0e
        00002d0e 58                              pop        eax                                   ; XREF=0x2d09"" '''
        return True

