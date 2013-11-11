'''
VizAsm

Created on 08.09.2013

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

class SeatBeltFilter(SecurityFilter):
    '''
    Check if a special sandbox profile has been set.
    
    See
    ---
    For more details and available profiles: http://iphonedevwiki.net/index.php/Seatbelt
    '''
    
    SANDBOX_PROFILES_OFFICIAL = dict(kSBXProfileNoNetwork = "nonet",
                                     kSBXProfileNoInternet = "nointernet",
                                     kSBXProfilePureComputation = "pure-computation",
                                     kSBXProfileNoWriteExceptTemporary = "write-tmp-only",
                                     kSBXProfileNoWrite = "nowrite"
                                     )
    
    def filter_method_call(self, function):
        sandbox_init_method = util.mc_c_function_has_any_name(function, ['sandbox_init'])
        profile_set = util.mc_contains_imp_got(function, 'kSBXProfile', search_substring = True)
        return sandbox_init_method or profile_set
    
    def _description(self):
        return 'Check if a special sandbox profile has been set. Available profiles are: %s' % (', '.join(self.SANDBOX_PROFILES_OFFICIAL))    
