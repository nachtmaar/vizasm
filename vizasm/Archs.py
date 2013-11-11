'''
VizAsm

Created on 09.10.2013

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

Architecture stuff ''' 

# Available architectures
ARCH_X86 = 'x86'
ARCH_X86_64 = 'x86_64'
ARCH_ARM = 'arm'
ARCH_ANYTHING = 'anything'

# available architectures
ARCHS = [ARCH_X86, ARCH_X86_64, ARCH_ARM]

def transform_hopper_arch(arch_str):
    ''' Transform the hopper architecture to the internal string representation of the arch ''' 
    HOP_ARCH_X86 = 'i386'
    HOP_ARCH_X86_64 = 'x86_64'
    HOP_ARCH_ARM = 'ARM'
    HOP_ARCH_ARM_THUMB = 'ARM (Thumb)'
    
    vizasm_arch_str = None
    if arch_str == HOP_ARCH_X86:
        vizasm_arch_str = ARCH_X86
    elif arch_str == HOP_ARCH_X86_64:
        vizasm_arch_str = ARCH_X86_64
    elif arch_str in [HOP_ARCH_ARM, HOP_ARCH_ARM_THUMB]:
        vizasm_arch_str = ARCH_ARM
        
    return vizasm_arch_str
