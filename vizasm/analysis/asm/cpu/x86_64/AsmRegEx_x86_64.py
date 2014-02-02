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

from vizasm.analysis.asm.cpu.AsmRegEx import AsmRegEx


class AsmRegEx_x86_64(AsmRegEx):
    ''' 
    Contains regular expressions (mostly in verbose mode) used for analyzing the assembler file on the x86_64 architecture  
    
    Parameters
    ----------
    RE_STACKVAR
        match e.g. "[ss:rbp-0x30+var_40]" or "qword [ss:rbp-0x0+var_m8]"
         
    RE_VAR_ASSIGNMENT
        match e.g. "[ds:rdx+rsi]"
         
    RE_IVAR
        match e.g. "[ds:_OBJC_IVAR_$_AppDelegate.obj3]"
         
    RE_CLASSREF
        match e.g. "[ds:objc_classref_Object1]"
         
    RE_FRAMEWORKCLASS
        match e.g. "[ds:bind__OBJC_CLASS_$_NSUserDefaults]"
         
    __RE_IMP
        Used for RE_IMP_STUBS and RE_IMP_GOT. DO NOT USE DIRECTLY !
        
    RE_IMP_STUBS
        match e.g "imp___stubs__NSApplicationMain", "imp___stubs__objc_retain", "imp___stubs__objc_msgSend" ... 
        
    RE_IMP_GOT
        match e.g "imp___got__NSStreamSocketSecurityLevelKey", "imp___got___NSConcreteStackBlock", "imp___got____gxx_personality_v0" 
         
    RE_ASSINGMENT_SPLIT
        match e.g.  "mov        rax, qword [ss:rbp-0x70+var_88]" or 
                    "lea        rax, qword [ds:objc_msg_alloc] ; @selector(alloc)" or
                    "cvtss2sd   xmm2, xmm2"
    
    RE_CALL_INSTRUCTION
        match e.g. "call       imp___stubs__objc_msgSend" or "jmp        qword [ds:imp___got__objc_msgSend]"
         
    RE_REGISTER
        match e.g. "ds:[rdi]", "rdi", "qword [ds:rdi]"
        
    RE_ADD_METHOD_ARG_STACK
        match e.g. "arg_0"
    '''    

    RE_CLASSREF_GR_CLASSREF = 'classref'
    RE_CLASSREF = r'''
 \[ds\:                 # [ds:
 objc[_]classref[_]     # objc_classref_
 (?P<%s>\w+)            # Object1
 \]                     # ]
''' % (RE_CLASSREF_GR_CLASSREF)

    RE_FRAMEWORKCLASS_GR_FCLASS = 'frameworkclass'
    RE_FRAMEWORKCLASS = r'''
 \[ds\:                         # [ds:
 bind[_]{2}OBJC[_]CLASS[_]\$[_] # bind__OBJC_CLASS_$_
 (?P<%s>\w+)                    # NSUserDefaults
 \]                             # ]
''' % (RE_FRAMEWORKCLASS_GR_FCLASS)

    RE_IVAR_GR_CLASS = 'class'
    RE_IVAR_GR_IVAR = 'ivar'
    RE_IVAR = r'''
 \[ds\:                 # [ds:
 [_]OBJC[_]IVAR[_]\$[_] # _OBJC_IVAR_$_
 (?P<%s>\w+)            # AppDelegate
 \.                     # .
 (?P<%s>\w+)            # obj3
 \]                     # ]
''' % (RE_IVAR_GR_CLASS, RE_IVAR_GR_IVAR)

    RE_VAR_ASSIGNMENT_GR_SELF_REGISTER = 'class'
    RE_VAR_ASSIGNMENT_GR_IVAR_REG = 'var'
    RE_VAR_ASSIGNMENT = r'''
 \[ds\:                 # [ds:
 (?P<%s>\w+)            # rdx
 \+                     # +
 (?P<%s>\w+)            # rsi
 (\+0x0)?               # + 0x0
 \]                     # ]
''' % (RE_VAR_ASSIGNMENT_GR_SELF_REGISTER, RE_VAR_ASSIGNMENT_GR_IVAR_REG)

    RE_ASSINGMENT_SPLIT_GR_VAL1 = 'val1'
    RE_ASSINGMENT_SPLIT_GR_VAL2 = 'val2'
    # mov        rax, qword [ss:rbp-0x70+var_88]
    RE_ASSINGMENT_SPLIT = r'''
 (mov[a-z]*|lea|cvt.*)\s+  # mov
 (?P<%s>.*?)              # rax
 ,\s*                     # ,
 (?P<%s>.*)               # qword [ss:rbp-0x70+var_88]
 ''' % (RE_ASSINGMENT_SPLIT_GR_VAL1, RE_ASSINGMENT_SPLIT_GR_VAL2) 
 
    RE_CALL_INSTRUCTION_GR_CALLED = 'called'
    RE_CALL_INSTRUCTION = r'''
 (call|jmp)\s+            # call  
 (?P<%s>.*)               # imp___stubs__objc_msgSend
''' % (RE_CALL_INSTRUCTION_GR_CALLED)

    RE_STACKVAR_GR_STACKVAR = 'stackvar'       
    RE_STACKVAR = r'''
 \[ss\:                 # [ss:
 [\w\-]+\+              # rbp-0x30+ 
 (?P<%s>\w+)            # var_40
 ''' % (RE_STACKVAR_GR_STACKVAR)
        
    __RE_IMP = r'''
 (\[(ds|ss)[:])?                  # [ds: <- optional    
 (?:imp[_]{3}(
     %s[_]{2,}                    # imp___stubs__ or imp___got__ or imp___symbol_stub(1)
     |        
     nl[_]symbol[_]ptr[_]{2}      # nl_symbol_ptr__
     ))
 (?P<%s>\w+)                      # NSLog
 (\])?                            # ] <- optional
 ''' 

    RE_IMP_STUBS_GR_IMP_STUBS = 'imp_stubs'
    RE_IMP_STUBS = __RE_IMP % ('(stubs|symbol_stub\d?)', RE_IMP_STUBS_GR_IMP_STUBS)

    RE_IMP_GOT_GR_IMP_GOT = 'imp_got'
    RE_IMP_GOT = __RE_IMP % ('got', RE_IMP_GOT_GR_IMP_GOT)

    RE_REGISTER_GR_QWORD_REG = 'qword_reg'
    RE_REGISTER_GR_DS_REG = 'ds_reg'
    RE_REGISTER_GR_REG = 'reg'
    RE_REGISTER_REG = '^[a-z]+[a-z0-9A-Z]{,3}$'
    RE_REGISTER_DS_REG = '[a-z]+[a-z0-9A-Z]{,3}'
    RE_REGISTER = r'''
(?:^(ds|ss)[:]\[)(?P<ds_reg>%s)(?:\]$)                # ds:[rdi] or
|
(?P<reg>%s)                                           # rdi or
|
(?:(byte|word)\ \[(ds|ss)[:])(?P<qword_reg>%s)(?:\])  # qword [ds:rdi]
''' % (RE_REGISTER_DS_REG, RE_REGISTER_REG, RE_REGISTER_DS_REG)

    RE_STACK_GR_ADDRESS = 'stack_adress'
    RE_STACK_GR_REG = 'stack_register'
    
    # arg_0
    RE_ADD_METHOD_ARG_STACK_GR_ARG_NR = 'arg_nr'
    RE_ADD_METHOD_ARG_STACK = '''
    arg[_]
    (?P<%s>\w+)
    ''' % RE_ADD_METHOD_ARG_STACK_GR_ARG_NR
     
    @staticmethod 
    def compiled_re_stack(stack_pointer_name):
        ''' 
        Return a compiled regular expression that matches  e.g. "qword [ss:rsp+0x8]"
        Use `RE_STACK_GR_ADDRESS` group key to get the stack address.
            
        Parameters
        ----------
        stack_pointer_name: string
            the name of stack pointer register (e.g. "rsp")
        '''
        RE_STACK = r'''
         \[ss:                           # [ss:
         (?P<%s>%s)                      # stack pointer name
         (\+                             # + 
         (?P<%s>0x\w+))*                 # 0x8 or empty -> 0x0
         \]                              # ]
        ''' % (AsmRegEx_x86_64.RE_STACK_GR_REG, stack_pointer_name, AsmRegEx_x86_64.RE_STACK_GR_ADDRESS)
        return AsmRegEx.compiled_vre(RE_STACK)        