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

class FillFromCpuInterface:
    ''' Interface for filling data of an object from cpu (registers or stack) '''
    
        
    def fill_from_cpu(self, cpu):
        ''' Fill data of object from cpu (registers or stack) '''
        raise NotImplementedError
