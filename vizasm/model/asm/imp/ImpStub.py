'''
VizAsm

Created on 02.04.2013

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

from vizasm.model.asm.imp.Imp import Imp

class ImpStub(Imp):
    ''' 
    Represents implementation stubs like e.g.:
        imp___stubs
        imp___stubs__NSApplicationMain
        imp___stubs__objc_msgSend
        
        imp___stubs__objc_retain
        imp___stubs__objc_retainAutorelease
        imp___stubs__objc_retainAutoreleasedReturnValue
        
        imp___stubs__objc_release
        imp___stubs__objc_autoreleaseReturnValue
        
        
        imp___stubs__NSLog
        imp___stubs__objc_setProperty_atomic
        imp___stubs__objc_getProperty
        imp___stubs__objc_storeStrong
        
    and implementation gots like e.g.:
        imp___got__objc_msgSend
        
    Parameters
    ----------
    imp_stub
        mapped to value of `Value`
    '''
    
    NSLOG = 'NSLog'
    PRINTF = 'printf'
    
    SET_PROPERTY = 'objc_setProperty'
    GET_PROPERTY = 'objc_getProperty'
    STORE_STRONG = 'objc_storeStrong'
    
    def __init__(self, imp_stub):
        Imp.__init__(self, imp_stub)
    
    def is_nslog(self):
        ''' Check if ImpStub is NSLog '''
        return self.get_imp() == ImpStub.NSLOG
    
    def is_printf(self):
        ''' Check if ImpStub is print '''
        return self.get_imp() == ImpStub.PRINTF
    
    def is_any_printf(self):
        ''' Check if ImpStub is any printf '''
        return self.get_imp().find(ImpStub.PRINTF) != -1
    
    def is_format_string_log(self):
        ''' Check if ImpStub is NSLog or printf '''
        return any((self.is_nslog(), self.is_any_printf()))
    
    def is_get_property(self):
        ''' Check if ImpStub is get_property '''
        return self.get_imp() == ImpStub.GET_PROPERTY
    
    def is_set_property(self):
        ''' Check if ImpStub is autorelease '''
        return self.get_imp() == ImpStub.SET_PROPERTY

    def is_store_strong(self):
        ''' Check if ImpStub is store_strong '''
        return self.get_imp() == ImpStub.STORE_STRONG

