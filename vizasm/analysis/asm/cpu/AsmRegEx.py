'''
VizAsm

Created on 20.03.2013

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

from vizasm.RegEx import RegEx
from vizasm.util import Util
from itertools import imap

class AsmRegEx(RegEx):
    ''' 
    Contains regular expressions (mostly in verbose mode) used for analyzing the assembler file 
    
    Parameters
    ----------
    RE_SELECTOR
        match e.g. "@selector(objectForKey:)"
         
    RE_BASIC_BLOCK
        match e.g. "; Basic Block Input Regs: rax rdx rsi rdi -  Killed Regs: rax rcx rdx rsp rbp rsi rdi r8"
         
    RE_METH_IMPL
        match e.g. "methImpl_AppDelegate_applicationDidFinishLaunching_"
        or "methImpl_static_Segment_demangleNoSuffix"
        
    RE_CATEGORY
        match category method like e.g. "+[NSURLRequest(AnyHttpsCert) allowsAnyHTTPSCertificateForHost:]_100002120:" (static category method) or "-[NSURLRequest(AnyHttpsCert) initWithURL:cachePolicy:timeoutInterval:]_100002060:" (class category method)

    RE_HEX_VALUE
        match e.g. "OxFF or 0xff" or "#0xFF" (arm)
    
    SEARCH_NOP
        use to search for nop command
    
    RE_MATCH_ENTRYPOINT
        use to identify entry point in asm file
        
    RE_OWN_C_METHOD_DEF
        match .e.g "// cFunction(int, int, int)"
        
    RE_OWN_C_METHOD_CALLED
        match e.g. "cFunction(int, int, int)"
        
    RE_SUB
        match e.g. "sub_1001bc366:"
        
    RE_CALLED_SUB
        match e.g. "sub_1001bc366"
        
    RE_C_METHOD
        match e.g. "_CGPointMake_10002c4e0_1:"
        
    RE_CALLED_C_METHOD
        match e.g. "_CGPointMake_10002c4e0_1"
        
    RE_CLASS_PARENT
        match e.g. "Class Object1 (parent class: SuperObject)"
        
    RE_FORMAT_STRING
        match e.g. @""%s%d' but not '@"%%"' and not '@"Defaults"'. The string must contain a format argument like e.g. %@ 
        
    RE_STRING
        match e.g. '@"defaults"'         
    '''
    
    # use to match only if string begins with whitespace
    __ONLY_WS_AT_BEGINNING = '^\s+'
    
    RE_SELECTOR_GR_SELECTOR = 'selector'
    RE_SELECTOR = r'''
 @selector\(            # @selector(
 (?P<%s>[\w:]+)         # objectForKey:
 \)                     # )
 ''' % (RE_SELECTOR_GR_SELECTOR)

    RE_BASIC_BLOCK_INPUT_REGS = 'input_regs'
    RE_BASIC_BLOCK_KILLED_REGS = 'killed_regs'
    RE_BASIC_BLOCK = r'''
 Basic\ Block\ Input\ Regs\:\s*   # ; Basic Block Input Regs: 
 (?P<%s>[\w <>]+)                 # rax rdx rsi rdi
 \s+-\s+                          #  -  
 Killed\ Regs\:\s*                # Killed Regs: 
 (?P<%s>[\w ]+)                   # rax rcx rdx rsp rbp rsi rdi r8
 \s*
''' % (RE_BASIC_BLOCK_INPUT_REGS, RE_BASIC_BLOCK_KILLED_REGS)  # rax rcx rdx rsp rbp rsi rdi r8

    RE_METH_IMPL_GR_CLASS = 'class'
    RE_METH_IMPL_GR_SELECTOR = 'selector'
    RE_METH_IMPL_GR_STATIC = 'static'
    RE_METH_IMPL = r'''
    ^\s+                                   # only whitespace at the beginning 
    (methImpl|method|meth)[_]              # methImpl_ or method_ or meth_
    (?P<%s>static)?_?                      # static_
    (?P<%s>([A-Za-z0-9]+[_]*))             # AppDelegate
    [_]                                    # _
    (?P<%s>([A-Za-z0-9]+[_]*)+)            # applicationDidFinishLaunching_
    ''' % (RE_METH_IMPL_GR_STATIC, RE_METH_IMPL_GR_CLASS, RE_METH_IMPL_GR_SELECTOR)

    
    RE_CATEGORY_ON_CLASS = 'on_class'
    RE_CATEGORY_CLASS = 'class'
    RE_CATEGORY_SELECTOR = 'selector'
    RE_CATEGORY_STATIC_SYMBOL = 'selector_type'
    RE_CATEGORY = r'''
 (?P<%s>[+]|-)+      # starts with + or -
 \[                  # [ 
 (?P<%s>\w+)         # NSURLRequest
 \((?P<%s>\w+)\)     # AnyHttpsCert
 \s+                 # whitespace
 (?P<%s>[\w:]+)      # initWithURL:cachePolicy:timeoutInterval:
 \]                  # ]
 _\S+:               # _100002060: 
