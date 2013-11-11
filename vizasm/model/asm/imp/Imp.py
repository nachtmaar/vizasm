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

from vizasm.model.asm.Value import Value

class Imp(Value):
    ''' 
    Base class for `ImpStub` and `ImpGot`.
    '''
    
    MSG_SEND = 'objc_msgSend'
    MSG_SEND_STRET = 'objc_msgSend_stret'
    MSG_SEND_FPRET = 'objc_msgSend_fpret'
    
    MSG_SEND_SUPER = 'objc_msgSendSuper'
    MSG_SEND_SUPER_STRET = 'objc_msgSendSuper_stret'
    
    RETAIN = 'objc_retain'
    RETAIN_AUTORELEASE = 'objc_retainAutorelease'
    RETAIN_AUTORELEASED_RETURN_VALUE = 'objc_retainAutoreleasedReturnValue'
    RETAIN_FUNCTIONS = (RETAIN, RETAIN_AUTORELEASE, RETAIN_AUTORELEASED_RETURN_VALUE)
    
    RELEASE = 'objc_release'
    AUTORELEASE = 'autoreleaseReturnValue'
    
    def __init__(self, imp):
        Value.__init__(self, imp)
    
    def __str__(self):
        return self.get_imp()
    
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.get_imp())
    
    def get_imp(self):
        return self.get_value()   

    imp = property(get_imp, None, None, "")
        
    def is_msg_send(self):
        ''' Check if ImpStub is objc_msgSend '''
        return self.get_imp() == Imp.MSG_SEND
    
    def is_msg_send_fpret(self):
        ''' Check if ImpStub is objc_msgSend_fpret.
        This is a message with float return value '''
        return self.get_imp() == Imp.MSG_SEND_FPRET
    
    def is_msg_send_stret(self):
        ''' Check if ImpStub is objc_msgSend_stret.
        This is a message with a data-structure return value '''
        return self.get_imp() == Imp.MSG_SEND_STRET
    
    def is_msg_send_super(self):
        ''' Check if ImpStub is objc_msgSendSuper(2) '''
        return not self.is_msg_send_super_stret() and self.get_imp() == Imp.MSG_SEND_SUPER
    
    def is_msg_send_super_stret(self):
        ''' Check if ImpStub is objc_msgSendSuper_stret(2).
        This is a message send to super with a data-structure return value '''
        return self.get_imp().find(Imp.MSG_SEND_SUPER_STRET) != -1
    
    def is_any_msg_send_super(self):
        ''' Check if ImpStub is any objc_msgSendSuper '''
        return self.get_imp().find(Imp.MSG_SEND_SUPER) != -1
    
    def is_any_msg_send(self):
        ''' Check if ImpStub is any objc_msgSend '''
        return self.get_imp().find(Imp.MSG_SEND) != -1
    
    def is_any_msg_send_stret(self):
        ''' Check if ImpStub is any objc_msgSend_stret '''
        return self.is_msg_send_stret() or self.is_msg_send_super_stret()
    
    def is_retain(self):
        ''' Check if ImpStub is retain '''
        return self.get_imp() == Imp.RETAIN
    
    def does_retain(self):
        ''' Check if ImpStub is retaining Object '''
        return self.get_imp() in Imp.RETAIN_FUNCTIONS
    
    def is_release(self):
        ''' Check if ImpStub is release '''
        return self.get_imp() == Imp.RELEASE
    
    def does_release(self):
        ''' Check if the ImpStub is releasing Object (release, autorelease ,...) '''
        return self.get_imp() in (Imp.RELEASE, Imp.AUTORELEASE);
     
    def is_autorelease(self):
        ''' Check if ImpStub is autorelease '''
        return self.get_imp() == Imp.AUTORELEASE
    
    def is_return_important(self):
        ''' Indicate if Imp is important for analyzing the return value of a call (rax = [NSUserDefaults retain])'''
        return self.get_imp().find('objc') != -1 and not self.is_msg_send()
