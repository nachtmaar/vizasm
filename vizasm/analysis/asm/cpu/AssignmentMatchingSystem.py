'''
VizAsm

Created on 24.08.2013

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
from vizasm.util.Log import log
from vizasm.analysis.asm.cpu.Resetable import Resetable
from vizasm.Settings import setting_for_key, SETTINGS_C_FUNC_HEURISTIC

class AssignmentMatchingSystem(object, Resetable):
    '''
    The AssignmentMatchingSystem is the base class for a system that reads a line of assembler code in which an assignment is being made.
    
    The system has to parse the values with the help of the `parse_util` and wrap them into the appropriate class.

    The system also has to recognize stack operations (push and pop).
     
    The left and right object of the assignment can be accessed via `lobject` and `robject` but only if an assignment has been made.
    
    If a stack push has been read, the stack can be adjusted with `process_stack_push`.
    Reading a stack fetch will store the fetched argument in `robject`.
    
    If you want to use an estimation for the number of arguments a function takes (not objective-c function)
    you have to keep track of register and stack usage via `reg_usage_since_last_call` and `stack_usage_since_last_call.
    
    Parameters
    ----------
    _cpu: Cpu
    __parse_util: ParseUtil
        the `ParseUtil` to use for splitting and parsing the line
    _lobject: object
        the left value of the assignment matched to a type
    _robject: object
        the right value of the assignment matched to a type
    _is_stack_fetch: bool (default is False)
        indicates if the assignment is a fetch from the stack
        e.g. "mov        rax, qword [ss:rbp-0x70+arg_8]"
    _is_stack_push: bool (default is False)
        indicates if the assignment is a stack push operation. x86_64 example: "mov dword [ss:rsp], 0x7".
    _stack_push_objects: list<object> (default is [])
        the objects being pushed onto the stack
    _stack_address: int (default is None)
        the stack address
    `: set<Register>
        use to store the registers that have been used 
        to store any value since the last call statement
    _stack_usage_since_last_call: set<object>
        use to store the stack arguments that have been used to 
        store any value since the last call statement
    c_func_heuristic: bool
        if enabled use heuristic to determine arguments for c function calls
    '''
    def __init__(self, cpu, parse_util):
        self._cpu = cpu
        self._parse_util = parse_util 
        self.__init_defaults()
        self.clear_usage_since_last_call()
        self._c_func_heuristic = setting_for_key(SETTINGS_C_FUNC_HEURISTIC)

    def __init_defaults(self):
        ''' Set all objects that are affected by reading an assignment to their defaults '''
        self._lobject, self._robject = None, None
        self._is_stack_fetch = False
        self._is_stack_push = False
        self._stack_push_objects = []
        self._stack_address = None

    def get_c_func_heuristic(self):
        return self.__c_func_heuristic

    def set_c_func_heuristic(self, value):
        self.__c_func_heuristic = value

    def get_stack_args_since_last_call(self):
        return self._stack_usage_since_last_call

    def set_stack_args_since_last_call(self, value):
        self._stack_usage_since_last_call = value

    def get_reg_args_since_last_call(self):
        return self._reg_usage_since_last_call

    def set_reg_args_since_last_call(self, value):
        self._reg_usage_since_last_call = value

    def clear_usage_since_last_call(self):
        ''' The `Cpu` uses this after a new call has been read 
        to reset the register and stack usage since the last call '''
        self._reg_usage_since_last_call = set()
        self._stack_usage_since_last_call = set()
        
    def get_usage_since_last_call(self):
        ''' Get the registers and stack usage since the last call.
        
        Returns
        -------
        set<object>
        '''
        return self.stack_usage_since_last_call.union(self.reg_usage_since_last_call)
        
    def get_stack_address(self):
        return self._stack_address

    def set_stack_address(self, value):
        ''' Set the stack address.
        If address is given as string version of the hex address it will be converted to int '''
        if isinstance(value, str):
            value = int(value, 16)
        self._stack_address = value

    def get_stack_push_objects(self):
        return self._stack_push_objects

    def set_stack_push_objects(self, value):
        self._stack_push_objects = value
        
    def get_is_stack_push(self):
        return self._is_stack_push

    def set_is_stack_push(self, value):
        self._is_stack_push = value

    def set_is_stack_fetch(self, value):
        self._is_stack_fetch = value

    def get_parse_util(self):
        return self._parse_util

    def set_parse_util(self, value):
        self._parse_util = value

    def get_is_stack_fetch(self):
        return self._is_stack_fetch

    def get_lobject(self):
        return self._lobject
    
    def set_lobject(self, value):
        self._lobject = value 

    def get_robject(self):
        return self._robject
    
    def set_robject(self, value):
        self._robject = value 
        
    def get_cpu(self):
        return self._cpu

    def set_cpu(self, value):
        self._cpu = value
        
    cpu = property(get_cpu, set_cpu, None, "__cpu(Cpu)")
    parse_util = property(get_parse_util, set_parse_util, None, "__parse_util(ParseUtil) -- the `ParseUtil` to use for splitting and parsing the line")
    lobject = property(get_lobject, set_lobject, "_lobject(object) -- the left value of the assignment matched to a type")
    robject = property(get_robject, set_robject, None, "_robject(object) -- the right value of the assignment matched to a type")
    is_stack_fetch = property(get_is_stack_fetch, set_is_stack_fetch, None, '_is_stack_fetch(bool) -- indicates if the assignment is a fetch from the stack e.g. "mov        rax, qword [ss:rbp-0x70+arg_8]"')
    is_stack_push = property(get_is_stack_push, set_is_stack_push, None, '_is_stack_push: bool (default is False) -- indicates if the assignment is a stack push operation. x86_64 example: "mov dword [ss:rsp], 0x7".')
    stack_push_objects = property(get_stack_push_objects, set_stack_push_objects, None, "_stack_push_objects: list<object> (default is []) -- the objects being pushed onto the stack")
    stack_address = property(get_stack_address, set_stack_address, None, "_stack_address: int (default is None) -- the stack address")
    stack_usage_since_last_call = property(get_stack_args_since_last_call, set_stack_args_since_last_call, None, "stack_usage_since_last_call(set<object>) -- use to store the stack arguments that have been used to store any value since the last call statement")
    reg_usage_since_last_call = property(get_reg_args_since_last_call, set_reg_args_since_last_call, None, "reg_usage_since_last_call(set<Register>) -- use to store the registers that have been used to store any value since the last call statement")
    c_func_heuristic = property(get_c_func_heuristic, set_c_func_heuristic, None, "c_func_heuristic(bool) -- if enabled use heuristic to determine arguments for c function calls")
    
    def add_reg_arg_since_last_call(self, reg, robject):
        '''
        Add a `Register` to `reg_usage_since_last_call` if the 
        register is specified as an register holding method arguments.
        
        See `CallingConventionsInterface.arguments_registers`.
        
        Parameters
        ----------
        reg: Register
        '''
        cpu = self.get_cpu()
        if cpu.c_func_heuristic:
            if not cpu.fetches_all_arguments_from_stack():
                if isinstance(reg, Register):
                    exclude_regs = cpu.exclude_argument_regs()
                    # check that reg is valid argument register
                    if not (reg in exclude_regs or robject in exclude_regs) and reg in cpu.arguments_registers(): 
                        self.reg_usage_since_last_call.add(reg)
            
    def read_assignment(self, asmline):
        '''
        Read an assignment and try to split it.
        
        Call this first to reset the `AssignmentMatchingSystem` 
        or do it at your own!
        
        Parameters
        ----------
        asmline : string
            line of assembler
        '''
        self.reset()
    
    def number_of_arguments_since_last_call(self):
        ''' Get the number of arguments that have been seen since the last call.
        For the arguments going over `Register`s only count
        the ones specified by `CallingConventionsInterface.arguments_registers` and 
        only take as much as they are still in the given order.
        If the `Cpu` gets its arguments from stack, only take these into account '''
        cpu = self.get_cpu()
        if cpu.c_func_heuristic:
            cnt = 0
            cnt_stack_args = len(self.stack_usage_since_last_call)
            if cpu.fetches_all_arguments_from_stack():
                # only use stack args
                return cnt_stack_args
            else:
                cnt = 0
                arguments_regs = cpu.arguments_registers()
                args = self.reg_usage_since_last_call
                for arg_reg in cpu.arguments_registers():
                    if arg_reg in args:
                        cnt += 1
                    # not in right order -> no argument for function
                    else:
                        break
                # all arguments from registers taken, use stack args too
                if cnt == len(arguments_regs):
                    return cnt + cnt_stack_args 
            return cnt
            
    def _log_assignment_split(self, val1, val2):
        ''' Use to log the assignment after splitting to its operands. Mostly values after comma '''
        log.debug('assignment split: (%s, %s)', val1, val2)    
        
    def process_stack_push(self):
        ''' Push the objects onto the stack '''
        if self.get_is_stack_push():
            cpu = self.cpu
            pushed_objects = self.get_stack_push_objects()
            address = self.get_stack_address()
            try:
                for obj in pushed_objects:
                    # resolve register value
                    if isinstance(obj, Register):
                        obj = cpu.memory.registers.resolve_current_register_value(obj)
                    log.debug('pushing %s on StackFrame at address: %s' % (obj, address))
                    cpu.memory.stack.add(obj, address)        
                    address += self.get_cpu().pointer_size()
                self.stack_address = address
            except TypeError:
                pass
    
    def reset(self):
        ''' Use to reset the system after an assignment has been read. '''
        self.__init_defaults()
        
