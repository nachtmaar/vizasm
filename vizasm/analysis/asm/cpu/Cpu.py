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

import sys

from vizasm.analysis.asm.cpu.AsmRegEx import AsmRegEx
from vizasm.analysis.asm.cpu.CRuntime import CRuntime
from vizasm.analysis.asm.cpu.CallingConventionsInterface import \
    CallingConventionsInterface
from vizasm.analysis.asm.cpu.ParseUtil import ParseUtil
from vizasm.analysis.asm.cpu.Resetable import Resetable
from vizasm.analysis.asm.cpu.exceptions.CpuCouldNotGetDestination import \
    CpuCouldNotGetDestination
from vizasm.analysis.asm.cpu.exceptions.CpuCouldNotGetSelfref import \
    CpuCouldNotGetSelfref
from vizasm.analysis.asm.cpu.exceptions.CpuCouldNotReadNSLogException import \
    CpuCouldNotReadLogFuncException
from vizasm.analysis.asm.cpu.exceptions.CpuException import CpuException
from vizasm.analysis.asm.cpu.memory.Memory import Memory
from vizasm.analysis.asm.cpu.objcruntime.ObjectiveCRuntime import \
    ObjectiveCRuntime
from vizasm.hopper.hopannotate import hopanno
from vizasm.model.asm.imp.Imp import Imp
from vizasm.model.asm.imp.ImpStub import ImpStub
from vizasm.model.asm.var_assignment.VarAssignment import VarAssignment
from vizasm.model.asm.var_assignment.VarAssignmentIvarRegisterWrongTypeException import \
    VarAssignmentIvarRegisterWrongTypeException
from vizasm.model.objc.arguments.ArgumentsException import ArgumentsException
from vizasm.model.objc.arguments.FormatString import \
    FormatStringOverLoadedException, FormatStringUnderLoadedException
from vizasm.model.objc.arguments.Selector import Selector
from vizasm.model.objc.function.Function import Function
from vizasm.model.objc.methodcall.MethodCall import MethodCall
from vizasm.model.objc.object.nsobject.NSString import NSString
from vizasm.util.Log import log, clilog
from vizasm.model.objc.arguments.Arguments import Arguments
from vizasm.Settings import setting_for_key, SETTINGS_C_FUNC_HEURISTIC
from vizasm.model import ModelUtil
from vizasm.model.asm.CString import CString
from vizasm.model.asm.var_assignment.VarAssignmentResolveRegisterException import VarAssignmentResolveRegisterException

class Cpu(object, CRuntime, CallingConventionsInterface, Resetable): 
    '''
    The `Cpu` is the heart of VizAsm.
    
    It reads and interprets the asm file (use `read_line`).
    and keeps track of the `StackFrame` and the `Register`s.
    
    It stores the method calls that have been made in the `MethodCall` 
    (stores the calls for a single method implementation).
    
    Every time you read a new method implementation, you should `reset` the `Cpu`.
     
    Parameters
    ----------
    _memory: Memory
        the memory of the cpu
    _objc_runtime: ObjectiveCRuntime, optional (default is ObjectiveCRuntime)
        the objective-c runtime
    __assignment_matching_system: AssignmentMatchingSystem
        the system to read assignments
    _parse_util: ParseUtil
        utility for parsing the asm file
    _register_class: classobj
        subclass of Register (only the reference!). 
        this class reference is used to create the correct register subclass depending on the cpu architecture.
    _linenumber: int
        the current line number in the asm file. Given as parameter in `read_line`. 
    __address: int
        the address of the current asm line
    _method: FunctionInterface
        the method which is currently being analyzed
    __method_call: MethodCall
        This is the actual output of the `Cpu`. It stores the messages that have been read. 
    c_func_heuristic: bool
        if enabled use heuristic to determine arguments for c function calls
        
    Notes
    -----
    Subclasses need to implement `CallingConventionsInterface` as well as:
        create_and_store_method_selector_arguments
        ignore_hex_addr_call
    '''
    
