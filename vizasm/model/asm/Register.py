'''
VizAsm

Created on 09.06.2013

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

from copy import deepcopy
  
class Register(object):
    '''
    This class represents an register of the cpu.
    It implements a fallback support for a register if the `register_dict` variable is set.
    
    Fallback support means e.g. that "eax" presents the lower 32 bits of "rax" and 
    if the value of "eax" cannot be looked up in the Registers class, all of the fallback registers can be tried.  
    
    A Register is equal to another, if they have the same fallback list.
    If the fallback list is None, the register is used for equality. 
    
    Parameters
    ----------
    register: string
    fallback_list: list<string>
        list of equivalent registers used for fallback support. E.g. on x86_64 'rsp' and 'esp' are equal.
    '''
    def __init__(self, register, register_dict = None):
        '''
        Parameters
        ----------
        register_dict: dict<string, list<string>>
            dictionary containing a list of fallback registers for each register
        '''
        self._register = register
        self._fallback_list = self.fallback_support(register, register_dict)

    def get_register_dict(self):
        return self._register_dict

    def set_register_dict(self, value):
        self._register_dict = value

    def get_register(self):
        return self._register

    def get_fallback_list(self):
        return self._fallback_list

    def set_register(self, value):
        self._register = value

    def set_fallback_list(self, value):
        self._fallback_list = value

    def __hash__(self):
        return hash((tuple(self.fallback_list)))

    def __eq__(self, other):
        if isinstance(other, Register):
            return self is other or (tuple(self.fallback_list)) == (tuple(other.fallback_list))
        return False
    
    def __ne__(self, other):
        return not self == other
    
    def __str__(self):
        return self.register
    
    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.register, self.fallback_list)
    
    register = property(get_register, set_register, None, "register(string)")
    fallback_list = property(get_fallback_list, set_fallback_list, None, "fallback_list(list<string>) -- list of equivalent registers used for fallback support. E.g. on x86_64 'rsp' and 'esp' are equal.")
    
    @staticmethod
    def fallback_support(register, register_dict):
        '''
        Returns a list of registers which are equal in the manner that one registers uses the memory space of the other.
        E.g. "eax" presents the lower 32 bits of "rax".
         
        Parameters
        ----------
        register: string
        register_dict: dict<string, list<string>>
            dictionary containing a list of fallback registers for each register
        
        Returns
        -------
        reg_list: list<string>
            a list of fallback registers. The Register `register` is also included in the list.
        '''
        fallback_reg_list = [register]
        if register_dict is not None:
            for key, val in register_dict.items():
                reg_list = deepcopy(val)
                reg_list.append(key)
                if register in reg_list:
                    return reg_list
        return fallback_reg_list
