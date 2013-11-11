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

from vizasm.analysis.security.filter.SecurityFilter import SecurityFilter
import util

class UntrustedSSLCertsFilter(SecurityFilter):
    '''
    Check if invalid SSL certificates are being accepted.
    
    See
    ---
    http://stackoverflow.com/questions/933331/how-to-use-nsurlconnection-to-connect-with-ssl-for-an-untrusted-cert/#comment13096647_2033823
    http://stackoverflow.com/questions/2001565/alternative-method-for-nsurlrequests-private-setallowsanyhttpscertificateforh
    https://github.com/pokeb/asi-http-request
    '''
    def config_filter_method_definition(self):
        return True
    
    def config_filter_method_call(self):
        return True
    
    def filter_method_call(self, filter_me):
        # check for ASIHTTPRequest (wrapper around CFNetwork API) setValidatesSecureCertificate:
        # and continueWithoutCredentialForAuthenticationChallenge (NSURLConnectionDelegate)
        # as well as setAllowsAnyHTTPSCertificate:forHost (NSURLRequest)
        selector_list = ['continueWithoutCredentialForAuthenticationChallenge', 'setValidatesSecureCertificate:', 'setAllowsAnyHTTPSCertificate:forHost:']
        return util.mc_has_any_selector(filter_me, selector_list, search_substring = False)

    def filter_method_definition(self, method):
        # category on NSURLRequest overwrites allowsAnyHTTPSCertificateForHost method
        return util.md_filter_category(method, 'allowsAnyHTTPSCertificateForHost:', category_on = 'NSURLRequest', category_name = None, search_substring = True) 
    
    def _description(self):
        return 'Check if invalid SSL certificates are being accepted'
    
#####################################################################################
# AttributeNodeInterface                                                            #
#####################################################################################

    def node_color_red(self):
        return 255

    def node_color_green(self):
        return 0

    def node_color_blue(self):
        return 0
