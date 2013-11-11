'''
VizAsm

Created on 07.04.2013

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

from vizasm.analysis.asm.cpu.Resetable import Resetable
from vizasm.analysis.asm.cpu.exceptions.CpuException import CpuException
from vizasm.hopper.hopannotate import hopanno
from vizasm.util import Util
from vizasm.util.Log import log


class NoSuchStackObjectException(CpuException):
    '''
    Exception for the case that the element at the specified address or idx does not exist.
    
    Parameters
    ----------
    addr: int
    stack: StackFrame
    '''    
    
    def __init__(self, addr, stack): 
        CpuException.__init__(self, None)
        self._addr = addr
        self._stack = stack
    
    def __str__(self):
        return 'There is no object at address/idx: %d on the stack frame:\n%s' % (self._addr, self._stack)
    
class NoSuchStackObjectAtAddressException(NoSuchStackObjectException):
    def __str__(self):
        return 'There is no object at address: %d on the stack frame:\n%s' % (self._addr, self._stack)    
    
class NoSuchStackObjectAtIdxException(NoSuchStackObjectException):
    def __str__(self):
        return 'There is no object at idx: %d on the stack frame:\n%s' % (self._addr, self._stack)
    
class StackFrame(object, Resetable):
    r''' 
    Represents a stack frame.
        
    Let r10 = arg1, r11 = arg2, rbx = arg3, then pushes to stack look like (x86_64 example):
    
    "0000000100002b67 4C891424                        mov        qword [ss:rsp], r10
    
    0000000100002b6b 4C895C2408                       mov        qword [ss:rsp+0x8], r11
    
    0000000100002b70 48895C2410                       mov        qword [ss:rsp+0x10], rbx"
    
    The example leads to the stack: arg1, arg2, arg3 (with top of the stack = left, lowest address)

    Parameters
    ----------
    __stack: dict<int, object>
        stack of the CPU
    __cpu: Cpu
    '''

#####################################################################################
# Resetable                                                                         #
#####################################################################################    

    def reset(self):
        self.__stack = {}
        
#####################################################################################
# Implementation                                                                    #
#####################################################################################

    # TODO: keep stack sorted?? -> IMRPROVES PERFORMANCE! OrderedDict ?
    def __init__(self, cpu):
        self.__cpu = cpu
        self.reset()

    def __str__(self):
        return '%s: %s' % (self.__class__.__name__, Util.pretty_format_dict(self.stack))
    
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, Util.pretty_format_dict(self.stack, True))

    def __len__(self):
        return len(self.stack)
    
    def get_stack(self):
        return self.__stack

    def set_stack(self, value):
        self.__stack = value

    def get_cpu(self):
        return self.__cpu

    def set_cpu(self, value):
        self.__cpu = value

    def stack_is_empty(self):
        ''' Return whether the stack is empty '''
        return bool(self.get_stack())
        
    stack = property(get_stack, set_stack, None, "__stack(dict<int, object>) -- stack of the CPU")
    cpu = property(get_cpu, set_cpu, None, "__cpu(Cpu)") 
    
    def add(self, value, address):
        '''
        Add an object to the `StackFrame`.
        The stack grows to higher addresses, 
        meaning that the top of the stack is always the value with the lowest address.
        The order in which the elements are added does not play any role.
        The order is given by the `address`.
        
        Parameters
        ----------
        address: int
        '''
        msg = 'stack frame at %s' % hex(address)
        hopanno.annotate_assignment(msg, value, self.cpu.address)
        log.debug(msg)
        self.stack[address] = value
        
    def add_from_idx(self, value, idx):
        ''' Add an value from given `idx` '''
        self.add(value, idx * self.cpu.pointer_size())
    
    def pop(self):
        ''' Pop item. Top of stack is the lowest address '''
        items_list = sorted(self.stack.items())
        key = val = None
        if items_list:
            key, val = items_list[0] 
            self.stack.pop(key)
        return val
    
    def get_from_idx(self, idx):
        '''
        Get element from given `idx`.
        
        Raises
        ------
        NoSuchStackObjectAtIdxException
            if there is no object at the given idx
        '''
        items_list = sorted(self.stack.items())
        val = None
        if items_list:
            try:
                _, val = items_list[idx] 
                return val
            except IndexError:
                raise NoSuchStackObjectAtIdxException(idx, self), None, sys.exc_info()[2]
        return None
    
    def __getitem__(self, addr):
        '''
        Raises
        ------
        NoSuchStackObjectAtIdxException
            if there is no object at the given address
        '''
        try:
            return self.stack[addr]
        except KeyError:
            raise NoSuchStackObjectAtAddressException(addr, self), None, sys.exc_info()[2]
        
if __name__ == '__main__':
    sf = StackFrame()
    sf.add('arg3', 0x3e8)
    sf.add('arg2', 0x3e7)
    sf.add('arg4', 0x2710)
    sf.add('arg1', 0)
    sf.add('arg5', 0x186a0)
    print sorted(sf.stack.items())
    print sf.pop()
    print sf.get_from_idx(0)
    print sf.get_from_idx(1)