''' % (RE_CATEGORY_STATIC_SYMBOL, RE_CATEGORY_ON_CLASS, RE_CATEGORY_CLASS, RE_CATEGORY_SELECTOR)
    RE_CATEGORY_SYMBOL_STATIC = '+'
    RE_CATEGORY_SYMBOL_NON_STATIC = '-'
    
    RE_HEX_VALUE_GR_HEX_VALUE = 'hex_value'
    RE_HEX_VALUE = r'''
 \#?               # optional with leading "#" (arm)
 (?P<%s>
 0x[0-9a-zA-Z]+    # 0xFF
 )     
 ''' % (RE_HEX_VALUE_GR_HEX_VALUE)

    # cFunction(int, int, int)
    RE_OWN_C_METHOD_BASE_GR_NAME = 'name'
    RE_OWN_C_METHOD_BASE_GR_ARGS = 'args'
    RE_OWN_C_METHOD_BASE = '''
    \s*
    (?P<%s>[^@]*) # match all but @selector(...) - cFunction
    [(]           # (
    (?P<%s>.*)    # int, int, int
    [)]           # )
    ''' % (RE_OWN_C_METHOD_BASE_GR_NAME, RE_OWN_C_METHOD_BASE_GR_ARGS)
    
    # // cFunction(int, int, int)
    RE_OWN_C_METHOD_DEF = '%s%s' % ('[/]{2}', RE_OWN_C_METHOD_BASE)
    
    # ; cFunction(int, int, int)
    RE_OWN_C_METHOD_CALLED = '%s%s' % ('[;]', RE_OWN_C_METHOD_BASE)
    
    #    [/]{2}
    # base re for RE_SUB and RE_CALLED_SUB
    _RE_CALLED_SUB_BASE = '''
    (?P<%s>
    sub[_]         # sub_
    \S+)           # 1001bc366
    '''
    RE_CALLED_SUB_GR_SUBNAME = 'subname'
    # match only add end of line
    RE_CALLED_SUB = (_RE_CALLED_SUB_BASE + '$') % RE_CALLED_SUB_GR_SUBNAME  
    
    RE_SUB_GR_SUBNAME = 'subname'
    # match only add end of line
    RE_SUB = (__ONLY_WS_AT_BEGINNING + _RE_CALLED_SUB_BASE + '[:]$') % RE_SUB_GR_SUBNAME
    
    # base re for RE_C_METHOD and RE_CALLED_C_METHOD
    _RE_C_METHOD_BASE = '''
    _+              # _ 
    (?P<%s>\S+)     # CGPointMake_10002c4e0_1
    '''
    
    RE_C_METHOD_GR_NAME = 'c_method_name'
    # match only add end of line
    RE_C_METHOD = (__ONLY_WS_AT_BEGINNING + _RE_C_METHOD_BASE + '[:]$') % RE_C_METHOD_GR_NAME  
    
    RE_CALLED_C_METHOD_GR_NAME = 'c_method_name'
    # match only add end of line
    RE_CALLED_C_METHOD = (_RE_C_METHOD_BASE + '$') % RE_CALLED_C_METHOD_GR_NAME  
    
    SEARCH_NOP = 'nop'
    
    RE_MATCH_ENTRYPOINT = '\s*EntryPoint:\s*'
    
    RE_CLASS_PARENT_GR_CLASS = 'class'
    RE_CLASS_PARENT_GR_PARENT = 'parent'
    RE_CLASS_PARENT = r'''
 Class\s+             # Class
 (?P<%s>\w+)\s+       # Object1
 \(parent\s+class[:]\s+ # (parent class:  
 (?P<%s>\w+)          # SuperObject)
 \)
 ''' % (RE_CLASS_PARENT_GR_CLASS, RE_CLASS_PARENT_GR_PARENT) 

    RE_FORMAT_STRING_GR_STRING = 'format_string'
    RE_FORMAT_STRING_GR_OBJC_STRING = 'objc_string'
    # WARNING TODO: INSERT GR ARGUMENT!!
    
    # @"error: %s, code: %d"
    RE_FORMAT_STRING = r'''
 (?P<objc_string>@?)"                         # @" or "
 (?P<format_string>
  (?:
  [^%]                       # match all but %
  |                          # or
  %%)                        # %% (escaped %)
  *(?:%.*)                   # at least one (or more) % followed by alphanumeric or @ is needed 
  )
 "                          # "
'''
    RE_STRING_GR_STRING = 'string'
    RE_STRING = r'''
 @"                         # @"
 (?P<%s>.*)                 # defaults
 "                          # "
''' % (RE_STRING_GR_STRING)

    RE_C_STRING_GR_NAME = 'c_string'
    RE_C_STRING = '''
    "(?P<%s>.*)"
    ''' % RE_C_STRING_GR_NAME
    
    @staticmethod
    def method_implementation_is_static(re_meth_impl_gr_static_val):
        ''' Returns if the method is static '''
        return re_meth_impl_gr_static_val is not None
    
    @staticmethod
    def is_method_implementation(asmline):
        ''' Indicates if a line is a `CategoryClass` or method implementation.
        See `AsmRegEx.RE_CATEGORY` and `AsmRegEx.RE_METH_IMPL`.
        '''
        funcs = [AsmRegEx.compiled_vre(AsmRegEx.RE_CATEGORY), AsmRegEx.compiled_vre(AsmRegEx.RE_METH_IMPL)]
        return Util.get_fst_not_none(imap(lambda f: getattr(f, 'search')(asmline), funcs))
    
    @staticmethod
    def is_entrypoint(asmline):
        ''' Check if line is entry point in asm file (See `AsmRegEx.RE_MATCH_ENTRYPOINT`) '''
        return AsmRegEx.compiled_re(AsmRegEx.RE_MATCH_ENTRYPOINT).match(asmline) is not None
    
    
if __name__ == '__main__':
    print AsmRegEx.c_method_name('sub_1000045f0:')
    print AsmRegEx.c_method_name('_argTest_2df0')
