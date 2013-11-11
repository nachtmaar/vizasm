'''
VizAsm

Created on 17.09.2013

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

from vizasm.analysis.asm.cpu.Resetable import Resetable
from vizasm.analysis.asm.cpu.objcruntime.IVarRefLookup import IVarRefLookup
from vizasm.analysis.asm.cpu.objcruntime.exceptions.ObjcRuntimeCouldNotGetSelector import \
    ObjcRuntimeCouldNotGetSelector
from vizasm.analysis.asm.cpu.objcruntime.exceptions.ObjcRuntimeCouldNotReadMsgSendException import \
    ObjcRuntimeCouldNotReadMsgSendException
from vizasm.analysis.asm.cpu.objcruntime.exceptions.ObjcRuntimeSelectorWrongTypeException import \
    ObjcRuntimeSelectorWrongTypeException
from vizasm.model.asm.ivar.IVar import IVar
from vizasm.model.asm.ivar.IvarRefCouldNotBeResolved import \
    IvarRefCouldNotBeResolvedException
from vizasm.model.asm.ivar.IvarRefWrongTypeException import \
    IvarRefWrongTypeException
from vizasm.model.objc.arguments.Selector import SelectorOverloadedException, \
    SelectorUnderloadedException, Selector
from vizasm.model.objc.function.FunctionInterface import FunctionInterface
from vizasm.model.objc.function.MethodSelectorArgument import \
    MethodSelectorArgument
from vizasm.model.objc.function.MsgSend import MsgSend
from vizasm.model.objc.function.MsgSendInterface import MsgSendInterface
from vizasm.model.objc.object.nsobject.NSObject import NSObject
from vizasm.model.objc.object.nsobject.NSObjectInterface import \
    NSObjectInterface
from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass
from vizasm.util import Util
from vizasm.util.Log import log


METHOD_ARGUMENTS_PREFIX = 'arg'
# destination = 0 means the destination is a reference to a variable (&var)
NOT_INITIALIZED_CLASS = ObjcClass.not_initialized

class ObjectiveCRuntime(object, Resetable):
    '''
    Models the objective-c runtime.
    
    It keeps track of seen instance variables and their values
    and handles calls to super as well as all msgSend stuff
    (objc_msgSend).  
    
    Parameters
    ----------
    _cpu: Cpu
    _ivar_lookup: IVarRefLookup
        Dictionary helper to look up instance variables    
    _superclass_dict: dict<ObjcClass, ObjcClass>, optional (default {})
        dictionary holding the base classes of the classes        
        
    See
    ---
    Implement these:
        create_and_store_method_selector_arguments
        store_self_cmd_for_stack_fetching_cpu
    '''
    
#####################################################################################
# Resetable                                                                         #
#####################################################################################    

    def reset(self):
        ''' Reset the objective-c runtime '''
        self.ivar_lookup.reset()
        
#####################################################################################
# Implementation                                                                    #
#####################################################################################
    
    def __init__(self, cpu, superclass_dict):
        self._cpu = cpu
        self._ivar_lookup = IVarRefLookup()
        
        if superclass_dict is None:
            superclass_dict = {}
        self._superclass_dict = superclass_dict

    def __str__(self):
        return '%s: %s' % (self.__class__.__name__, self.ivar_lookup)
    
    def __repr__(self):
        return '%s: %s\%s' % (self.__class__.__name__, repr(self.ivar_lookup), Util.pretty_format_dict(self.superclass_dict, True))
    
    def get_cpu(self):
        return self._cpu
    
    def set_cpu(self, value):
        self._cpu = value
        
    def get_ivar_lookup(self):
        return self._ivar_lookup

    def set_ivar_lookup(self, value):
        self._ivar_lookup = value
        
    def get_superclass_dict(self):
        return self._superclass_dict

    def set_superclass_dict(self, value):
        self._superclass_dict = value        
        
    cpu = property(get_cpu, set_cpu, None, "_cpu(Cpu)")
    ivar_lookup = property(get_ivar_lookup, set_ivar_lookup, None, "_ivar_lookup(IVarRefLookup) -- Dictionary helper to look up instance variables")    
    superclass_dict = property(get_superclass_dict, set_superclass_dict, None, "_superclass_dict(dict<ObjcClass, ObjcClass>, optional (default {})) -- dictionary holding the base classes of the classes")

#####################################################################################
# Implement them                                                                    #
#####################################################################################

    def create_and_store_method_selector_arguments(self, method_selector):
        '''
        Create and store the arguments for the `method_selector`.
        There will be as many arguments created as the `Selector` needs.
        
        Parameters
        ----------
        method_selector: Selector
            the `Selector` describing the method that is currently being read by the `Cpu`
        
        Raises
        ------
        SelectorOverloadedException
            if selector has more arguments than it needs
        '''
        raise NotImplementedError
    
    def store_self_cmd_for_stack_fetching_cpu(self, objc_class, selector):
        ''' Store self and _cmd in the appropriate place if the
        `Cpu` fetches all of its arguments from stack''' 
    
#####################################################################################
# Implementation                                                                    #
#####################################################################################    

    @staticmethod
    def create_method_selector_arg(number):
        '''
        Create a method argument for the current method selector. See `method_selector`. 
        The method arguments are stored as instance of `MethodSelectorArgument` named with the suffix `Cpu.METHOD_ARGUMENTS_PREFIX`.
        
        Parameters
        ----------
        number: int
            the number to append to the argument name
        
        Returns
        -------
        MethodSelectorArgument
        '''
        objc_class = NSObject('%s%d' % (METHOD_ARGUMENTS_PREFIX, number))
        return MethodSelectorArgument(objc_class)
    
    def set_superclass(self, ivar_ref):
        '''
        Set the superclass for the `ivar_ref` from the `superclass_dict`.
        
        Parameters
        ----------
        ivar_ref: MsgSend
        '''
        # set superclass if available
        if isinstance(ivar_ref, MsgSend):
            objc_class = ivar_ref.msg_receiver
            # TODO: EQUALITY DOES NOT TAKE PLACE, IS STATIC! WHY? THIS IS A TEMPORARY WORKAROUND
            objc_class.is_static = False
            if isinstance(objc_class, ObjcClass):
                superclass = self.superclass_dict.get_from_idx(objc_class)
                if superclass is not None:
                    objc_class.superclass = superclass    
                    
    def read_msg_send(self, imp, destination):
        ''' Read a msg_send and store it .
    
        Raises
        ------
        ObjcRuntimeCouldNotGetSelector
            if the value of the destination register could not be resolved
        ObjcRuntimeSelectorWrongTypeException
            if the selector has not the right class. Has to be: `Selector`
        
        Returns
        -------
        MsgSend
            the `MsgSend` created
        '''
        # resolve superclass
        if imp.is_any_msg_send_super():
            method = self.cpu.method
            if method is not None and method.is_objc_function():
                method_class = method.msg_receiver
                destination = self.superclass_dict.get(method_class)
                # if no superclass has been found, set it to NSObject
                if destination is None:
                    destination = ObjcClass.nsobject
                    
        if imp.is_any_msg_send():
            # deepcopy needed for arm
            # otherwise multiple usage of same selectors leads to the same selector every time
            # and new arguments cannot be filled into an full selector
            selector = deepcopy(self.get_current_selector_check_sel_type(imp.is_any_msg_send_stret()))
            selector.reset()
            # TODO.
            msgSend = self._msgsend_from_selector(selector, destination)
            return msgSend
        return None                    
    
    def _msgsend_from_selector(self, selector, destination):
        ''' Create a MsgSend and store it in the `MethodCall`.
        
        Parameters
        ----------
        selector: Selector
        destination: 
            to which object to send the message
        
        Raises
        ------
        ObjcRuntimeCouldNotReadMsgSendException
            if the msgSend could not be read
            
        Returns
        -------
        MsgSend
            the created `MsgSend`
        '''
        cpu = self.cpu
        try:
            selector.fill_from_cpu(cpu)
        except (SelectorOverloadedException, SelectorUnderloadedException) as e:
            log.exception(e)
        msg_send = self.msg_send_from_destination(destination, selector)
        if msg_send is None:
            raise ObjcRuntimeCouldNotReadMsgSendException(cpu, destination, selector)
        # save MsgSend in return register
        self.cpu._store_function(msg_send)
        return msg_send
        
    def read_selector(self, selector, destination):
        ''' Called is a `Selector`. 
        Create a `MsgSend` and store it in the `MethodCall.
         
        Returns
        -------
        MsgSend
            the created `MsgSend 
        '''
        dest = None
        if selector is not None:
            if isinstance(destination, IVar):
                try:
                    destination.resolve_ivar_ref(self.ivar_lookup)
                except (IvarRefCouldNotBeResolvedException, IvarRefWrongTypeException) as e:
                    log.exception(e)
                    
            if isinstance(destination, FunctionInterface):
                dest = destination
            elif isinstance(destination, NSObjectInterface):
                dest = destination.get_nsobject()
            
            msg_send = self._msgsend_from_selector(selector, dest)
            return msg_send
        return None        

    def msg_send_from_destination(self, destination, selector):
        '''
        Create a MsgSend from the given `destination` and `selector`.
        
        Parameters
        ----------
        selector: Selector
        destination: 
            to which object to send the message

        Returns
        -------
        msg_send: MsgSend
            the created `MsgSend`
        '''
        msg_send = None
        if selector is not None:
            if isinstance(destination, MsgSendInterface) or destination == 0:
                # set 0 to not_initialized
                if isinstance(destination, IVar):
                    if destination.ivar_ref == 0:
                        destination.ivar_ref = MsgSend(NOT_INITIALIZED_CLASS, [])
                # set 0 to not_initialized
                if destination == 0:
                    msg_send = MsgSend(NOT_INITIALIZED_CLASS, [selector])
                else:
                    # ivar_ref_lookup kwarg resolves ivar_ref from IVar 
                    msg_send = destination.create_msg_send(selector, ivar_ref_lookup = self.ivar_lookup)
        return msg_send

    def read_return_important_objc_call(self, imp, destination, return_register):
        ''' Read a line which seems to return something and store it in the return register. 
        
        Returns
        -------
        is return important
        '''
        is_return_important = imp.is_return_important()
        if is_return_important:
            log.debug('%s = %s', return_register, destination)
            self.cpu.memory.registers.set_value_for_register(return_register, destination)        
        return is_return_important    
    
    def _get_current_selector(self, objc_msgSend_stret, raise_cpu_selector_wrong_type_exception = False):
        ''' Return the current selector.
        If the `Cpu` fetches its arguments from stack, it will be popped from the stack. 
        
        Parameters
        ----------
        raise_cpu_selector_wrong_type_exception: bool
            raise ObjcRuntimeSelectorWrongTypeException if this exceptions occurrs but only if the bool is True
            
        Raises
        ------
        ObjcRuntimeCouldNotGetSelector
            raised if the value of the selector register could not be detected
        ObjcRuntimeSelectorWrongTypeException
            raised if the type of selector is not Selector but only if raise_cpu_selector_wrong_type_exception
        
        Returns
        -------
        Selector
        ''' 
        cpu = self.cpu
        selector_reg = cpu.selector_register()
        if objc_msgSend_stret:
            selector_reg = cpu.next_reg_for_spret(selector_reg)
        selector = self.cpu.memory.get_argument(selector_reg)
        if selector is not None:
            if isinstance(selector, Selector):
                return selector
            elif raise_cpu_selector_wrong_type_exception:
                raise ObjcRuntimeSelectorWrongTypeException(self, selector)
            return selector
        raise ObjcRuntimeCouldNotGetSelector(cpu)    
    
    def get_current_selector_check_sel_type(self, objc_msgSend_stret = False):
        ''' Return the current selector and check the type of the selector.
        If not correct, raise ObjcRuntimeSelectorWrongTypeException.
        
        Parameters
        ----------
        objc_msgSend_stret: bool, optional (default is False)
            indicate an objc_msgSend_stret
            
        Raises
        ------
        ObjcRuntimeCouldNotGetSelector
            raised if the value of the selector register could not be detected
        ObjcRuntimeSelectorWrongTypeException
            raised if the type of selector is not Selector
            
        Returns
        -------
        selector: Selector
            The selector currently stored in the register specified by `selector_registers`.
        '''
        return self._get_current_selector(objc_msgSend_stret, raise_cpu_selector_wrong_type_exception = True)