#####################################################################################
# Resetable                                                                         #
#####################################################################################    

    def reset(self):
        ''' Reset the `Cpu` and make it ready to analyze the next method implementation '''
        self.memory.reset()
        self.objc_runtime.reset()
        self.__init_resetable_stuff()
        
#####################################################################################
# Implementation                                                                    #
#####################################################################################
    
    def __init__(self, assignment_matching_system, parse_util, _register_class, superclass_dict = None, objc_runtime = None):
        self.__assignment_matching_system = assignment_matching_system
        self._parse_util = parse_util
        self._register_class = _register_class
        
        self._memory = Memory(self)
        # use standard objective-c runtime if nothing else given
        if objc_runtime is None:
            objc_runtime = ObjectiveCRuntime(self, superclass_dict)
        self._objc_runtime = objc_runtime
        
        self._c_func_heuristic = setting_for_key(SETTINGS_C_FUNC_HEURISTIC)
        self.__init_resetable_stuff()

    def __init_resetable_stuff(self):
        ''' Init stuff that needs to be initiliazed/resetted for 
        every method implementation that will be read '''
        self.__method_call = MethodCall()
        self._line_number = None
        self.__address = None
        self._method = None
    
    def __str__(self):
        return '%s: %s\n%s' % (self.__class__.__name__, self.memory, self.objc_runtime)
    
    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, repr(self.memory), repr(self.objc_runtime))
    
#####################################################################################
# Getter and Setter                                                                 #
#####################################################################################

    def get_c_func_heuristic(self):
        return self._c_func_heuristic

    def set_c_func_heuristic(self, value):
        self._c_func_heuristic = value
        
    def get_objc_runtime(self):
        return self._objc_runtime

    def set_objc_runtime(self, value):
        self._objc_runtime = value
        
    def get_memory(self):
        return self._memory

    def set_memory(self, value):
        self._memory = value
        
    def get_parse_util(self):
        return self._parse_util

    def set_parse_util(self, value):
        self._parse_util = value

    def get_method(self):
        return self._method

    def set_method(self, value):
        self._method = value
        
    def get_line_number(self):
        return self._line_number

    def set_line_number(self, value):
        self._line_number = value
        
    def get_address(self):
        return self.__address

    def set_address(self, value):
        self.__address = value

    def get_assignment_matching_system(self):
        return self.__assignment_matching_system
    
    def set_assignment_matching_system(self, value):
        self.__assignment_matching_system = value
        
    def get_register_class(self):
        return self._register_class

    def set_register_class(self, value):
        self._register_class = value
    
    def get_method_call(self):
        return self.__method_call

    def set_method_call(self, value):
        self.__method_call = value
        
    def set_method_selector_reg_value(self, value):
        ''' Set the value for the register where the selector of the current method is stored. '''
        if not self.fetches_all_arguments_from_stack():
            self.memory.registers.set_value_for_register(self.selector_register(), value)
    
    def set_selfref_reg_value(self, value):
        ''' Set the value for the register where the self reference of the current method is stored '''
        if not self.fetches_all_arguments_from_stack():
            self.memory.registers.set_value_for_register(self.destination_register(), value)
    
    def get_method_selector_reg_value(self):
        ''' Get the value for the register where the selector of the current method is stored.
        If the argument is on stack, do not pop it. '''
        if self.fetches_all_arguments_from_stack():
            return self.stack.get_from_idx(1)
        return self.memory.registers.get_value_for_register(self.selector_register())
        
    def get_selfref_reg_value(self):
        ''' Get the value for the register where the self reference of the current method is stored.
        If the argument is on stack, do not pop it. '''
        if self.fetches_all_arguments_from_stack():
            return self.stack.get_from_idx(0)
        return self.memory.registers.get_value_for_register(self.destination_register())
    
    memory = property(get_memory, set_memory, None, "memory(Memory) -- the memory of the cpu")
    objc_runtime = property(get_objc_runtime, set_objc_runtime, None, "_objc_runtime(ObjectiveCRuntime) -- the objective-c runtime")
    parse_util = property(get_parse_util, set_parse_util, None, "_parse_util(ParseUtil) -- utility for parsing the asm file")
    assignment_matching_system = property(get_assignment_matching_system, set_assignment_matching_system, None, "__assignment_matching_system(AssignmentMatchingSystem) -- the system to read assignments")
    line_number = property(get_line_number, set_line_number, None, "the current line number in the asm file. Given as parameter in `read_line`.")
    address = property(get_address, set_address, None, "__address(int) -- the address of the current asm line")
    register_class = property(get_register_class, set_register_class, None, """_register_clas(classobj) -- 
    subclass of Register (only the reference!). 
    This class reference is used to create the correct register subclass depending on the cpu architecture""") 
    method_call = property(get_method_call, set_method_call, None, "__method_call(MethodCall) -- this is the actual output of the `Cpu`. It stores the messages that have been read.")
    method = property(get_method, set_method, None, "_method(FunctionInterface) -- the method which is currently being analyzed")
    c_func_heuristic = property(get_c_func_heuristic, set_c_func_heuristic, None, "c_func_heuristic(bool) -- if enabled use heuristic to determine arguments for c function calls")

