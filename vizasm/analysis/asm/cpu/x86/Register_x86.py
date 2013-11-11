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

from vizasm.model.asm.Register import Register

REGISTER_DICT = dict(rax = ['eax', 'ax', 'ah', 'al'], rbx = ['ebx', 'bx', 'bl'],
                          rcx = ['ecx', 'cx', 'cl'], rdx = ['edx', 'dx', 'dl'],
                          rsi = ['esi', 'si', 'sil'], rdi = ['edi', 'di', 'dil'],
                          rbp = ['ebp', 'bp', 'bpl'], rsp = ['esp', 'sp', 'spl'],
                          r8 = ['r8d', 'r8w', 'r8b'], r9 = ['r9d', 'r9w', 'r9b'],
                          r10 = ['r10d', 'r10w', 'r10L', 'r10b'], r11 = ['r11d', 'r11w', 'r11L', 'r11b'],
                          r12 = ['r12d', 'r12w', 'r12L', 'r12b'], r13 = ['r13d', 'r13w', 'r13L', 'r13b'],
                          r14 = ['r14d', 'r14w', 'r14L', 'r14b'], r15 = ['r15d', 'r15w', 'r15L', 'r15b']
                    )
    
class Register_x86(Register):
    '''
    Implements an register for the x86 architecture 
    
    Notes
    -----
    Register list taken from: http://msdn.microsoft.com/en-us/library/ff561499.aspx
    '''
    
    def __init__(self, register):
        Register.__init__(self, register, REGISTER_DICT)
