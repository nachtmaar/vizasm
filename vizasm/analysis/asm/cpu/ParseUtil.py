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

from itertools import imap

from vizasm.analysis.asm.cpu.AsmRegEx import AsmRegEx as regexp
from vizasm.model.asm.CString import CString
from vizasm.model.objc.arguments.CFormatString import CFormatString
from vizasm.model.objc.arguments.FormatString import FormatString
from vizasm.model.objc.arguments.Selector import Selector
from vizasm.model.objc.function.Function import Function
from vizasm.model.objc.function.MethodImplementation import MethodImplementation
from vizasm.model.objc.function.Sub import Sub
from vizasm.model.objc.object.nsobject.NSString import NSString
from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass
from vizasm.util import Util
from vizasm.util.Log import log


class ParseUtil(object):
    ''' 
    Base class for parsing an assembler line and turning it into the appropriate class. 
    
    Parameters
    ----------
    cpu: Cpu
    register_class: classobj
        the class to wrap around a register string
    '''
    def __init__(self, cpu, register_class):
        self._cpu = cpu
        self._register_class = register_class 

    def get_register_class(self):
        return self._register_class

    def set_register_class(self, value):
        self._register_class = value

    def get_cpu(self):
        return self._cpu

    def set_cpu(self, value):
        self._cpu = value

    register_class = property(get_register_class, set_register_class, None, "register_class(classobj) -- the class to wrap around a register string")
    cpu = property(get_cpu, set_cpu, None, "cpu(Cpu)")

#####################################################################################
# Implement these                                                                   #
#####################################################################################    
    
    def parse_objc_class_from_classref(self, asmline):
        raise NotImplementedError
    
    def parse_objc_class_from_framework_class(self, asmline):
        raise NotImplementedError
    
    def parse_ivar(self, asmline):
        raise NotImplementedError    
    
    def parse_var_assignment_without_ivar_ref_from_asmline(self, asmline):
        ''' Create a VarAssignment from asmline like e.g. "[ds:rax+rcx] (x86_64 example) " 
        
        Parameters
        ----------
        asmline: String
            
        Raises
        ------
        VarAssignmentResolveSelfrefRegisterException
            if the value cannot be resolved
        VarAssignmentResolveIvarRegisterException
            if the value cannot be resolved and `resolve_ivar_value` is true
        VarAssignmentIvarRegisterWrongTypeException
            if the type of the ivar_reg is not `IVar and `resolve_ivar_value` is true
                        
        Returns
        -------
        VarAssignment
            the VarAssignment without ivar_ref set (None if no VarAssignment)           
        '''        
        raise NotImplementedError
    
    def parse_var_assignment_with_ivar_ref_from_asmline(self, asmline):
        '''
        Create a VarAssignment from a line of assembler (like e.g. "[ds:rax+rcx]", x86_64 example)
        
        If the asmline has the form of "[ds:rdx+rsi], rax" the ivar_ref will be resolved.
        But the part after the comma can be left out.   
        
        Based on this method the `Cpu` keeps an instance variable cache. See `IVarRefLookup`.
        
        Parameters
        ----------
        asmline: string
        
        Raises
        ------
        VarAssignmentResolveSelfrefRegisterException
            if the value cannot be resolved
        VarAssignmentResolveIvarRegisterException
            if the value cannot be resolved
        VarAssignmentIvarRegisterWrongTypeException
            if the type of the ivar_reg is not `IVar`
        
        Returns
        -------
        VarAssignment
            the VarAssignment with ivar_ref set (if possible)
        None 
        '''        
        raise NotImplementedError
    
    def parse_stackvar(self, asmline):
        raise NotImplementedError
    
    def parse_imp_stub(self, asmline):
        raise NotImplementedError
    
    def parse_imp_got(self, asmline):
        raise NotImplementedError
    
    def parse_call_instruction(self, asmline):
        '''
        Check if the line is a call instruction like "call" (x86) or "blx" (arm)
        and return what is called as string. 
        '''
        raise NotImplementedError
    
    def parse_register(self, register):
        '''
        Parse a register.
        
        Parameters
        ----------
        register_type: type
            the type of the register to create. If non given, a string is used for the register representation.
        
        Returns
        --------
        register: `register_type`
            the register wrapped in `register_type` 
        None
            if regular expression did not classify as register  
        '''
        raise NotImplementedError

