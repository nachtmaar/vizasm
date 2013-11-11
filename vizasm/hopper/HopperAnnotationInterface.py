'''
VizAsm

Created on 21.08.2013

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

class HopperAnnotationInterface:
    ''' Use this interface for classes that define a custom string representation for annotation in Hopper '''
    
    def hopper_str(self):
        ''' Get the string representation annotating hopper '''
        raise NotImplementedError
    
    @staticmethod
    def try_get_hopper_string(obj):
        '''
        Use the `hopper_str()` representation if available.
        Otherwise take str() representation.
        '''
        if isinstance(obj, HopperAnnotationInterface):
            return obj.hopper_str()
        return str(obj)
