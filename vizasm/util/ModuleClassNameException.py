'''
VizAsm

Created on 01.08.2013

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

class ModuleClassNameException(Exception):
    ''' Exception for the case that the module does not have the specified class '''
    
    def __init__(self, module_name, class_name):
        self.module_name = module_name
        self.class_name = class_name
        
    def __str__(self):
        return 'The module (%s) does not have the specified class (%s) !' % (self.module_name, self.class_name)  
    
    
class ModuleNotSameClassNameException(Exception):
    ''' Exception for the case that the module has a different name than the class '''
    
    def __init__(self, module_name):
        self.module_name = module_name
        
    def __str__(self):
        return 'The module name (%s) does not equal the class name !' % self.module_name  
        