'''
Created on 28.08.2013

@author: nils

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

from vizasm.analysis.asm.cpu.x86_64.ASM_x86_64 import ASM_x86_64

class ASM_x86(ASM_x86_64):

    def _var_assignment_action(self, var_assign):
        ''' For x86 a line like e.g "mov        eax, dword [ds:eax+0x4]
         with eax = self needs to resolve the `Ivar` from the `IVarRefLookup`'''
        return self.cpu.objc_runtime.ivar_lookup.get_ivar_ref(var_assign.selfref_value)
