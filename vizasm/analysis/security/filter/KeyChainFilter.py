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

class KeyChainFilter(SecurityFilter):
    '''
    Check for Keychain usage.
    
    See
    ---
    https://developer.apple.com/library/mac/documentation/Security/Conceptual/keychainServConcepts/01introduction/introduction.html#//apple_ref/doc/uid/TP30000897-CH203-TP1
    '''
    def filter_method_call(self, function):
        keychain_methods = ['SecItem',  # iOS
                           'SecKeychain']  # Mac
        keychain_wrapper = util.mc_objc_class_with_any_name(function, ['KeychainItemWrapper'], search_substring = True)
        keychain_method = util.mc_c_function_has_any_name(function, keychain_methods, search_substring = True)
        return keychain_wrapper or keychain_method
        
    def _description(self):
        return 'Check for Keychain usage'
