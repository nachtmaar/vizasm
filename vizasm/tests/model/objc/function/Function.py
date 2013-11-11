'''
VizAsm

Created on 19.10.2013

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

from vizasm.model.objc.arguments.Selector import Selector
from vizasm.model.objc.function.Function import Function
from vizasm.model.objc.function.MethodImplementation import MethodImplementation
from vizasm.model.objc.function.MsgSend import MsgSend
from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass


class FunctionTests(TestCase):
    
    def test_function_eq(self):
        func_name = 'cFunction'
        cfunc_impl = Function(func_name, ['int', 'int', 'int'])
        cfunc1 = Function(func_name, [1, 2, 3])
        res = cfunc1 == cfunc_impl and hash(cfunc1) == hash(cfunc_impl)
        res2 = cfunc_impl == cfunc1
        self.assertTrue(res and res2, 'The equality of Function and CFuncImpl is not working properly!')
        
    def test_msg_send_eq(self):
        objc_class = ObjcClass('Foo')
        sels = [Selector('alloc'), Selector('init'), Selector('foo:', ['1'])]
        sels2 = [Selector('foo:', ['1'])]
        msg_send1 = MsgSend(objc_class, sels)
        msg_send2 = MethodImplementation(objc_class, sels2)
        res = msg_send1 == msg_send2 and msg_send2 == msg_send1
        print '%s == %s and vice versa = %s' % (msg_send1, msg_send2, res)
        self.assertTrue(res, 'Node quality not correct! Method calls will not link to the corresponding method implementations and vice versa\n')

