'''
VizAsm

Created on 01.04.2013

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

from copy import deepcopy

from vizasm.model.objc.arguments.Selector import Selector
from vizasm.model.objc.function.FunctionInterface import FunctionInterface
from vizasm.model.objc.function.MsgSendInterface import MsgSendInterface
from vizasm.model.objc.object.nsobject.NSObjectInterface import \
    NSObjectInterface
from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass

class MsgSend(FunctionInterface, NSObjectInterface, MsgSendInterface):
    ''' 
    Represents a MsgSend in objective-c like e.g. [NSUserDefaults standardUserdefaults]
    or [[[NSUserDefaults standardUserDefaults] objectForKey:aKey] setValueForKey:aKey value:value]
    
    Alloc init stuff like [[Object3 alloc] init] or [[Object3] new] is reformatted to Object3*.
    
    Parameters
    ----------
    __msg_receiver: FunctionInterface
        the class to which the message(s) will be sent
    __selectors: list<Selector>
        the selector(s) to send to the class (default [])
    '''
    
    def __init__(self, msg_send_class, selectors = None, is_static = False):
        FunctionInterface.__init__(self, is_static)
        if selectors is None:
            selectors = []
        self.__selectors = selectors
        self.__msg_receiver = msg_send_class
        
    def __hash__(self):
        selectors = self.__unfilled_selector_names_for_eq()
        return hash((self.get_msg_receiver(), tuple(selectors)))
    
    def __eq__(self, other):
        if isinstance(other, MsgSend):
            # Networkx node equality. Let method calls link to corresponding method implementations and vice versa\n
            # achieve "-[MainClass selfMethod:]"  == "[MainClass selfMethod:n/a]" == "[MainClass selfMethod:5]"
            s_sels, o_sels = self.__unfilled_selector_names_for_eq(), other.__unfilled_selector_names_for_eq()
            return self is other or ((self.get_msg_receiver(), tuple(s_sels))) == ((other.get_msg_receiver(), tuple(o_sels)))
        return False
    
    def __ne__(self, other):
        return not self == other    
    
    def __str__(self):
        res = self.get_msg_receiver().__str__()
        if len(self.get_selectors()) is 0:
            return '[%s n/a]' % (res)
        selectors = self.get_selectors()
        if self.has_init():
            # leave alloc and init or new out
            selectors = self.selectors_without_init()
            res = '%s*' % (res)
        for sel in selectors:
            try:
                res = '[%s %s]' % (res, sel)
            except RuntimeError:
                res = '[%s %s]' % (res, sel.get_obj_name())
        return res
    
    def __repr__(self):
        return '%s(%s: %s, %s)' % (self.__class__.__name__, self.get_msg_receiver().__repr__(), self.get_selectors().__repr__(), self.is_static)
    
    def __iter__(self):
        ''' Return an iterator over the `Selector`s '''
        return iter(self.selectors)
    
    def __unfilled_selector_names_for_eq(self):
        ''' Return the unfilled selector names and leave alloc and init or new out'''
        return [sel.selector_name for sel in self.selectors_without_init()]
    
    def unfilled_args_name(self):
        ''' Get a string representation without filling the `Selector` with its arguments '''
        res = str(self.get_msg_receiver())
        for sel in self.selectors:
            res = '[%s %s]' % (res, sel.selector_name)
        return res
    
    @staticmethod
    def create_from_msgsend(msg_send, selector):
        ''' Create a MsgSend from existing MsgSend.
        This method makes a deep copy of the parameters `msg_send` and `selector`.
        
        Parameters
        ----------
        msg_send: MsgSend
        selector: Selector
         
        Returns:
        MsgSend
            `MsgSend` created from the parameters
        '''
        if isinstance(msg_send, MsgSend):
            receiver = deepcopy(msg_send.get_msg_receiver())
            selectors = deepcopy(msg_send.get_selectors())
            selectors.append(selector)   
            return MsgSend(receiver, selectors)
        return None
    
    def get_selectors(self):
        return self.__selectors

    def set_selectors(self, value):
        self.__selectors = value
        
    def get_class(self):
        return self.get_objc_name()
    
    def get_msg_receiver(self):
        return self.__msg_receiver

    def set_msg_receiver(self, value):
        self.__msg_receiver = value
    
    def get_first_selector(self):
        ''' Returns the first selector. None if not exisiting. '''
        selectors = self.get_selectors()
        if selectors:
            return selectors[0]
        
    def __selector_contains_same_msgsend(self, selector):
        ''' Return if the selector has a MsgSend as an argument that has the same ObjcClass '''    
        for arg in selector.get_arguments():
            if isinstance(arg, MsgSend) and isinstance(arg.get_msg_receiver(), ObjcClass) and arg.get_msg_receiver() == self.get_msg_receiver():
                return True
        return False
    
    def fst_selector(self):
        ''' Returns the first selector. None if not available '''
        selectors = self.get_selectors()
        if selectors:
            return selectors[0]
    
    def fst_sel_is_alloc(self):
        ''' Check if the first selector is alloc '''
        selectors = self.get_selectors()
        if selectors:
            return selectors[0].is_alloc()

    def fst_sel_is_new(self):
        ''' Check if the first selector is new '''
        selectors = self.get_selectors()
        if selectors:
            return selectors[0].is_new()
        
    def fst_sel_does_retain(self):
        ''' Check if the first selector increments the retain count '''
        selector = self.fst_selector()
        if selector is not None:
            return selector.does_retain()
        return False
    
    def lst_sel_does_retain(self):
        ''' Check if the first selector increments the retain count '''
        selectors = self.selectors
        length = len(selectors)
        if length > 0:
            return selectors[length - 1].does_retain()
        return False
    
    def fst_sel_does_release(self):
        ''' Check if the first selector decrements the retain count '''
        selector = self.fst_selector()
        if selector is not None:
            return selector.does_release()
        return False
    
    def lst_sel_does_release(self):
        ''' Check if the last selector decrements the retain count '''
        selectors = self.selectors
        length = len(selectors)
        if length > 0:
            return selectors[length - 1].does_release()
        return False
    
    def cnt_init_selectors(self):
        ''' Return the number of init selectors.
            Returns:
                0 -- no init selectors
                1 -- selector is new
                2 -- selectors are alloc and init
        ''' 
        selectors = self.get_selectors()
        if len(selectors) > 1:
            if selectors[0].is_alloc() and selectors[1].is_init():
                return 2
        if len(selectors) > 0 :
            if selectors[0].is_new():
                return 1
        return 0
    
    def has_init(self):
        ''' Return if the first so selectors are alloc and init (order is important!) or new'''
        return self.cnt_init_selectors() > 0
    
    def selectors_without_init(self):
        '''
        Return the selectors without any init selectors.
        See  `cnt_init_selectors()`.
        
        Returns
        -------
        list<Selector>
        '''
        sels = self.selectors
        if self.has_init():
            sels = sels[self.cnt_init_selectors():]
        return sels
    
    
#####################################################################################
# FunctionInterface                                                                 #
#####################################################################################    

    def get_arguments(self):
        return self.get_selectors()

    def get_function_name(self):
        return self.__str__()

    def is_c_function(self):
        return FunctionInterface.is_c_function(self)

    def is_objc_function(self):
        return True

    def cnt_needs_arguments(self):
        res = 0
        for sel in self.get_selectors():
            res += sel.cnt_needs_arguments()
        return res

    def cnt_has_arguments(self):
        res = 0
        for sel in self.get_selectors():
            res += sel.cnt_has_arguments()
        return res

#####################################################################################
# NSObjectInterface                                                                 #
#####################################################################################
    def get_nsobject(self):
        return self.get_msg_receiver()
    
#####################################################################################
# MsgSendInterface                                                                  #
#####################################################################################    
    def create_msg_send(self, selector, *args, **kwargs):
        ''' Create a `MsgSend` with the specified `selector`.
        
        Parameters
        ----------
        selector: Selector
            the `Selector` with which the `MsgSend` shall be created.
            
        Returns
        -------
        MsgSend
            the created `MsgSend` 
        ''' 
        return MsgSend.create_from_msgsend(self, selector)
        
    selectors = property(get_selectors, set_selectors, None, "__selectors(list) -- the selector(s) to send to the class (default [])")
    msg_receiver = property(get_msg_receiver, set_msg_receiver, None, "__msg_receiver(ObjClass) -- the class to which the message(s) will be sent")
        
if __name__ == '__main__':
    from vizasm.model.objc.function.MethodImplementation import MethodImplementation

    objcclass = ObjcClass('NSUserDefaults')
    sel1 = Selector('standardUserDefaults')
    sel2 = Selector('objectForKey:', ['aKey'])
    sel3 = Selector('setValueForKey:value:', ['aKey', 'value'])
    msg = MsgSend(objcclass, [sel1, sel2, sel3]) 
    print msg   
    msg2 = MsgSend(objcclass, [Selector('alloc'), Selector('init'), Selector('httpsConnection')])
    print msg2   
    msg2 = MsgSend(objcclass, [Selector('new'), Selector('httpsConnection')])
    print msg2   
    msg4 = MsgSend(objcclass, [Selector('alloc'), Selector('init')])
    print msg4
     
    msg3 = MsgSend.create_from_msgsend(msg, sel1)
    print msg3