#####################################################################################
# Own implementation                                                                #
#####################################################################################

    @staticmethod
    def get_address_from_asmline(asmline):
        '''
        Get the hex address of the current line. This is the first number of the line.
        Return it as int or None if not available.
        '''
        split = asmline.split(' ')
        int_addr = None
        try:
            int_addr = int(split[0], 16)
        except ValueError:
            pass
        finally:
            return int_addr
        
    def parse_selector(self, asmline):
        ''' If annotated by Hopper, the `Selector` will be created from this.
        Otherwise implement this method yourself!
        '''
        return Selector.create_from_asm_line(asmline)
    
    def parse_format_string(self, asmline):
        ''' Create a `FormatString` from e.g. @"%s%d" '''
        string_match = regexp.compiled_vre(regexp.RE_FORMAT_STRING).search(asmline)
        if string_match is not None:
            name = string_match.group(regexp.RE_FORMAT_STRING_GR_STRING)
            is_objc_format_string = string_match.group(regexp.RE_FORMAT_STRING_GR_OBJC_STRING)
            if not is_objc_format_string:
                return CFormatString(CString(name))
            else:
                return FormatString(NSString(name))
        return None

    def parse_nsstring(self, asmline):
        ''' Create a `NSString` from e.g. @"defaults" '''
        string_match = regexp.compiled_vre(regexp.RE_STRING).search(asmline)
        if string_match is not None:
            name = string_match.group(regexp.RE_STRING_GR_STRING)
            return NSString(name)
        return None
    
    def parse_c_string(self, asmline):
        ''' Create a `CString` from a c string like e.g. "defaults" '''
        c_string_match = regexp.compiled_vre(regexp.RE_C_STRING).search(asmline)
        if c_string_match is not None:
            c_string = c_string_match.group(regexp.RE_C_STRING_GR_NAME)
            return CString(c_string)
        return None
    
    def parse_var_assignment(self, asmline):
        ''' 
        Wrapper for `parse_var_assignment_with_ivar_ref_from_asmline`.
        Ignores nop operations e.g. "nop        dword [ds:rax+0x0]"
        
        Create a VarAssignment from a line of assembler (like e.g. "[ds:rax+rcx]", x86_64 example
        
        If the asmline has the form of "[ds:rdx+rsi], rax" the ivar_ref will be resolved.
        But the part after the comma can be left out.   
        
        
        Based on this method (more general `parse_var_assignment_with_ivar_ref_from_asmline`), the `Cpu` keeps an instance variable cache. See `IVarRefLookup`.
        
        Parameters
        ----------
        asmline: string
        
        Raises
        ------
        VarAssignmentResolveSelfrefRegisterException
            if the value cannot be resolved
        VarAssignmentResolveIvarRegisterException
            if the value cannot be resolved
        VarAssignmentIvarRegisterWrongTypeException
            if the type of the ivar_reg is not `IVar`
        
        Returns
        -------
        VarAssignment
            the VarAssignment with ivar_ref set (if possible)
        None 
            if no VarAssignment                
        '''
        if asmline.find(regexp.SEARCH_NOP) == -1:
            return self.parse_var_assignment_with_ivar_ref_from_asmline(asmline)
        return None  
    
    def parse_objc_class(self, asmline):
        ''' Create ObjcClass from classref ([ds:objc_classref_Object1]) 
            or from frameworkclass e.g. ([ds:bind__OBJC_CLASS_$_NSUserDefaults]) 
            Returns None if no class matches.
        '''
        return self.get_fst_match(asmline, [self.parse_objc_class_from_framework_class, self.parse_objc_class_from_classref])
    
    def parse_stack_access(self, asmline):
        ''' Parse a stack access like e.g. "[sp, #0x8]" or "[r7, #0x8]" or "[sp] (arm).
        The latter should lead to an address of 0x0.
        
        Returns
        -------
        tuple<string, string>
            Return the stack pointer name as well as the stack address as hex string.
        '''        
        raise NotImplementedError
    
    def parse_string(self, asmline):
        '''
        Parse a string and return the appropriate string class. 
        
        Returns
        -------
        FormatString, NSString or string
        None
            if nothing matches
        '''
        return self.get_fst_match(asmline, [self.parse_format_string, self.parse_nsstring, self.parse_c_string])
        
    def parse_hex(self, asmline):
        ''' 
        Parse a line containing a hex value and convert it to an int. 
          
        Parameters
        ----------
        asmline: string
        
        Returns
        -------
        int: int
            hex value converted to int
        None
            if regular expression did not classify as hex value
        
        '''
        hex_match = regexp.compiled_vre(regexp.RE_HEX_VALUE).search(asmline)
        hex_value, res = None, None
        if hex_match is not None:
            hex_value = hex_match.group(regexp.RE_HEX_VALUE_GR_HEX_VALUE)
            try:
                res = int(hex_value, 16)
            except TypeError:
                log.warn('%s is no hex value!', hex_value)
        return res
    
    def parse_imp(self, asmline):
        '''
        Create a subclass of `Imp` like `ImpStub` or `ImpGot` from the asm line.
        '''
        return self.get_fst_match(asmline, [self.parse_imp_stub, self.parse_imp_got])
    
    @staticmethod
    def get_fst_match(asmline, functionlist):
        '''
        Get the first function (lazy) that matches on the given input argument.
         
        Parameters
        ----------
        asmline: string
            the argument to apply on the functions
        functionlist: list<functionrefs>
            the functions on which to apply the input argument 
        '''
        return Util.get_fst_not_none(imap(lambda x: x(asmline), functionlist))
    
    @staticmethod
    def get_fst_match_bool_list(asmline, functionlist):
        '''
        Get the first function (lazy) that matches on the given input argument.
         
        Parameters
        ----------
        asmline: string
            the argument to apply on the functions
        functionlist: list<functionrefs>
            the functions on which to apply the input argument 
        
        Returns
        -------
        tuple<list<bool>, object>
            Return a list where the function that matched has a True entry and the rest False.
            The second argument of the tuple is the return value of the function that matched.
        '''
        bool_list = [False] * len(functionlist)
        for idx, val in enumerate(imap(lambda x: x(asmline), functionlist)):
            if val is not None:
                bool_list[idx] = True
                return (bool_list, val)
        return (bool_list, None)
    
    @staticmethod
    def parse_any_method_implementation(asmline):
        ''' Parse (lazy) `parse_meth_impl`, `ParseUtil.parse_own_c_method_def`, `parse_c_method_name`, category,.
        
        Returns
        -------
        tuple<list<bool>, object>
            Return a list where the function that matched has a True entry and the rest False.
            The second argument of the tuple is the return value of the function that matched.
        '''
        # match category before parse_c_method_name because it will match also but should not
        functionlist = [ParseUtil.parse_meth_impl, ParseUtil.parse_own_c_method_def, ParseUtil.parse_c_method_name, MethodImplementation.create_from_asm_line]
        return ParseUtil.get_fst_match_bool_list(asmline, functionlist)
    
    @staticmethod
    def parse_meth_impl(asmline):
        ''' Parse a method implementation like e.g. "methImpl_AppDelegate_applicationDidFinishLaunching_". 
        
        For more details see `RE_METH_IMPL`.
        
        Returns
        -------
        MethodImplementation
        ''' 
        meth_impl_match = regexp.compiled_vre(regexp.RE_METH_IMPL).search(asmline)
        if meth_impl_match is not None:
            classname = meth_impl_match.group(regexp.RE_METH_IMPL_GR_CLASS)
            selectorname = meth_impl_match.group(regexp.RE_METH_IMPL_GR_SELECTOR)
            selector = Selector.selector_from_underscore_delimiter(selectorname)
            is_static = regexp.method_implementation_is_static(meth_impl_match.group(regexp.RE_METH_IMPL_GR_STATIC))
            if classname is not None:
                objc_class = ObjcClass(classname, is_static = is_static)
                return MethodImplementation(objc_class, [selector], is_static)
        return None
    
    @staticmethod
    def parse_c_method_name(asmline):
        '''
        Check if is `RE_SUB` or `RE_C_METHOD` and return the appropriate name if available.
        Otherwise None.
        
        Returns
        -------
        Function
            if `RE_C_METHOD` matches
        Sub
            if `RE_SUB` matches
        '''
        re_sub_match = regexp.compiled_vre(regexp.RE_SUB).search(asmline)
        if re_sub_match:
            return Sub(re_sub_match.group(regexp.RE_SUB_GR_SUBNAME))
        re_c_method_match = regexp.compiled_vre(regexp.RE_C_METHOD).search(asmline)
        if re_c_method_match:
            return Function(re_c_method_match.group(regexp.RE_C_METHOD_GR_NAME))
        return None
    
    @staticmethod
    def parse_own_c_method_def(asmline):
        re_own_c_method_def_match = regexp.compiled_vre(regexp.RE_OWN_C_METHOD_DEF).search(asmline)
        if re_own_c_method_def_match:
            func_name = re_own_c_method_def_match.group(regexp.RE_OWN_C_METHOD_BASE_GR_NAME)
            func_args_str = re_own_c_method_def_match.group(regexp.RE_OWN_C_METHOD_BASE_GR_ARGS)
            if func_args_str is not None:
                func_args_list = re_own_c_method_def_match.group(regexp.RE_OWN_C_METHOD_BASE_GR_ARGS).split(' ,')
            else:
                func_args_list = []
            return Function(func_name, func_args_list)
        return None
    
    @staticmethod
    def parse_own_c_method_called(asmline):
        re_own_c_method_call_match = regexp.compiled_vre(regexp.RE_OWN_C_METHOD_CALLED).search(asmline)
        if re_own_c_method_call_match:
            func_name = re_own_c_method_call_match.group(regexp.RE_OWN_C_METHOD_BASE_GR_NAME)
            func_args_str = re_own_c_method_call_match.group(regexp.RE_OWN_C_METHOD_BASE_GR_ARGS)
            if func_args_str is not None:
                func_args_list = re_own_c_method_call_match.group(regexp.RE_OWN_C_METHOD_BASE_GR_ARGS).split(', ')
            else:
                func_args_list = []                
            return Function(func_name, func_args_list)
        return None
    
    @staticmethod
    def parse_called_method_name(asmline):
        '''
        Check if `asmline` is a c method being called.
        Check for `RE_CALLED_SUB` and `RE_CALLED_C_METHOD` and return the appropriate name if available.
        Otherwise None.
        
        Returns
        -------
        Function
            if `RE_C_METHOD` matches
        Sub
            if `RE_SUB` matches        
        '''
        re_sub_match = regexp.compiled_vre(regexp.RE_CALLED_SUB).search(asmline)
        if re_sub_match:
            return Sub(re_sub_match.group(regexp.RE_CALLED_SUB_GR_SUBNAME))
        re_c_method_match = regexp.compiled_vre(regexp.RE_CALLED_C_METHOD).search(asmline)
        if re_c_method_match:
            return Function(re_c_method_match.group(regexp.RE_CALLED_C_METHOD_GR_NAME))
        return None
    
    @staticmethod
    def parse_category(asmline):
        '''
        Parse a category method implementation.
        
        Returns
        -------
        MethodImplementation
        '''
        return MethodImplementation.create_from_asm_line(asmline)
    
