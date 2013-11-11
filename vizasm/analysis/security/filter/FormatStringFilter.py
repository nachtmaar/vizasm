'''
VizAsm

Created on 20.04.2013

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

import util
from vizasm.analysis.security.filter.SecurityFilter import SecurityFilter

class FormatStringFilter(SecurityFilter):
    '''
    Check for exploitable log function  
    '''
    
    # dictionary thats knows at which argument idx the format string is located
    # see man printf    
    FORMAT_STRING_ARG_IDX = dict(
                                 NSLog = 0,
                                 printf = 0,
                                 fprintf = 1,
                                 sprintf = 1,
                                 snprintf = 2,
                                 asprintf = 1,
                                 dprintf = 1,
                                 vprintf = 0,
                                 vfprintf = 1,
                                 vsprintf = 1,
                                 vsnprintf = 2,
                                 vasprintf = 1,
                                 vdprintf = 1
                                 ) 

    def filter_method_call(self, function):
        return util.mc_is_exploitable_log_func(function)
    
    def _description(self):
        return 'Check for exploitable log function (printf and NSLog)'

#####################################################################################
# AttributeNodeInterface                                                            #
#####################################################################################

    def node_color_red(self):
        return 0

    def node_color_green(self):
        return 255

    def node_color_blue(self):
        return 0
