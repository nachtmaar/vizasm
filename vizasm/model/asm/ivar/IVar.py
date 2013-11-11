'''
VizAsm

Created on 10.04.2013

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

from vizasm.model.asm.ivar.IvarRefCouldNotBeResolved import \
    IvarRefCouldNotBeResolvedException
from vizasm.model.asm.ivar.IvarRefWrongTypeException import \
    IvarRefWrongTypeException
from vizasm.model.objc.function.MsgSend import MsgSend
from vizasm.model.objc.function.MsgSendInterface import MsgSendInterface
from vizasm.model.objc.object.nsobject.NSObjectInterface import \
    NSObjectInterface
from vizasm.util.Log import log

class IVar(object, NSObjectInterface, MsgSendInterface):
    ''' 
    Represents an ivar (instance variable) e.g. created out of this asmline: "[ds:_OBJC_IVAR_$_AppDelegate.obj3]"
     
    where obj3 is the variable of the ObjcClass AppDelegate
     
    which points to a MsgSend like [[Object3 alloc] init]

    Parameters
    ----------
    __ivar_class: ObjcClass
        ObjcClass e.g. created from "[ds:_OBJC_IVAR_$_AppDelegate.obj3]"
    __ivar_ref: MsgSend, optional (default is None)
        the MsgSend where the ivar points to
    '''
    
    def __init__(self, ivar_class, ivar_ref = None):
        self.__ivar_class = ivar_class
        self.__ivar_ref = ivar_ref
    
    def __str__(self):
        ivar_ref = self.get_ivar_ref()
        if ivar_ref is None:
            return self.get_ivar_class().__str__()
        else:
            return ivar_ref.__str__()
    
    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.ivar_class, self.ivar_ref)
    
    def __hash__(self):
        return hash((self.get_ivar_class(), self.get_ivar_ref()))
    
    def __eq__(self, other):
        if isinstance(other, IVar):
            return self is other or (self.get_ivar_class(), self.get_ivar_ref()) == (other.get_ivar_class(), other.get_ivar_ref())
        return False
    
    def __ne__(self, other):
        return not self == other
    
    def get_ivar_class(self):
        return self.__ivar_class

    def get_ivar_ref(self):
        ''' Get the `ivar_ref`.
        You might want to call resolve_ivar_ref() before to resolve it.''' 
        return self.__ivar_ref

    def set_ivar_class(self, value):
        self.__ivar_class = value

    def set_ivar_ref(self, value):
        self.__ivar_ref = value
    
    ivar_class = property(get_ivar_class, set_ivar_class, None, '__ivar_class(ObjcClass) -- ObjcClass e.g. create from "[ds:_OBJC_IVAR_$_AppDelegate.obj3]"')
    ivar_ref = property(get_ivar_ref, set_ivar_ref, None, "__ivar_ref(MsgSend) -- the MsgSend where the ivar points to")
    
    def create_ivar_lookup_entry(self, ivar_ref_lookup):
        r"""
        Create a lookup entry in the `IVarLookup` using ivar_class as key and ivar_ref as value.
        If `ivar_ref` is None, no entry will be created. 
        
        Parameters
        ----------
        ivar_ref_lookup: IVarRefLookup
            the class where the `ivar_ref` will be stored
        
        Returns
        -------
        True
            if the entry could be created
        False
            if the entry could not be created because the ivar_ref was not available
        """
        ivar_ref = self.get_ivar_ref() 
        if isinstance(ivar_ref, MsgSend):
            ivar_ref_lookup.set_ivar_ref(self.get_ivar_class(), ivar_ref)
            return True
        return False    
    
    def resolve_ivar_ref(self, ivar_ref_lookup):
        r"""
        Resolve the ivar_ref from `ivar_ref_look` and set it.
        The value can be obtained via get_ivar_ref() if no exception occurred.
        
        Parameters
        ----------
        ivar_ref_lookup: IVarRefLookup
            the class where the ivar_ref is stored
        
        Raises
        ------
        IvarRefWrongTypeException
            if the ivar_ref could not be resolved to the correct type (should be MsgSend)
        IvarRefCouldNotBeResolvedException
            if the ivar_ref could not be resolved at all
        """
        ivar_ref = ivar_ref_lookup.get_ivar_ref(self.get_ivar_class()) 
        if ivar_ref is not None:
            if isinstance(ivar_ref, MsgSend):
                self.set_ivar_ref(ivar_ref)
            else:
                raise IvarRefWrongTypeException(self, ivar_ref)
        else:
            raise IvarRefCouldNotBeResolvedException(self, ivar_ref_lookup)
        
#####################################################################################
# NSObjectInterface                                                                 #
#####################################################################################
    def get_nsobject(self):
        ivar_ref = self.get_ivar_ref()
        if ivar_ref is not None:
            return ivar_ref.get_nsobject()
        else:
            return self.get_ivar_class()
        
#####################################################################################
# MsgSendInterface                                                                  #
#####################################################################################    
    def create_msg_send(self, selector, ivar_ref_lookup = None, *args, **kwargs):
        ''' Create a `MsgSend` with the specified `selector`.
        If the `ivar_ref` is not None, this will be used for the `MsgSend`.
        Otherwise the `ivar_class` is used.
        
        Parameters
        ----------
        selector: Selector
            the `Selector` with which the `MsgSend` shall be created.
        ivar_ref_lookup: IVarRefLookup, optional
            if given, the ivar_ref will be resolved
        Returns
        -------
        MsgSend
            the created `MsgSend` with `ivar_ref`  or `ivar_class`  
        ''' 
        # ivar_ref_lookup = kwargs.get('ivar_ref_lookup')
        if ivar_ref_lookup is not None:
            try:
                self.resolve_ivar_ref(ivar_ref_lookup)
            except (IvarRefCouldNotBeResolvedException, IvarRefWrongTypeException) as e:
                log.exception(e)
        ivar_ref = self.get_ivar_ref()
        if ivar_ref is not None:
            return MsgSend.create_from_msgsend(ivar_ref, selector)
        else:
            return MsgSend(self.get_ivar_class(), [selector])
