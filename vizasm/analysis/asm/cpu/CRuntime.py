'''
VizAsm

Created on 18.09.2013

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

from vizasm.analysis.asm.cpu.objcruntime.ObjectiveCRuntime import \
    ObjectiveCRuntime


class CRuntime:
    ''' Manages c specific stuff '''    
    
    def create_and_store_c_func_arguments(self, method):
        '''
        Create and store the arguments for the function.
        Cause you dont know how many the function takes, create as much as registers are available
        to store it.
        
        Parameters
        ----------
        method: Function
        '''
        # create the arguments for a c function
        if method is not None and method.is_c_function():
            for i, reg in enumerate(self.arguments_registers(), 1):
                arg = ObjectiveCRuntime.create_method_selector_arg(i)
                self.memory.registers.set_value_for_register_ann_method_ead(reg, arg)        
        
        
