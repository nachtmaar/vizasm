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

class DataProtectionFilter(SecurityFilter):
    '''
    Check if data is protected.
    
    See
    ---
    https://developer.apple.com/library/ios/documentation/Cocoa/Reference/Foundation/Classes/NSData_Class/Reference/Reference.html#//apple_ref/doc/uid/20000172-BCIICCHI
    http://stackoverflow.com/questions/7471270/secure-contents-in-document-directory
    http://stackoverflow.com/questions/5155789/implementing-and-testing-ios-data-protection
    '''

    NS_DATA_WRITING_FILE_PROTECTIONS_OPTIONS = {0x10000000 : 'NSDataWritingFileProtectionNone',
                                                0x20000000 : 'NSDataWritingFileProtectionComplete',
                                                0x30000000 : 'NSDataWritingFileProtectionCompleteUnlessOpen',
                                                0x40000000 : 'NSDataWritingFileProtectionCompleteUntilFirstUserAuthentication',
                                                0xf0000000 : 'NSDataWritingFileProtectionMask'
                                                }
    
    NS_FILEMANAGER_PROTECTIONS_OPTIONS = ['NSFileProtectionNone',
                                          'NSFileProtectionComplete',
                                          'NSFileProtectionCompleteUnlessOpen',
                                          'NSFileProtectionCompleteUntilFirstUserAuthentication'
                                          ]
    
    def config_mac_filter(self):
        return False    
    
    def filter_method_call(self, function):
        return self._check_ns_file_manager(function) or self._check_nsdata_writing(function)
    
    def _description(self):
        nsdata_options = ', '.join(('%s (%s)' % (x[1], hex(x[0])) for x in self.NS_DATA_WRITING_FILE_PROTECTIONS_OPTIONS.items()))
        nsfilemgr_options = ', '.join(self.NS_FILEMANAGER_PROTECTIONS_OPTIONS)
        return '''Check for data storage via NSFileManager and NS(Mutable)Data (iOS only).
Available options for NS(Mutable)Data writing are: %s,
Available options for NSFileManager writing are: %s
''' % (nsdata_options, nsfilemgr_options)        

    def _check_ns_file_manager(self, function):
        ''' Check for file protection via NSFileManager '''
        # check for FileManager write
        file_manager_write_sels = ['createDirectoryAtURL:withIntermediateDirectories:attributes:error:',
                                  'createDirectoryAtPath:withIntermediateDirectories:attributes:error:',
                                  'createFileAtPath:contents:attributes:']
        file_manager_write = util.mc_has_any_selector(function, file_manager_write_sels, search_substring = False)
        
        # check if the NSFileProtectionKey it set somewhere
        file_protection_key_set = util.mc_contains_imp_got(function, 'NSFileProtection', search_substring = True)
        
        return any((file_manager_write, file_protection_key_set))
    
    def _check_nsdata_writing(self, function):
        '''
        Check for protection via NSData.
        
        The NSDataWritingOptions are encoded as hex values
        and are transformed to their string representation for better reading.
        
        See
        ---
        NSData.h for available NSDataWritingOptions
        '''
        # convert hex value to string representation of nsdata writing options
        # e.g. 0x10000000 -> NSDataWritingFileProtectionNone
        if util.mc_is_objectivec_function(function):
            sub_sel_name = 'options'
            for sel in function:
                sub_sel_arg = sel.get_argument_for_sub_selector(sub_sel_name)
                # correct selector
                if sub_sel_arg is not None:
                    if self.NS_DATA_WRITING_FILE_PROTECTIONS_OPTIONS.has_key(sub_sel_arg):
                        sub_sel_arg = '%s (%s)' % (self.NS_DATA_WRITING_FILE_PROTECTIONS_OPTIONS[sub_sel_arg], hex(sub_sel_arg))
                        sel.set_argument_for_sub_selector(sub_sel_name, sub_sel_arg)
                
        # writing can be done via these selectors
        nsdata_sels = ['writeToFile:options:error:', 'writeToURL:options:error:']
        return util.mc_has_any_selector(function, nsdata_sels, search_substring = False)
