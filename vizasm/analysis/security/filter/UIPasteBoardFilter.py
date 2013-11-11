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

class UIPasteBoardFilter(SecurityFilter):
    '''
    UIPasteBoard filter
    
    See
    ---
    https://developer.apple.com/library/ios/documentation/uikit/reference/UIPasteboard_Class/Reference
    '''
    
    def config_mac_filter(self):
        return False

    def filter_method_call(self, function):
        # only match on `Selector`s cause Hopper does not always read the class correct (arm)
        sels = ['generalPasteboard', 'pasteboardWithName:create:', 'pasteboardWithUniqueName']
        return util.mc_has_any_selector(function, sels, search_substring = False)
    
    def _description(self):
        return 'Check for UIPasteboard usage '
