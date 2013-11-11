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

from vizasm.analysis.asm.cpu.Resetable import Resetable
from vizasm.hopper.hopannotate import hopanno
from vizasm.util import Util
from vizasm.util.Log import log


class Registers(object, Resetable):
    r''' 
    Represents the registers of a cpu.
    
    Parameters
    ----------
    __registers: dict
        registers of the CPU
    __cpu: Cpu
    '''

#####################################################################################
# Resetable                                                                         #
#####################################################################################    

    def reset(self):
        self.__registers = dict()

#####################################################################################
# Implementation                                                                    #
#####################################################################################
        
    def __init__(self, cpu):
        self.__cpu = cpu
        self.reset()
        
    def __str__(self):
        return '%s: %s' % (self.__class__.__name__, Util.pretty_format_dict(self.registers))
    
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, Util.pretty_format_dict(self.registers, True))
    
    def get_cpu(self):
        return self.__cpu

    def set_cpu(self, value):
        self.__cpu = value
        
    def get_registers(self):
        return self.__registers

    def get_value_for_register(self, register):
        ''' 
        Return the value which is currently stored in the register.
        If register is not in dict, None will be returned
        '''  
        if register in self.get_registers():  
            return self.get_registers()[register]
        return None
    
    def _set_value_for_register(self, register, value):
        ''' Set the value for the specified register ''' 
        if None not in (register, value):
            # log
            log_msg = '%s = %s'
            log.debug(log_msg, register, value)
            
            # store value for register
            self.get_registers()[register] = value
            
    def set_value_for_register(self, register, value):
        ''' Set the value for the specified register and annotate the assignment  ''' 
        
        if None not in (register, value):
            self._set_value_for_register(register, value)
            # annotate hopper
            hopanno.annotate_assignment(register, value, self.cpu.address)
            
    def set_value_for_register_ann_method_ead(self, register, value):
        ''' Set the value for the specified register and annotate the method head ''' 
        if None not in (register, value):
            self._set_value_for_register(register, value)
            # annotate hopper
            log_msg = '%s = %s'
            hopanno.annotate_assignment_method_head(log_msg % (register, value))
        
    def resolve_current_register_value(self, register):
        '''
        Resolve the current register value. 
        If the register has an entry in the registers dictionary this will be returned.
        Otherwise the register will be returned
            
        Parameters
        ----------
        register: string
            the register for which to look up the value
        '''
        current_reg_val = self.get_value_for_register(register)
        if current_reg_val is not None:
            return current_reg_val
        return register      
    
    def delete_element(self, key):
        '''
        Delete an element from the registers dictionary.
        
        Parameters
        ----------
        key
            any key of the dictionary
        
        Returns
        -------
        True
            if the entry could be deleted
        False
            otherwise
        
        '''
        try:
            del self.registers[key]
        except KeyError:
            return False
        return True
    
    def delete_elements(self, killed_regs):
        '''
        Read a list of killed regs and delete them.
        
        Parameters
        ----------
        input_regs: list<string>
            e.g. ['rax', 'rcx', 'rdx', 'rsp' ,'rbp', 'rsi', 'rdi', 'r8']
        
        Returns
        -------
        True
            if all registers could be deleted
        False
            otherwise
        '''
        killed_all_regs = True
        if killed_regs:
            for killed_reg in killed_regs:
                if not self.delete_element(killed_reg):
                    killed_all_regs = False
        return killed_all_regs
        
    registers = property(get_registers, None, None, "__registers(dict) -- registers of the CPU")
    cpu = property(get_cpu, set_cpu, None, "__cpu(Cpu)")