#####################################################################################
# Subclasses need to overwrite these methods                                        #
#####################################################################################
    def pointer_size(self):
        ''' Return the pointer size in bytes '''
        raise NotImplementedError
    
    def ignore_hex_addr_call(self):
        ''' Return True if you want to ignore calls to hex addresses '''
        return False
    
#####################################################################################
# Public Interface                                                                  #
#####################################################################################

    def is_32_bits(self):
        ''' Check if is 32 bit `Cpu` '''
        return self.pointer_size() == 4
    
    def is_64_bits(self):
        ''' Check if is 64 bit `Cpu` '''
        return self.pointer_size() == 8
    
    def read_line(self, asmline, linenr = None):
        ''' 
        Read a line of the asm file and process the information
        to keep track of the registers and stack.
        
        Parameters
        ----------
        asmline: string
            a line of assembler
        linenr: int, optional
            the current line number in the file. 
            If not given, it will not be used in the output.
        
        Raises
        ------
        CpuException
            if any underlying exception has been raised 
         '''
        log.debug('reading line: %s', asmline)
        if linenr is not None:
            self.line_number = linenr
        self.address = ParseUtil.get_address_from_asmline(asmline)
        try:
            self._read_basic_block(asmline)
            self._read_meth_impl(asmline)
            self._read_assignment(asmline)
            self._read_call_line(asmline)
        except (ArgumentsException, VarAssignmentIvarRegisterWrongTypeException) as e:
            raise CpuException(self, e), None, sys.exc_info()[2]
    
    def get_current_destination(self, objc_msgSend_stret = False):
        ''' Return the current destination. 
    
        Parameters
        ----------
        objc_msgSend_stret: bool, optional (default is False)
            indicate an objc_msgSend_stret
            
        Raises
        ----------
        CpuCouldNotGetDestination
            raised if the value of the destination could not be detected
            
        Returns
        -------
        destination
        ''' 
        dest_reg = self.destination_register()
        if objc_msgSend_stret:
            dest_reg = self.next_reg_for_spret(dest_reg)
        dest = self.memory.get_argument(dest_reg)
        if dest is not None:
            return dest
        raise CpuCouldNotGetDestination(self)
    
