'''
VizAsm

Created on 22.04.2013

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

class RandomFuncFilter(SecurityFilter):
    def __init__(self, name = None, methodcall = None):
        SecurityFilter.__init__(self, name, methodcall)
        
    RAND_FUNCS = ['rand', 'random', 'arc4random']
    
    def filter_method_call(self, filter_me):
        return util.mc_c_function_has_any_name(filter_me, self.RAND_FUNCS)
        
    def _description(self):
        return 'Look out for functions generating random values: %s' % ', '.join(self.RAND_FUNCS)
    
#####################################################################################
# AttributeNodeInterface                                                            #
#####################################################################################

    def node_color_red(self):
        return 0

    def node_color_green(self):
        return 0

    def node_color_blue(self):
        return 255
