'''
VizAsm

Created on 14.09.2013

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

from vizasm.analysis.asm.cpu.AsmRegEx import AsmRegEx
from vizasm.model.objc.AsmParserInterface import AsmParserInterface
from vizasm.model.objc.function.MsgSend import MsgSend
from vizasm.model.objc.object.nsobject.objcclass.CategoryClass import \
    CategoryClass
from vizasm.model.objc.arguments.Selector import Selector
    
class MethodImplementation(MsgSend, AsmParserInterface):
    ''' Represents a method implementation (normal objective-C Method or category) '''
    
    def __str__(self):
        return '%s%s' % (self.__static_str() , self.unfilled_args_name())
    
    def __static_str(self):
        is_static = self.is_static
        return '+' if is_static else '-'

######################################################################################
# AsmParserInterface                                                                 #
######################################################################################
    @staticmethod
    def create_from_asm_line(asmline):
        ''' Create a `MethodImplementation` from an assembler line like e.g " +[NSURLRequest(AnyHttpsCert) allowsAnyHTTPSCertificateForHost:]_100002120:" 
            Returns a `MethodImplementation` where the class is a `CategoryClass`.
        '''
        msg_send = None
        category_match = AsmRegEx.compiled_vre(AsmRegEx.RE_CATEGORY).search(asmline)
        if category_match is not None:
            category_on_class = category_match.group(AsmRegEx.RE_CATEGORY_ON_CLASS)
            classname = category_match.group(AsmRegEx.RE_CATEGORY_CLASS)
            category_is_static = category_match.group(AsmRegEx.RE_CATEGORY_STATIC_SYMBOL) == AsmRegEx.RE_CATEGORY_SYMBOL_STATIC
            selectorname = category_match.group(AsmRegEx.RE_CATEGORY_SELECTOR)
            selector = Selector(selectorname)
            cclass = CategoryClass(classname, category_on_class)
            msg_send = MethodImplementation(cclass, [selector], is_static = category_is_static)
        return msg_send
        
if __name__ == '__main__':
    from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass
    method = MethodImplementation(ObjcClass('AppDelegate'), [Selector('applicationDidFinishLaunching:')], is_static = False)
    print method
    
    category_msg_send = MethodImplementation.create_from_asm_line(' +[NSURLRequest(AnyHttpsCert) allowsAnyHTTPSCertificateForHost:]_100001c70:')
    print 'MsgSend from category: %s ' % (category_msg_send)

