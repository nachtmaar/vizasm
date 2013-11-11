'''
VizAsm

Created on 05.10.2013

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

from unittest import TestCase

from vizasm.analysis.security.filter.util.MethodDefFilterUtil import \
    md_filter_method_defintion, md_filter_category, md_is_category, \
    md_is_static_category_method
from vizasm.model.ModelUtil import is_method_implementation
from vizasm.model.objc.arguments.Selector import Selector
from vizasm.model.objc.function.MethodImplementation import MethodImplementation
from vizasm.model.objc.function.MsgSend import MsgSend
from vizasm.model.objc.object.nsobject.objcclass.CategoryClass import \
    CategoryClass
from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass


class MethodDefFilterUtilTests(TestCase):
    ''' Tests for the `MethodDefFilterUtil` '''
    
    MSG = 'The `%s` method is not working properly !'    
    
    def get_category_class(self):
        return self.__category_class

    def set_category_class(self, value):
        self.__category_class = value

    def get_category(self):
        return self.__category

    def set_category(self, value):
        self.__category = value

    def setUp(self):
        TestCase.setUp(self)
        
        self.__category_class = CategoryClass('AnyHttpsCert', ObjcClass('NSURLRequest'))
        self.__category = MethodImplementation(self.category_class, [Selector('allowsAnyHTTPSCertificateForHost:')], is_static = True)
    
    def test_filter_method_definition(self):
        ''' Test `md_filter_method_defintion` '''
        selname = 'application:handleOpenURL:'
        sel = Selector(selname)
        msg_send = MsgSend(ObjcClass('AppDelegate'), [sel])
        res = md_filter_method_defintion(msg_send, class_name = None, selector_name = selname, search_substring = True)
        print '%s has selector %s = %s' % (msg_send, sel, res)
        self.assertTrue(res, self.MSG % 'MethodDefFilterUtil')
        
    def test_filter_category(self):
        ''' Tests for the method `md_filter_category` '''
        category_on_class_name = 'NSURLRequest'
        category_on_class = ObjcClass(category_on_class_name)
        category_name = 'AnyHttpsCert'
        cclass = CategoryClass(category_name, category_on_class = category_on_class)
        selector = Selector('allowsAnyHTTPSCertificateForHost')
        category_msg_send = MsgSend(cclass, [selector])
        
        # test with all properties at once
        category_match = md_filter_category(category_msg_send, str(selector), category_on_class_name, category_name, search_substring = False) 
        print '%s is category on %s with name %s and selector %s = %s' % (category_msg_send, category_on_class_name, category_name, selector, category_match)
        
        category_match2 = md_filter_category(category_msg_send, str(selector), category_on_class_name, category_name = None, search_substring = False) 
        print '%s is category on %s and selector %s = %s' % (category_msg_send, category_on_class_name, selector, category_match2)
        
        # category_on test
        category_match3 = md_filter_category(category_msg_send, category_on = category_on_class_name) 
        print '%s is category on %s = %s' % (category_msg_send, category_on_class_name, category_match3)
        
        # category name test
        category_match4 = md_filter_category(category_msg_send, category_name = category_name) 
        print '%s is category with name %s = %s' % (category_msg_send, category_name, category_match4)
        
        # selector test
        category_match5 = md_filter_category(category_msg_send, selector = str(selector)) 
        print '%s is category with selector %s = %s' % (category_msg_send, str(selector), category_match5)
        
        self.assertTrue(all((category_match, category_match2, category_match3, category_match4, category_match5)), self.MSG % 'md_filter_category')
        
    def test_is_category(self):
        ''' Test the `md_is_category` method '''
        res = md_is_category(self.category)
        print '%s is category = %s' % (self.category, res)
        self.assertTrue(res, self.MSG % 'md_is_category')
        
    def test_is_static_category_method(self):
        ''' Test the `md_is_static_category_method' method '''
        MSG = self.MSG % 'md_is_static_category_method'
        
        # static category
        res = md_is_category(self.category)
        print '%s is static category = %s' % (self.category, res)
        self.assertTrue(res, MSG)
        
        # not static category
        self.category.is_static = False
        res = md_is_static_category_method(self.category)
        print '%s is static category = %s' % (self.category, res)
        self.assertFalse(res, MSG)
        
    def test_is_method_implementation(self):
        ''' Test the `is_method_implementation` method '''
        self.assertTrue(is_method_implementation(self.category), self.MSG % 'is_method_implementation')
                        
    category = property(get_category, set_category, None, None)
    category_class = property(get_category_class, set_category_class, None, None)
        
        
