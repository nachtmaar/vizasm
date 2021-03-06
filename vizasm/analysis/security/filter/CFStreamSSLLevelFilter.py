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

class CFStreamSSLLevelFilter(SecurityFilter):
    ''' 
    Check the SSL level of a CFStream.
    
    See
    ---
    CFSocketStream.h
    https://developer.apple.com/library/mac/documentation/Networking/Conceptual/CFNetwork/CFStreamTasks/CFStreamTasks.html#//apple_ref/doc/uid/TP30001132-CH6-SW1

    '''
    
    CFSTREAM_LEVELS = ['kCFStreamSocketSecurityLevelNone', 'kCFStreamSocketSecurityLevelTLSv1,',
                      'kCFStreamSocketSecurityLevelSSLv2', 'kCFStreamSocketSecurityLevelSSLv3',
                      'kCFStreamSocketSecurityLevelNegotiatedSSL']
    
    def filter_method_call(self, function):
        return util.mc_contains_imp_got(function, 'kCFStreamSSL', search_substring = True)
        
    def _description(self):
        return 'Check the SSL level of a CFStream. Available levels are: %s' % ', '.join(self.CFSTREAM_LEVELS)
