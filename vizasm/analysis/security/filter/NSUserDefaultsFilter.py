'''
VizAsm

Created on 29.07.2013

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

class NSUserDefaultsFilter(SecurityFilter):
    ''' Filter all NSUserDefault access '''
    
    def filter_method_call(self, filter_me):
        cls_found = util.mc_objc_class_with_any_name(filter_me, ['NSUserDefaults'], search_substring = False)
        if cls_found:
            return True
        return util.mc_has_any_selector(filter_me, ['standardUserDefaults'], search_substring = False)
    
    def _description(self):
        return 'Filters all NSUserDefault access'
    
#####################################################################################
# AttributeNodeInterface                                                            #
#####################################################################################

    # yellow
    
    def node_color_red(self):
        return 255

    def node_color_green(self):
        return 219

    def node_color_blue(self):
        return 73
    
        
