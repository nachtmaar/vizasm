'''
VizAsm

Created on 23.08.2013

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

from vizasm.model.asm.Register import Register

REGISTER_DICT = register_dict = dict(r13 = ['sp'], r14 = ['lr'], r15 = ['pc'])

class Register_arm(Register):
    ''' Implements an register for the x86_64 architecture 
    
    Notes
    -----
    Register list taken from: http://msdn.microsoft.com/en-us/library/ms253983(v=vs.80).aspx
    and http://www.raywenderlich.com/37181/ios-assembly-tutorial.
    '''
    def __init__(self, register):
            Register.__init__(self, register, REGISTER_DICT)