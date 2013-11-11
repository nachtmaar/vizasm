'''
VizAsm

Created on 31.08.2013

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

from vizasm.analysis.asm.cpu.AsmRegEx import AsmRegEx

class AsmRegEx_arm(AsmRegEx):
    ''' 
    Contains regular expressions (mostly in verbose mode) used for analyzing the assembler file on the arm architecture.  
    
    Parameters
    ----------
    RE_IVAR
        match e.g. "IVAR_0x291c"
         
    RE_CLASSREF
        match e.g. "@bind__OBJC_CLASS_$_UIScreen"
         
    RE_IMP_SYMBOLSTUB
        match e.g "imp___symbolstub1__objc_msgSend" 
    
    RE_IMP_NL_SYMBOL_PTR
        match e.g. "@imp___nl_symbol_ptr__objc_retain"
        
    RE_ASSINGMENT_SPLIT
        match e.g.  "ldr        r8, [sp], #0x4" or 
                    "ldr        r1, [r0] " or
                    "cvtss2sd   xmm2, xmm2"
                    
    RE_OFFSET_ADDRESSING
        match .e.g "[sp, #0x8]"
    
    RE_CALL_INSTRUCTION
        match e.g. "blx        imp___symbolstub1__objc_msgSend"
        
    RE_ADD
        match e.g. "add r7, sp, #0xc" or
                   "add        r7, sp" or
                   "add        r7, #0xc"
                    
    RE_REGISTER
        match e.g. "ro"
    
    RE_ANNOTATED_SUPERCALL
         match e.g. "; call to super: 0xbb4e"
    '''    
    
    RE_IMP_STUBS_GR_IMP_SYMBOLSTUB = 'imp_symbolstub'
    RE_IMP_SYMBOLSTUB = r'''
 (?:imp[_]{3}symbolstub1[_]{2,})  # imp___symbolstub1__
 (?P<%s>.*)                      # objc_msgSend
 ''' % RE_IMP_STUBS_GR_IMP_SYMBOLSTUB
    
    # @imp___nl_symbol_ptr__objc_retain
    RE_IMP_NL_SYMBOL_PTR_GR_NAME = 'name'
    RE_IMP_NL_SYMBOL_PTR = '''
    @imp[_]{3}nl[_]symbol[_]ptr[_]{2} # @imp___nl_symbol_ptr__
    (?P<%s>\S+)                       # objc_retain
    ''' % RE_IMP_NL_SYMBOL_PTR_GR_NAME

    RE_CLASSREF_GR_CLASSREF = 'classref'
    RE_CLASSREF = '''
    @bind[_]{2}OBJC[_]CLASS[_][$][_] # @bind__OBJC_CLASS_$_
    (?P<%s>\S+)                      # UIScreen
    ''' % RE_CLASSREF_GR_CLASSREF 
    
    RE_ASSINGMENT_SPLIT_GR_OP = 'op'
    RE_ASSINGMENT_SPLIT_GR_VAL1 = 'val1'
    RE_ASSINGMENT_SPLIT_GR_VAL2 = 'val2'
    #  ldr        r8, [sp], #0x4    
    RE_ASSINGMENT_SPLIT = r'''
 (?P<%s>(add|mov|ldr|.*cvt|st(m|r)).*?)    # ldr
 \s+
 (?P<%s>.*?)                                # r8
 ,\s*                                       # ,
 =?                                         # optional "=" for ldr
 (?P<%s>.*)                                 # [sp], #0x4
 ''' % (RE_ASSINGMENT_SPLIT_GR_OP, RE_ASSINGMENT_SPLIT_GR_VAL1, RE_ASSINGMENT_SPLIT_GR_VAL2)
 
    RE_CALL_INSTRUCTION_GR_CALLED = 'called'
    RE_CALL_INSTRUCTION = '''
    blx?             # bl or blx
    \s*              # whitespace
    (?P<%s>\S+)      # called
    ''' % RE_CALL_INSTRUCTION_GR_CALLED
    
    RE_IVAR_GR_NAME = 'ivar_addr'
    RE_IVAR = r'''
 IVAR[_]      # IVAR_
 (?P<%s>\S+)  # 0x291c
 ''' % (RE_IVAR_GR_NAME)
 
    # [ro]
    RE_REGISTER_GR_NAME = 'name'
    RE_REGISTER = '''
    \[?               # "[" is optional
    (?P<%s>
     (
      [^]]             # no ]
      \S               # no whitespace
     )+                # match all but whitespace and ]      
    )      
    \]?               # "]" is optional 
    ''' % (RE_REGISTER_GR_NAME)
    
    # [sp, #0x8]
    RE_OFFSET_ADDRESSING_GR_BASE_REGISTER = 'base_register'
    RE_OFFSET_ADDRESSING_GR_OFFSET = 'offset'
    RE_OFFSET_ADDRESSING = '''
    \[             # [
    (?P<%s>\w+)    # sp
    (
    ,\s*           # , 
    [#]?           # #
    (?P<%s>\w+)    # 0x8 
    )?
    \]             # ]
    ''' % (RE_OFFSET_ADDRESSING_GR_BASE_REGISTER, RE_OFFSET_ADDRESSING_GR_OFFSET)
    
    RE_ADD_GR_DEST = 'dest'
    RE_ADD_GR_OPERAND1 = 'operand1'
    RE_ADD_GR_OPERAND2 = 'operand2'
    # add        r7, sp, #0xc
    RE_ADD = '''
    add\w*         # add
    \s+            # whitespace
    (?P<%s>\w+)    # r7
    ,              # ,
    \s*            # whitespace
    (?P<%s>\#?\w+) # sp
    (
    ,\s*           # , whitespace
    (?P<%s>\#?\w+) # #0xc
    )*
    ''' % (RE_ADD_GR_DEST, RE_ADD_GR_OPERAND1, RE_ADD_GR_OPERAND2) 
    
    # ; call to super: 0xbb4e
    RE_ANNOTATED_SUPERCALL_GR_SUPERREF_ADDR = 'superref_addr'
    RE_ANNOTATED_SUPERCALL = '''
    call\s+to\s+super[:]\s+        # "; call to super:"  
    (?P<%s>0x\w+)                  # 0xbb4e
    ''' % (RE_ANNOTATED_SUPERCALL_GR_SUPERREF_ADDR)
    
    RE_STACK_PUSH_GR_REGISTERS = 'registers'
    @staticmethod
    def compiled_re_stack_push_via_stm(stack_pointer, asmline):
        ''' Read a stack push via "stm" like e.g. "stm.w      sp, {r3, r11}"
        and return the re match object.
        Use `RE_STACK_PUSH_GR_REGISTERS` to get the list<str> of pushed registers '''
        
        RE_STACK_PUSH = '''
        stm.*?                # stm
        \s*                   # whitespace
        %s                    # stack pointer
        ,\s*                  # , 
        [{]                   # {
        (?P<%s>.*)            # r3, r11
        [}]                   # }
        ''' % (stack_pointer, AsmRegEx_arm.RE_STACK_PUSH_GR_REGISTERS)
        stack_push_match = AsmRegEx_arm.compiled_vre(RE_STACK_PUSH).search(asmline)
        if stack_push_match is not None:
            return stack_push_match
        return None
    
    RE_STACK_GR_STACK_POINTER = 'stack_pointer'
    RE_STACK_GR_ADDRESS = 'stack_address'
    RE_STACK_GR_OFFSET = 'stack_offset'
    @staticmethod 
    def compiled_re_stack(stack_pointer_name, frame_pointer_name):
        ''' 
        Return a compiled regular expression that matches  e.g. "[sp, #0x8]" or "[sp], #0x4"
        Use `RE_STACK_GR_ADDRESS` group key to get the stack address.
            
        Parameters
        ----------
        stack_pointer_name: string
            the name of stack pointer register (e.g. "sp")
        '''
        RE_STACK = r'''
         \[                              # [
         (?P<%s>%s|%s)                   # stack pointer name or frame pointer name
         (
                 (
                 \]
                 ,\s+                            # ,
                 [#]                             # #
                 (?P<%s>0x\w+)                   # 0x8
                 )
             |                                   # or
                 (                
                 ,\s+                            # , 
                 [#]
                 (?P<%s>0x\w+)                   # #0x8
                 \]                              # ]
                 )
            |
                \]                              # ]
         )

        ''' % (AsmRegEx_arm.RE_STACK_GR_STACK_POINTER, stack_pointer_name, frame_pointer_name, AsmRegEx_arm.RE_STACK_GR_OFFSET, AsmRegEx_arm.RE_STACK_GR_ADDRESS)
        return AsmRegEx.compiled_vre(RE_STACK) 
    
    @staticmethod
    def stack_pointer_sub(stack_pointer_str, asmline):
        '''
        Read a line like e.g. "sub        sp, #0x14"
        and return the value that is being subtracted from the stack pointer as string.
        None if did not match. 
        '''
        
        RE_SP_SUB_GR_SUBTRACTED = 'subtracted'
        RE_SP_SUB = '''
        sub\w*
        \s*
        %s,
        \s*
        \#(?P<%s>\w+)
        ''' % (stack_pointer_str, RE_SP_SUB_GR_SUBTRACTED)
        
        re_sp_sub_match = AsmRegEx_arm.compiled_vre(RE_SP_SUB).search(asmline)
        if re_sp_sub_match is not None:
            return re_sp_sub_match.group(RE_SP_SUB_GR_SUBTRACTED)
        return None