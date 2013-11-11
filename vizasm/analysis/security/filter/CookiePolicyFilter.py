'''
VizAsm

Created on 16.09.2013

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

class CookiePolicyFilter(SecurityFilter):
    '''
    Check if a special cookie policy has been set
    '''
    
    COOKIE_POLICIES = {0 : 'NSHTTPCookieAcceptPolicyAlways',
                       1 : 'NSHTTPCookieAcceptPolicyNever',
                       2 : 'NSHTTPCookieAcceptPolicyOnlyFromMainDocumentDomain'
                       }
    
    def filter_method_call(self, function):
        if util.mc_is_objectivec_function(function):
            sub_sel_name = 'setCookieAcceptPolicy'
            for sel in function:
                sub_sel_arg = sel.get_argument_for_sub_selector(sub_sel_name)
                # correct selector
                if sub_sel_arg is not None:
                    if self.COOKIE_POLICIES.has_key(sub_sel_arg):
                        sub_sel_arg = '%s (%s)' % (self.COOKIE_POLICIES[sub_sel_arg], sub_sel_arg)
                        sel.set_argument_for_sub_selector(sub_sel_name, sub_sel_arg)
        return util.mc_has_any_selector(function, ['setCookieAcceptPolicy:'], search_substring = True)
        
    def _description(self):
        return 'Check if a special cookie policy has been set. Available policies: %s' % ', '.join(self.COOKIE_POLICIES.values())
