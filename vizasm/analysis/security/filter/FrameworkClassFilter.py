'''
VizAsm

Created on 14.09.2013

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

from vizasm.analysis.security.filter.SecurityFilter import SecurityFilter
import util

class FrameworkClassFilter(SecurityFilter):
    ''' Filter classes that belong to the Apple framework. Currently only working on x86_64 platform. '''
    
    def config_ios_filter(self):
        return False
    
    def filter_method_call(self, function):
        clazz = util.mc_get_objc_class(function)
        if clazz is not None:
            return util.is_frameworkclass(clazz)
        return False
        
    def _description(self):
        return 'Filter classes that belong to the Apple framework. Currently only working on x86_64 platform.'
