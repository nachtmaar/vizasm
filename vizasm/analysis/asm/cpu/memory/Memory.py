'''
VizAsm

Created on 17.09.2013

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

from vizasm.analysis.asm.cpu.Resetable import Resetable
from vizasm.analysis.asm.cpu.memory.MemoryLookupException import \
    MemoryCouldNotGetAllStackValues, MemoryCouldNotGetAllRegisterValues
from vizasm.analysis.asm.cpu.memory.Registers import Registers
from vizasm.analysis.asm.cpu.memory.StackFrame import StackFrame
from vizasm.util.Log import log

class Memory(object, Resetable):
    ''' 
    Manages the memory of the `Cpu`.
    This includes `Register`s as well as the `StackFrame`.
    
    Parameters
    ----------
    cpu: Cpu
        the corresponding cpu
    _registers: Registers
        Registers of the cpu
    _stack: StackFrame
        Stack of the cpu    
    '''
    
#####################################################################################
# Resetable                                                                         #
#####################################################################################    

    def reset(self):
        ''' Reset the memory by resetting the registers and stack '''
        self.registers.reset()
        self.stack.reset()
        
#####################################################################################
# Implementation                                                                    #
#####################################################################################
    
    def __init__(self, cpu):
        self._cpu = cpu
        self._registers = Registers(cpu)
        self._stack = StackFrame(cpu)
        
    def __str__(self):
        return '%s:\n %s\n %s' % (self.__class__.__name__, self.registers, self.stack)
    
    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, repr(self.registers), repr(self.stack))
    
    def get_cpu(self):
        return self._cpu

    def set_cpu(self, value):
        self._cpu = value

    def get_registers(self):
        return self._registers

    def get_stack(self):
        return self._stack        
    
    cpu = property(get_cpu, set_cpu, None, "cpu(Cpu) -- the corresponding cpu")
    registers = property(get_registers, None, None, "_registers(Registers) -- registers of the CPU")
    stack = property(get_stack, None, None, "_stack(StackFrame)  -- stack of the CPU")
    
    def get_argument(self, register = None, objc_msgSend_stret = False):
        ''' Get an argument from the specified `Register`.
        If the `Cpu` fetches its arguments from stack, pop it from where.
        
        Parameters
        ----------
        objc_msgSend_stret: bool, optional (default is False)
            indicate an objc_msgSend_stret
            
        Parameters
        ----------
        register: Register
            from which `Register` to get_from_idx the argument
        ''' 
        res = None
        if self.cpu.fetches_all_arguments_from_stack():
            res = self.stack.pop()
            # pop address for structure return from stack
            if objc_msgSend_stret:
                log.debug('popped structure return address from stack due to objc_msgSend_stret(). Popped: %s', res)
                res = self.stack.pop()
        else:
            res = self.get_registers().get_value_for_register(register)
        return res    
    
    def get_arguments(self, cnt, register_list, try_only = False):
        ''' Look up the values of `Register`s and return a list of the looked up values,
        but only if the `Cpu` fetches arguments from stack (returns []).
        
        Parameters
        ----------
        cnt: int
            the number of arguments to look up
        register_list:list<Register>
            the register list from which to get the value
        try_only: bool, optional (default is False)
            If True no exception will be raised if not all values could be looked up.
            Tries to get the maximum number of arguments it can until one is None
            
        Raises
        ------
        MemoryCouldNotGetAllRegisterValues
            raised if not all values could be looked up and not `try_only`
        MemoryCouldNotGetAllStackValues
            raised if not all values could be looked up and not `try_only`
                        
        Returns
        -------
        arguments: list<object>
            list of resolved registers
        ''' 
        arguments = []
        try:
            arguments = self.get_arguments_from_registers(cnt, register_list, try_only)
            # still arguments needed, take them from stack
            cnt_args_needed = cnt - len(arguments)
            if cnt_args_needed:
                try:
                    stack_args = self.get_arguments_from_stack(cnt_args_needed, try_only)
                    arguments.extend(stack_args)
                except MemoryCouldNotGetAllStackValues:
                    raise
        except (MemoryCouldNotGetAllRegisterValues, MemoryCouldNotGetAllStackValues):
            if try_only:
                return arguments
            else:
                raise
        return arguments      
        
    def get_arguments_from_registers(self, cnt, register_list, try_only = False):
        ''' Look up the values of registers and return a list of the looked up values,
        but only if the `Cpu` fetches arguments from stack (returns []).
        
        Parameters
        ----------
        cnt: int
            the number of arguments to look up
        register_list:list<Register>
            the register list from which to get the value
        try_only: bool, optional (default is False)
            If True no exception will be raised if not all values could be looked up.
            Tries to get the maximum number of arguments it can until one is None
            
        Raises
        ------
        MemoryCouldNotGetAllRegisterValues
            raised if not all values could be looked up and not `try_only`
        MemoryCouldNotGetAllStackValues
            raised if not all values could be looked up and not `try_only`
                        
        Returns
        -------
        arguments: list<object>
            list of resolved registers
        ''' 
        arguments = []
        cpu = self.cpu
        if not self.cpu.fetches_all_arguments_from_stack():
            # only resolve as much registers as indicated by cnt
            for reg in register_list[:cnt]:
                argument = self.get_registers().get_value_for_register(reg)
                if argument is None:
                    if register_list != cpu.floating_arg_registers():
                        self.get_arguments_from_registers(cnt, cpu.floating_arg_registers(), try_only)
                    else:
                        if try_only:
                            return arguments
                        else:
                            raise MemoryCouldNotGetAllRegisterValues(cpu, register_list, arguments)
                else:
                    arguments.append(argument)
        return arguments
    
    def get_arguments_from_stack(self, cnt, try_only = False):
        ''' Get a number of stack arguments.
    
        Parameters
        ----------
        cnt: int 
            the number of stack arguments to look up
        try_only: bool, optional (default is False)
            If True no exception will be raised if not all values could be looked up.
            Tries to get the maximum number of arguments it can until one is None
            
        Raises
        ------
        MemoryCouldNotGetAllStackValues
            raised if not all values could be looked up and not `try_only`
            
        Returns
        -------
        arguments: list<object>
            list of arguments
        ''' 
        arguments = []
        stack = self.stack
        # only resolve as much registers as indicated by cnt
        for i, _ in enumerate(range(cnt)):
            argument = None
            if stack:
                argument = stack.get_from_idx(i)
            if argument is None:
                if try_only:
                    return arguments
                else:
                    raise MemoryCouldNotGetAllStackValues(self.cpu, cnt, arguments)
            else:
                arguments.append(argument)
        return arguments
    
    def get_arguments_from_asm_heuristic(self):
        ''' Use the number of arguments (stack and register usage since last call, See the `AssignmentMatchingSystem`)
        to determine the number of arguments for the function.
        
        Only works if the c function call arguments heuristic is enabled!
        
        Returns
        -------
        list<object>
        '''
        cpu = self.cpu
        arguments = []
        if cpu.c_func_heuristic:
            cnt_args = cpu.assignment_matching_system.number_of_arguments_since_last_call()
            if cpu.fetches_all_arguments_from_stack():
                arguments = self.get_arguments_from_stack(cnt_args, try_only = True)
            else:
                arguments = self.get_arguments(cnt_args, cpu.arguments_registers(), try_only = True)
        return arguments
    
    def set_return_register_value(self, value):
        ''' Set the value for the return register '''
        return_reg = self.cpu.return_register()
        self.get_registers().set_value_for_register(return_reg, value)
