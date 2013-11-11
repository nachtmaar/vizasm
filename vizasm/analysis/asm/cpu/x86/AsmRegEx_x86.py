'''
Created on 23.08.2013

@author: nils

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

from vizasm.analysis.asm.cpu.x86_64.AsmRegEx_x86_64 import AsmRegEx_x86_64

class AsmRegEx_x86(AsmRegEx_x86_64):
    ''' 
    Contains regular expressions (mostly in verbose mode) used for analyzing the assembler file on the x86 architecture. 
    
    Parameters
    ----------
    RE_CLASSREF
        match e.g. "[ds:cls_NSAssertionHandler]" or "dword [ds:eax-0x25e1+cls_Object1]"
         
    __RE_IMP
        Used for RE_IMP_STUBS and RE_IMP_GOT. DO NOT USE DIRECTLY !
        
    RE_IMP_STUBS
        match e.g "imp___stubs__NSApplicationMain", "imp___stubs__objc_retain", "imp___stubs__objc_msgSend" ... 
        
    RE_VAR_ASSIGNMENT
        match e.g. "dword [ds:ecx+0x8]"
        
    RE_IMP_NL_SYMBOL_PTR
        match e.g "[ds:eax-0x221e+imp___nl_symbol_ptr__NSStreamSocketSecurityLevelKey]"
    '''    
    
    __RE_IMP = r'''
 (\[(ds|ss)[:])?                 # [ds: <- optional    
 (?:imp[_]{3}symbol[_]%s[_]{2,}) # imp___symbol_stub__          <- this seems to be the 32 bit version
 (?P<%s>\w+)                     # NSLog
 (\])?                           # ] <- optional
 ''' 
    RE_IMP_STUB_GR_IMP_STUB = 'imp_stub'
    RE_IMP_STUB = __RE_IMP % ('stub', RE_IMP_STUB_GR_IMP_STUB)

    RE_CLASSREF_GR_CLASSREF = 'classref'
    RE_CLASSREF = r'''
 \[ds\:                 # [ds:
 ([-\w]+[+])*           # eax-0x25e1+
 cls[_]                 # cls_
 (?P<%s>\w+)            # Object1
 \]                     # ]
''' % (RE_CLASSREF_GR_CLASSREF)

    RE_VAR_ASSIGNMENT_GR_SELF_REGISTER = 'class'
    RE_VAR_ASSIGNMENT_GR_IVAR_ADDR = 'var'
    RE_VAR_ASSIGNMENT = r'''
 \[ds\:                 # [ds:
 (?P<%s>\w+)            # ecx
 \+                     # +
 (?P<%s>0x\w+)          # 0x8
 \]                     # ]
''' % (RE_VAR_ASSIGNMENT_GR_SELF_REGISTER, RE_VAR_ASSIGNMENT_GR_IVAR_ADDR)

    RE_IMP_NL_SYMBOL_PTR_GR_NAME = 'name'
    RE_IMP_NL_SYMBOL_PTR = '''
 imp[_]{3}nl[_]symbol[_]ptr[_]{2}       # imp___nl_symbol_ptr__ 
 (?P<%s>\w+)                            # NSStreamSocketSecurityLevelKey 
    ''' % RE_IMP_NL_SYMBOL_PTR_GR_NAME
