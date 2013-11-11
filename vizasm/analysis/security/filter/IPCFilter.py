'''
VizAsm

Created on 09.09.2013

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


class IPCFilter(SecurityFilter):
    ''' Interprocess communication filter '''
    
    def config_filter_method_definition(self):
        return True
    
    def filter_method_call(self, function):
        # check for something like [[UIApplication sharedApplication] openURL:url];    
        shared_app_sel = 'sharedApplication'
        open_url_sel = 'openURL:'
        shared_app_sel_match = util.mc_has_any_selector(function, [shared_app_sel], search_substring = False) 
        open_url_sel_match = util.mc_has_any_selector(function, [open_url_sel], search_substring = False)
        return shared_app_sel_match and open_url_sel_match
        
    def filter_method_definition(self, method):
        # check for "- (BOOL)application:(UIApplication *)application handleOpenURL:(NSURL *) url;" from UIApplicationDelegate.
        sel = 'application:handleOpenURL:'
        return util.md_filter_method_defintion(method, class_name = None, selector_name = sel, search_substring = True)
    
    def _description(self):
        return '''Check if the app has configured its own URL handler (iOS only) or does any interprocess communication call '''
