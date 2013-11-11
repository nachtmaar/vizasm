'''
VizAsm

Created on 30.10.2013

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

# the util package contains the filter api
import util

class CustomFilter(SecurityFilter):
    ''' Template for a custom filter '''

#####################################################################################
# Specify architecture                                                              #
#####################################################################################

    def config_ios_filter(self):
        # default is True
        return SecurityFilter.config_ios_filter(self)

    def config_mac_filter(self):
        # default is True
        return SecurityFilter.config_mac_filter(self)
    
#####################################################################################
# Filter on method call or definition ?                                             #
#####################################################################################

    def config_filter_method_call(self):
        # default is True
        # use util.mc_ functions
        return SecurityFilter.config_filter_method_call(self)

    def config_filter_method_definition(self):
        # default is False
        # use util.md_ functions
        return SecurityFilter.config_filter_method_definition(self)

#####################################################################################
# Actual filtering                                                                  #
#####################################################################################

    def filter_method_call(self, function):
        # filter on a method call
        return util.mc_contains_imp_got(function, 'kCFStreamSSL', search_substring = True)
        
    def filter_method_definition(self, method):
        # filter on a method definition
        return SecurityFilter.filter_method_definition(self, method)

#####################################################################################
# Representation                                                                    #
#####################################################################################        

    def _description(self):
        return 'Supply your filter description!'

#####################################################################################
# Node color                                                                        #
# if no rgb values are given, a random color will be chosen                         # 
#####################################################################################

    def node_color_red(self):
        return SecurityFilter.node_color_red(self)

    def node_color_green(self):
        return SecurityFilter.node_color_green(self)

    def node_color_blue(self):
        return SecurityFilter.node_color_blue(self)
    