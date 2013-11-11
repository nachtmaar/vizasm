'''
VizAsm

Created on 04.04.2013

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
    MemoryCouldNotGetAllRegisterValues, MemoryCouldNotGetAllStackValues
from vizasm.model.objc.arguments.ArgumentsOverloadedException import \
    ArgumentsOverloadedException
from vizasm.model.objc.arguments.ArgumentsUnderloadedException import \
    ArgumentsUnderloadedException
from vizasm.model.objc.object.nsobject.NSObject import NSObject


class Arguments(NSObject, Resetable):
    ''' 
    Superclass for a class with arguments that can be filled from the cpu (register or stack)

    Parameters
    ----------
    arguments: list<object>
        queue holding selector arguments   

    Notes
    -----
    cnt_needs_arguments
    cnt_has_arguments
    ''' 
    
    def __init__(self, name, arguments, is_static):
        NSObject.__init__(self, name, is_static)
        self.__arguments = arguments
    
    def __hash__(self):
        return hash((NSObject.__hash__(self), tuple(self.get_arguments())))
    
    def __eq__(self, other):
        if isinstance(other, Arguments):
            return self is other or ((self.get_arguments() == (other.get_arguments())) and NSObject.__eq__(self, other))
        return False
    
    def __ne__(self, other):
        return not self == other    
    
    def __iter__(self):
        ''' Return and iterator over the arguments '''
        return iter(self.arguments)
    
    def get_arguments(self):
        return self.__arguments

    def set_arguments(self, value):
        self.__arguments = value

    def add_argument(self, argument):
        ''' 
        Add an argument to the object. 
        Subclasses should raise their own Exception if the arguments are overloaded.
        
        Raises
        ------
        ArgumentsOverloadedException
            if the class has more arguments than it needs
        RuntimeError
            if a subclass of `Arguments` is already in the arguments.
        ''' 
        if self.needs_more_arguments():
            if self._is_runtime_exception_safe(argument):
                self.get_arguments().append(argument)
            else:
                raise RuntimeError('Its not RuntimeError-safe to add the argument: %s' % argument)
        else:
            raise ArgumentsOverloadedException(self, argument)
        
    def try_add_arguments(self, arg_list):
        ''' Try to add the arguments. Trying means not to raise any exception if the operation fails. '''
        for arg in arg_list:
            try:
                self.add_argument(arg) 
            except ArgumentsOverloadedException:
                pass
    
    def clear_arguments(self):
        ''' Reset the arguments '''
        self.set_arguments([])
        
    def cnt_needs_arguments(self):
        ''' Return the number of arguments needed '''
        raise NotImplementedError
    
    def cnt_has_arguments(self):
        ''' Return the number of arguments currently available ''' 
        raise NotImplementedError
    
    def needs_more_arguments(self):
        ''' Return if more arguments are needed '''
        return self.cnt_missing_arguments() > 0
    
    def cnt_missing_arguments(self):
        ''' Return the number of missing arguments '''
        return self.cnt_needs_arguments() - self.cnt_has_arguments()

    def fill_from_cpu(self, cpu, register_list):
        ''' 
        Fill as much arguments as possible from cpu (registers and stack).
        
        Parameters
        ----------
        register_list: list<Register>
            the list of registers from which to fill 
    
        Raises
        ------
        ArgumentsUnderloadedException
            raised if more arguments than needed came from the cpu
        ArgumentsOverloadedException
            raised if not enough arguments came from the cpu
        '''
        cnt_arguments = self.cnt_missing_arguments()
        arguments = []
        try:
            arguments = cpu.memory.get_arguments_from_registers(cnt_arguments, register_list)
            # fill arguments for arguments if they can/need arguments 
            for arg in arguments:
                if isinstance(arg, Arguments):
                    # fill using not used registers of the register list
                    arg.fill_from_cpu(cpu, register_list[cnt_arguments:])
        except MemoryCouldNotGetAllRegisterValues:
            raise ArgumentsUnderloadedException(self, cpu)
        finally:
            for arg in arguments:
                self.add_argument(arg)
            if len(arguments) < cnt_arguments:
                return self._fill_remaining_args_from_stack(cpu)
            
    def _fill_remaining_args_from_stack(self, cpu):
        ''' 
        Fill as much arguments as possible from stack. 
    
        Raises
        ------
        ArgumentsUnderloadedException
            raised if more arguments than needed came from the stack of the cpu
        ArgumentsOverloadedException
            raised if not enough arguments came from the stack of the cpu
        '''
        arguments = []
        if self.needs_more_arguments():
            cnt_missing_args = self.cnt_missing_arguments()
            try:
                arguments = cpu.memory.get_arguments_from_stack(cnt_missing_args)
            except MemoryCouldNotGetAllStackValues:
                raise ArgumentsUnderloadedException(self, cpu)
            finally:
                for arg in arguments:
                    self.add_argument(arg)    
    
    def _is_runtime_exception_safe(self, ext_arg):
        ''' Check if a subclass of `Arguments` is already in the arguments.
        Use this to prevent a `RuntimeError`.
        If true it is safe to add the `ext_arg` to the arguments.
        '''
        if isinstance(ext_arg, Arguments):
            if self._contains_argument(ext_arg):
                return False
        return True
    
    def _contains_argument(self, ext_arg):   
        ''' Check recursive if `ext_arg` is already an argument inside the `Arguments` class '''
        if ext_arg in self:
            return True
        for arg in self:
            if isinstance(arg, Arguments):
                if arg._contains_argument(ext_arg):
                    return True
            
    arguments = property(get_arguments, set_arguments, None, "arguments(list<object>) -- queue holding selector arguments")
    
#####################################################################################
# Resetable                                                                         #
#####################################################################################

    def reset(self):
        ''' Reset the `Arguments` by clearing its arguments '''
        self.arguments = []
