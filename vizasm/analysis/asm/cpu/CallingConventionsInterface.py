'''
VizAsm

Created on 28.08.2013

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

from vizasm.util import Util

class CallingConventionsInterface:
    ''' Defines the calling conventions of the `Cpu` '''
     
    def destination_register(self):
        ''' Returns the `Register` in which the destination for the selector is stored ''' 
        raise NotImplementedError
    
    def selector_register(self):
        ''' Returns the `Register` in which the selector is stored '''
        raise NotImplementedError
    
    def fetches_all_arguments_from_stack(self):
        ''' Return True if all arguments are popped from the stack rather than taking them from registers '''
        raise NotImplementedError
    
    def arguments_registers(self):
        ''' List of `Register` which specifies where the arguments are being stored.
        If the `Cpu` fetches its arguments from stack an empty list will be returned. '''
        if self.fetches_all_arguments_from_stack():
            return []
        return [self.destination_register()] + [self.selector_register()] + self.selector_arg_registers()
    
    def arguments_registers_in_sequence(self):
        ''' Return True if the `destination_register`, `selector_register`,
            and the `selector_arg_registers` are specified one behind the other in `arguments_registers`.
        '''
        return True
    
    def exclude_argument_regs(self):
        ''' Return a list<Register> from which you know, 
        that they will not be used to hold arguments for a function call '''
        return [self.stack_pointer_register(), self.frame_pointer_register()]
    
    def next_reg_for_spret(self, register):
        ''' 
        If an objc_msgSend_stret is detected, the specified `Register` for the destination and selector do not match anymore
        due to the fact that the first argument register is needed for the return address of the structure.
        This means that all `Register` get shifted right.
        At least if `arguments_registers_in_sequence`. Otherwise you have to implement this yourself!
        
        Parameters
        ----------
        register: Register
        '''    
        if self.arguments_registers_in_sequence():
            arg_regs = self.arguments_registers()
            if arg_regs:
                try:
                    cur_idx = arg_regs.index(register)
                    return arg_regs[cur_idx + 1]
                except IndexError:
                    return None
            return None
        raise NotImplementedError('`CallingConventions.arguments_registers_in_sequence` returns False, implement this method yourself!')
    
    def next_regs_for_spret(self, reg_list):
        ''' Same as `next_reg_for_spret`, but do it for the whole list of `Register` '''
        return Util.filter_not_none((self.next_reg_for_spret(reg) for reg in reg_list))
    
    def selector_arg_registers(self):
        ''' The registers(list<Register>) where the arguments for the selector are stored. 
            If the selector needs more arguments, the remaining ones are taken from the stack '''
        raise NotImplementedError
    
    def stret_selector_arg_registers(self):
        ''' The registers (list<Register>) where the arguments for the selector are stored. 
            They are only used for a objc_msgSend_stret(). A message with a structure as return value.
            The first parameters will be used as an address where the structure is returned.
            So the first `Register` of `selector_arg_registers` will be cut off.
        '''
        regs = self.selector_arg_registers()
        if regs:
            return regs[1:]
        return []
    
    def return_register(self):
        ''' The register which holds the return value '''
        raise NotImplementedError
    
    def return_reg_is_fst_arg_reg(self):
        ''' Check if the return register is also the first argument register '''
        arg_regs = self.arguments_registers()
        if arg_regs:
            return self.return_register() == self.arguments_registers()[0]
        return False
        
    def nslog_arg_registers(self):
        ''' List of registers which hold the arguments for NSLog '''
        raise NotImplementedError
    
    def stack_pointer_register(self):
        ''' Return the stack pointer as instance of Register. E.g. "rsp" on x86_64. '''
        raise NotImplementedError
    
    def frame_pointer_register(self):
        ''' Return the frame pointer register '''
        raise NotImplementedError
    
    def floating_arg_registers(self):
        ''' The registers which hold the floating-point-numbers '''
        raise NotImplementedError
    
    def _reg_list(self, regs, reg_type):
        ''' Wrap the specified register names into the corresponding `Register` class
        
        Parameters
        ----------
        regs: list<string>
            list of register names
        reg_type: Register
            The register type, the reference cannot be an initialized class !
            Use the import reference !
        
        Returns
        -------
        list<reg_type>
        ''' 
        return map(lambda x: reg_type(x), regs)
    
    def reg_list(self, regs):
        ''' 
        Implement this method by calling `_reg_list` with the register type (`reg_typereg_type`).
        
        Parameters
        ----------
        regs: list<string>
        
        Returns
        -------
        list<reg_type>
        '''
        raise NotImplementedError

if __name__ == '__main__':
    from vizasm.analysis.asm.cpu.arm.Register_Arm import Register_arm as reg
    from vizasm.analysis.asm.cpu.arm.Cpu_arm import Cpu_arm
    from vizasm.analysis.asm.cpu.arm.ParseUtil_arm import ParseUtil_arm
    cpu = Cpu_arm(superclasses_dict = None)
    pu = ParseUtil_arm(cpu, reg)
    print 'objc_msgSend_spret destination register: %s' % (cpu.next_reg_for_spret(cpu.destination_register()))
    print 'objc_msgSend_spret selector register: %s' % (cpu.next_reg_for_spret(cpu.selector_register()))
    print 'objc_msgSend_spret selector arg registers: %s' % (cpu.next_regs_for_spret(cpu.selector_arg_registers()))

