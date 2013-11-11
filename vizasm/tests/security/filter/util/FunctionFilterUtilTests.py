'''
VizAsm

Created on 04.10.2013

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

from vizasm.analysis.security.filter.util import *
from vizasm.model.objc.function.Function import Function
from vizasm.model.objc.function.MsgSend import MsgSend


class FunctionFilterUtilTsts(TestCase):
    ''' Tests for the `FunctionFilterUtil` '''
            
    
    def test_mc_sel_via_nsselector_from_string(self):
        ''' Test the `mc_sel_via_nsselector_from_string` function '''
        sel_to_load = 'setAllowsAnyHTTPSCertificate:forHost'
        function = Function('NSSelectorFromString', [NSString(sel_to_load)])
        res = mc_sel_via_nsselector_from_string(function, 'setAllowsAnyHTTPSCertificate')
        print '%s loads selector: %s = %s' % (function, sel_to_load, res) 
        self.assertTrue(res, 'The method `mc_sel_via_nsselector_from_string` is not working properly!')
        
    def test_filter_function(self):
        ''' Test the `mc_filter_function` method '''
        func = lambda x: str(x) == '@"foo"'
        c_func = MsgSend(ObjcClass('Bla'), [Selector('foo:', [NSString('foo')])]) 
        msgsend = MsgSend(ObjcClass('SomeClass'), [Selector('someSelector:2dnarg:3rdarg:', [c_func, NSString('SomeString'), NSString('bar')])])
        check_method_correct_working = mc_filter_method_call(msgsend, [func], steps = 3)
        self.assertTrue(check_method_correct_working, 'The method `mc_filter_function` is not working properly!')
    
    def test_contains_imp_got(self):
        ''' Test the `mc_contains_imp_got` method '''
        imp_got_to_search = 'NSStreamSocketSecurityLevelNone'
        args = [ImpGot(imp_got_to_search), ImpGot('NSStreamSocketSecurityLevel')]
        msg_send = MsgSend(ObjcClass("NSOutputStream"), [Selector('setProperty:forKey:', arguments = args)])
        res = mc_contains_imp_got(msg_send, imp_got_to_search)
        print '%s\n has %s: %s' % (msg_send, imp_got_to_search, res)
        
        imp_got_to_search = 'kSBXProfileNoWrite'
        c_func = Function('sandbox_init', func_arguments = [ImpGot('kSBXProfileNoWrite')])
        res2 = mc_contains_imp_got(c_func, imp_got_to_search)
        print '%s\n has %s: %s' % (c_func, imp_got_to_search, res)
        
        self.assertTrue(res and res2, 'Method `mc_contains_imp_got` not working properly!')
    
    def test_is_exploitable_log_func(self):
        ''' Test the method `mc_is_exploitable_log_func` '''
        msg_send = MsgSend(ObjcClass('NSString'), [Selector('stringWithFormat:', [MethodSelectorArgument('arg1')])])
        exploitable_func = Function('NSLog', [msg_send])
        res = mc_is_exploitable_log_func(exploitable_func)
        print 'is exploitable: %s = %s' % (exploitable_func, res)
        
        exploitable_printf = Function('printf', [StackVar('var_216')])
        res2 = mc_is_exploitable_log_func(exploitable_printf)
        print 'is exploitable: %s = %s' % (exploitable_printf, res2)
        
        exploitable_printf2 = Function('printf', [MethodSelectorArgument('arg1')])
        res3 = mc_is_exploitable_log_func(exploitable_printf2)
        print 'is exploitable: %s = %s' % (exploitable_printf2, res3)
        
        self.assertTrue(all((res, res2, res3)), 'The method `mc_is_exploitable_log_func` is not working properly!')
    
    def test_has_any_selector(self):
        ''' Test the method `mc_has_any_selector` '''
        sel_name = 'format'
        msg_send = MsgSend(ObjcClass('NSString'), [Selector('stringWithFormat:', [FormatString('@"%@", @"foo"')])])

        res = mc_has_any_selector(msg_send, [sel_name], search_substring = True)
        print '%s has selector "%s" = %s' % (msg_send, sel_name, res)
        
        # [[UIApplication sharedApplication] beginBackgroundTaskWithExpirationHandler:]
        sel = 'beginBackgroundTaskWithExpirationHandler:'
        msg_send2 = MsgSend(ObjcClass('UIApplication'), [Selector('sharedApplication'), Selector(sel)])
        res2 = mc_has_any_selector(msg_send2, [sel], search_substring = False)
        self.assertTrue(res and res2 , 'The method `mc_has_any_selector` is not working properly!')
        
        
