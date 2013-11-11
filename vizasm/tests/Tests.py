'''
VizAsm

Created on 05.10.2013

@author: Nils Schmidt
'''
from unittest.suite import TestSuite
from vizasm.tests.security.filter.util.MethodDefFilterUtilTests import MethodDefFilterUtilTests
from vizasm.tests.security.filter.util.FunctionFilterUtilTests import FunctionFilterUtilTsts
from vizasm.tests.model.objc.function.Function import FunctionTests

class Tests(TestSuite):
    ''' TestSuite for VizAsm '''
    
    TESTS = [MethodDefFilterUtilTests, FunctionFilterUtilTsts, FunctionTests]
    
    def __init__(self, tests = ()):
        TestSuite.__init__(self, tests = tests)
        self.addTests(self.TESTS)
        