#####################################################################################
# Private Interface                                                                 #
#####################################################################################
                    
    def _read_basic_block(self, asmline):
        ''' 
        Read a Basic Block like " ; Basic Block Input Regs: rax rdx rsi rdi -  Killed Regs: rax rcx rdx rsp rbp rsi rdi r8"
        and kill the specified registers.
        '''
        basic_block_match = AsmRegEx.compiled_vre(AsmRegEx.RE_BASIC_BLOCK).search(asmline)
        if basic_block_match is not None:
            killed_regs = basic_block_match.group(AsmRegEx.RE_BASIC_BLOCK_KILLED_REGS)
            killed_regs = killed_regs.split(' ')
            self.memory.registers.delete_elements(killed_regs)
    
    def _read_meth_impl(self, asmline):
        ''' Read a line like e.g. "methImpl_AppDelegate_applicationDidFinishLaunching_"
        and detect the current class (AppDelegate) as well as the current method (applicationDidFinishLaunching_)
        
        If the `Cpu` does not fetch all of its arguments from stack, 
        self and _cmd will be set to the `Register`s defined by `CallingConventionsInterface`.
        
        Otherwise implement `store_self_cmd_for_stack_fetching_cpu` in your `Cpu`.
        
        Raises
        ------
        CpuCouldNotGetSelfref
            raised if the self reference could not be detected
        SelectorOverloadedException
            raised if the selector has more arguments than it needs
        SelectorUnderloadedException
            raised if the selector has less arguments than it needs 
            '''
        method_implementation, match = self.parse_util.parse_any_method_implementation(asmline)
        is_meth_impl, is_own_c_method_def, is_c_method, is_category = method_implementation
        
        method_impl = None
        if any([is_meth_impl, is_category]):
            method_impl = match
            selector = match.fst_selector()
            objc_class = match.msg_receiver

            if not self.fetches_all_arguments_from_stack():
                selfref_reg = self.destination_register()
                if selfref_reg is not None:
                    # store class for self reference
                    self.set_selfref_reg_value(objc_class)
                else:
                    raise CpuCouldNotGetSelfref(self, selfref_reg, '%s.%s' % (objc_class, selector))
            else:
                # set self and _cmd for cpu fetching its args from stack
                self.objc_runtime.store_self_cmd_for_stack_fetching_cpu(objc_class, selector)
                
            self.objc_runtime.create_and_store_method_selector_arguments(selector)
            # set method to use it in _try_log_reading_meth_impl
            self.method = method_impl

            # log method
            self._try_log_reading_meth_impl(selector)
            
            self.set_method_selector_reg_value(selector)
            
        elif is_c_method or is_own_c_method_def:
            log.debug('reading method: %s', match)
            method_impl = match
            self.create_and_store_c_func_arguments(method_impl)
        
        if any(method_implementation):
            clilog.info('reading method: %s', method_impl)
            # set method and sender for `MethodCall`
            self.method = method_impl
            self.method_call.sender = method_impl
    
    def _try_log_reading_meth_impl(self, method_selector):
        ''' Log the current meth_impl if selector has been filled with all its arguments ''' 
        if self.fetches_all_arguments_from_stack():
            log.info('reading meth_impl: %s', self.method)
        else:
            if not method_selector.needs_more_arguments():
                log.info('reading meth_impl: [(%s)%s (%s)%s]', self.destination_register(), self.get_selfref_reg_value(), self.selector_register(), method_selector)

    def _read_assignment(self, asmline):
        ''' Read a line of assembler code containing an assignment
        and let the `AssignmentMatchingSystem` process it.
        
        This includes stack operations.
        The assignments being made are stored in the appropriate place (stack or register)
        
        Moreover this method reads a `VarAssignment` and keeps track of the instance variable cache
        as well as setting the superclass if available.
        ''' 
        try:
            var_assign = self.parse_util.parse_var_assignment(asmline)
            if var_assign is not None:
                    self._process_var_assignment(var_assign)
            # CHECK IF ALSO CORRECT OR X86_64
            # consider "str        r0, [r4, r5]" (arm), needed to not set r5 = value(r0)
            else:
                self._process_assignment(asmline)
        except VarAssignmentResolveRegisterException as e:
            log.exception(e)
            
    def _process_var_assignment(self, var_assign):
        '''
        Process the `VarAssignment` and keep track of the instance variable cache
        as well as setting the superclass if available.
        
        Parameters
        ----------
        var_assign: VarAssignment
        '''
        if var_assign is not None:
            # set entry in IVarLookup if VarAssignment contains IVar
            ivar = var_assign.get_ivar_value()
            ivar_ref = ivar.get_ivar_ref()
    
            self.objc_runtime.set_superclass(ivar)
    
            if ivar is not None:
                if ivar.create_ivar_lookup_entry(self.objc_runtime.ivar_lookup):
                    msg = '%s -> %s' % (ivar.get_ivar_class(), ivar_ref)
                    log.debug(msg)
                    hopanno.annotate_other_assignment('added ivar lookup entry: ' + msg, self.address)
                    hopanno.annotate_assignment_method_head(msg)
                
    def _process_assignment(self, asmline):
        '''
        If the `Selector` of the method still needs arguments,  try to fill the remaining ones from stack.

        Parameters
        ----------
        asmline: string
        '''
        asm = self.get_assignment_matching_system()
        asm.read_assignment(asmline)
        
        robject = asm.get_robject() 
        # keep track of StackFrame
        if asm.is_stack_push:
            asm.process_stack_push()
        else:
            # keep track of assignments
            key = asm.get_lobject()
            if None not in (key, robject): 
                self.memory.registers.set_value_for_register(key, robject)      
    
    def _read_call_line(self, asmline):
        ''' Read a call line like e.g. "call qword [ds:objc_msg_alloc] ; @selector(alloc)" 
        ,split to what is called and interpret the called stuff.
        '''
        called = self.parse_util.parse_call_instruction(asmline)
        if called is not None:
            if self.c_func_heuristic:
                log.debug('args since last call: \n%s', ', '.join(str(x) for x in self.assignment_matching_system.get_usage_since_last_call()))
            self._read_called(asmline, called)
            self.assignment_matching_system.clear_usage_since_last_call()
            
    def _read_called(self, asmline, called):
        ''' Read a called line like e.g. "qword [ds:objc_msg_alloc] ; @selector(alloc)"
        and hand it on to the appropriate read method.
        
        Parameters
        ----------
        asmline: string
        called: ImpStub, Selector or string
        
        Raises
        ------
        IvarRefWrongTypeException
            if the ivar_ref has the wrong type
        CpuException
            if the value of the destination register could not be resolved
        CpuCouldNotReadLogFuncException
            if the NSLog could not be read
        CpuCouldNotReadMsgSendEception
            if the objc_msgsend() could not be read
        '''
        # called does not have to be a string due to the fact that read_register()
        # will recall this method with register resolved and passed as called
        imp = selector = destination = None
        if isinstance(called, str):
            imp = self.parse_util.parse_imp(called)
            # called can be e.g. _foo or sub_foo
            if not imp:
                called_method = self.parse_util.parse_called_method_name(called) 
                if called_method is not None:
                    called = called_method
                else:
                    if self.ignore_hex_addr_call() and self.parse_util.parse_hex(called):
                        return
                    
        # called can be Selector or Imp
        else:
            if isinstance(called, Imp):
                imp = called
            elif isinstance(called, Selector):
                selector = called
        try:
            # only pop from stack if really needed for a MsgSend
            if imp is not None and imp.is_any_msg_send() and self.fetches_all_arguments_from_stack() or not self.fetches_all_arguments_from_stack():
                is_msg_send_stret = False
                if imp is not None:
                    is_msg_send_stret = imp.is_any_msg_send_stret()
                destination = self.get_current_destination(is_msg_send_stret)
                                                           
            return_register = self.return_register()
            
            # if selector is not None, it's already resolved
            if selector is None:
                selector = self.parse_util.parse_selector(asmline)
            
            register = None
            if isinstance(called, str):
            # same as above, called can be anything else than a string
                register = self.parse_util.parse_register(called)
            
            log.debug('destination is %s', destination)
            
            # destination is VarAssignment
            if isinstance(destination, VarAssignment):
                # get ivar value from VarAssignment
                destination = destination.get_ivar_value()
                  
            if imp is not None:
                msgSend = self.objc_runtime.read_msg_send(imp, destination)
                if msgSend is None:
                    if self.objc_runtime.read_return_important_objc_call(imp, destination, return_register):
                        return
                    if self._read_formatstring_log(imp):
                        return
                    else:
                        self._read_remaining_stub(imp)
            else:
                if self._read_c_func(called):
                    return
                else:
                    self._read_register(register, asmline)
                if not self.objc_runtime.read_selector(selector, destination):
                    # TODO: HOW TO HANDLE (fp)([NSURLRequest class], selx, YES, host); ???
                    # called can be something else due to recalling of `_read_register`
                    if isinstance(called, str):
                        own_c_method_call = ParseUtil.parse_own_c_method_called(called)
                        if own_c_method_call is not None:
                            self._read_own_c_func_call(own_c_method_call)

        except CpuCouldNotGetDestination as e:
            raise CpuException(self, e), None, sys.exc_info()[2]

    def _read_formatstring_log(self, imp):
        ''' Read an NSLog `ImpStub` and add it to the `MethodCall. 
        
        Parameters
        ----------
        imp: Imp
        
        Raises
        ------
        CpuCouldNotReadLogFuncException
            if the NSLog could not be read 
            
        Returns
        -------
        is NSLog
        '''
        if isinstance(imp, ImpStub):
            is_formatstring_log = imp.is_format_string_log()
            log_func_name = imp.imp
            formatstring_log = None
            if is_formatstring_log:
                format_string_args = []
                # check if fst arg is `FormatString` and resolve the other arguments
                try:
                    formatstring_log_string = self.get_current_destination(objc_msgSend_stret = False)
                    format_string_args = [formatstring_log_string]
                    if isinstance(formatstring_log_string, str):
                        formatstring_log_string = NSString(formatstring_log_string)
                    elif isinstance(formatstring_log_string, Arguments):
                        try:
                            formatstring_log_string.fill_from_cpu(self)
                        except (FormatStringOverLoadedException, FormatStringUnderLoadedException) as e:
                            log.exception(e)
                    # fst arg is no format string -> use heuristic for number of arguments
                    elif not isinstance(formatstring_log_string, (NSString, CString)):
                        # use heuristic from `AssignmentMatchingSystem` to determine the number of arguments for the function
                        format_string_args = self.get_memory().get_arguments_from_asm_heuristic()
                        # fill args that can fill themselves from cpu
                        for arg in format_string_args:
                            if isinstance(arg, Arguments):
                                arg.fill_from_cpu(self)
                    formatstring_log = Function(log_func_name, format_string_args) 
                    self._store_function(formatstring_log)
                except CpuCouldNotGetDestination as e:
                    raise CpuCouldNotReadLogFuncException(self, log_func_name, '%s\n%s' % (formatstring_log, e)), None, sys.exc_info()[2] 
            return is_formatstring_log
        return False
    
    def _read_c_func(self, c_func):
        ''' Read a c function or subroutine like e.g. "sub_10013ec80" '''
        if ModelUtil.is_c_function(c_func):
            # use heuristic from `AssignmentMatchingSystem` to determine the number of arguments for the function
            arguments = self.get_memory().get_arguments_from_asm_heuristic()
            c_func.set_func_arguments(arguments)
            self._store_function(c_func)
            return True
        return False
        
    def _read_remaining_stub(self, imp_stub):
        ''' Turn remaining `ImpStub`s into a Function and store it in the `MethodCall` '''
        imp_stub_name = imp_stub.get_imp()
        function = Function(imp_stub_name)
        # use heuristic from `AssignmentMatchingSystem` to determine the number of arguments for the function
        arguments = self.get_memory().get_arguments_from_asm_heuristic()
        function.set_func_arguments(arguments)
        self._store_function(function)
        
    def _read_register(self, register, asmline):
        ''' Called is register. Resolve the register value and try again reading the call line. 
            E.g. a `Selector` could be stored in the `Register`.
        '''
        if register is not None:
            register = self.memory.registers.resolve_current_register_value(register)
            self._read_called(asmline, register)
    
    def _read_own_c_func_call(self, c_function):
        ''' Read a function call to a c function which is written in the application (not any library).
        E.g. "call       __Z9cFunctioniii_1000027d0    ; cFunction(int, int, int)" 
        '''
        cnt_args = len(c_function)
        args = self.get_memory().get_arguments(cnt_args, self.arguments_registers(), try_only = False)
        c_function.set_func_arguments(args)
        self._store_function(c_function)
                                
    def _store_function(self, function):    
        '''
        Store the function in the `return_register` of the `Cpu` and add it to the `MethodCall`.
         
        Parameters
        ----------
        function: FunctionInterface
        '''
        if function is not None:
            self.memory.set_return_register_value(function)
            self.get_method_call().add_methodcall(function, self.line_number, self.address)
        