if __name__ == '__main__':
    pu = ParseUtil(None, None)
    print repr(pu.parse_string('"SELECT username FROM users where uid = ?"'))
    print pu.parse_meth_impl(' methImpl_AppDelegate_applicationDidFinishLaunching_')
    print pu.parse_meth_impl(' methImpl_AppDelegate__cxx_destruct:')
    print pu.parse_any_method_implementation(' methImpl_AppDelegate__cxx_destruct')
    print pu.parse_any_method_implementation('                                            methImpl_Networking_cookies:')
    print pu.parse_any_method_implementation('+[NSURLRequest(AnyHttpsCert) allowsAnyHTTPSCertificateForHost:]_100001c70:')
    print 'this should not match: %s' % pu.parse_meth_impl('lea        rdi, qword [ds:cfstring________method_not_converted_to_OpenGL_ES_2_0] ; @"%@: %@ method not converted to OpenGL ES 2.')
    print 'sub: %s' % str(pu.parse_any_method_implementation('sub_e020:'))
    print 'c method: %s' % str(pu.parse_any_method_implementation('_main_1000016a0:'))
    print 'category: %s' % str(pu.parse_any_method_implementation('+[NSURLRequest(AnyHttpsCert) allowsAnyHTTPSCertificateForHost:]_100002120:'))
    print pu.parse_format_string('0000000100002a19 488D3D70310000                  lea        rdi, qword [ds:cfstring_error___s__code___d] ; @"error: %s, code: %d"')
    print 'format string: %s' % repr(pu.parse_string('"%d%d%d%d%d%d%d"'))
    
