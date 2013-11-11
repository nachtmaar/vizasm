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

from copy import deepcopy

from vizasm.Settings import setting_for_key, SETTINGS_CNT_SURROUNDING_LINES
from vizasm.model.objc.function.MsgSend import MsgSend
from vizasm.model.objc.methodcall.MethodCallItem import MethodCallItem
from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass
from vizasm.util import Util
from vizasm.vizasm_networkx import NodeAttributes
from vizasm.vizasm_networkx.AddMethodCallToGraphInterface import \
    AddMethodCallToGraphInterface

class MethodCall(object, AddMethodCallToGraphInterface):
    ''' 
    The `Methodcall` stores messages a sender has sent.
    This model is uses for a method (sender) that sends several messages and is the output of the `Cpu`.

    If the sender is not present at creation, using None as argument for the sender creates a pseudo none sender. 
    You can check if this sender is still present with the method has_no_sender().
    
    Parameters
    ----------
    __sender: FunctionInterface, optional (default is PSEUDO_NONE_SENDER)
    __calls: list<MethodCallItem>, optional (default is [])
    '''
    
    PSEUDO_NONE_NAME = 'pseudo none'
    PSEUDO_NONE_SENDER = MsgSend(ObjcClass(PSEUDO_NONE_NAME), [])
    
    def __init__(self, sender = None, calls = None):
        object.__init__(self)
        if calls is None:
            calls = []
        # fix for creation with None as sender
        if sender is None:
            sender = MethodCall.PSEUDO_NONE_SENDER
        self.__sender = sender
        self.__calls = calls

    def __len__(self):
        return len(self.get_calls())

    def __eq__(self, other): 
        if isinstance(other, MethodCall):
            return self is other or ((self.get_sender(), self.get_calls())) == ((other.sender(), other.get_msg()))   
        return False
    
    def __ne__(self, other):
        return not self == other
    
    def __hash__(self):
        return hash((self.get_sender().__hash__(), tuple(self.get_calls()).__hash__()))
    
    def __iter__(self):
        return iter(sorted(self.calls))
    
    def format_head(self):
        ''' Format the head (first line) of the `MethodCall`.
        No newline will be appended.
        '''
        return 'Method: %s' % (self.get_sender())
        
    def __str__(self):
        head = self.format_head()
        return '%s:\n%s\n%s' % (head, (len(head) + 1) * '-', ''.join(str(call) for call in self))
    
    def __repr__(self):
        return '%s(%s: %s)' % (self.__class__.__name__, self.get_sender(), self.get_calls())
    
    def get_sender(self):
        return self.__sender

    def get_calls(self):
        return self.__calls

    def set_sender(self, value):
        self.__sender = value

    def set_calls(self, value):
        self.__calls = value
        
    sender = property(get_sender, set_sender, None, "__sender(MsgSend, optional (default is PSEUDO_NONE_SENDER))")
    calls = property(get_calls, set_calls, None, "__calls:(list<MethodCallItem>, optional (default is []))")

    def add_methodcall(self, call, linenr, address = None):
        ''' Add a call.
        
        Parameters:
        -----------
        call: Function or MsgSend
        linenr: int
        address: int
        '''
        self.add_methodcallitem(MethodCallItem(call, linenr, address)) 
        
    def add_methodcallitem(self, methodcallitem):
        ''' Add the `MethodCallItem`.
        
        Parameters:
        -----------
        methodcallitem: MethodCallItem
            the `MethodCallItem` which shall be added
        '''
        self.get_calls().append(methodcallitem) 

    def idx_methodcallitem(self, linenr):
        ''' Return the index of the `MethodCallItem` with the given line number'''
        for i, methocallitem in enumerate(self.calls):
            if methocallitem.linenr == linenr:
                return i
        return None
                    
    def has_no_sender(self):
        ''' Check if the `Methodcall` has a sender. 
        If the `MethodCall` is initialized with None as sender, a pseudo none sender is created and used.
        ''' 
        return self.get_sender() == MethodCall.PSEUDO_NONE_SENDER
    
    def is_empty(self):
        ''' Returns if the methodcall does not contain any calls '''
        return len(self.get_calls()) == 0

    def create_gephi_attr_dicts(self, asm_lines, filtered_methodcall = None):    
        '''
        Construct the attribute dictionary describing the graph style.
        Use the created dictionaries with the `add_to_graph` method.
        
        The attributes are:
        Calling Method:
            assembler code
            the method calls (filtered or not)
        Method:
            line number in the asm file
            address in the asm file
            surrounding lines
            
        Parameters
        ----------
        asm_lines: string
            the assembler method as string
        filtered_methodcall: MethodCall, optional (default is None)
            the filtered `MethodCall`
        
        Returns
        -------
        methodcall_sender_attr_dict: dict
        methodcall_calls_attr_list_dict: dict
        '''
        method_lines_list = [str(methodcallitem) for methodcallitem in self.calls]

        if filtered_methodcall is None:
            filtered_methodcall = self
            
        # construct calls attribute dictionary
        methodcall_calls_attr_list_dict = []
        cnt_surrounding_lines = setting_for_key(SETTINGS_CNT_SURROUNDING_LINES)
        if cnt_surrounding_lines >= 0:
            for i, methodcallitem in enumerate(filtered_methodcall.calls):
                # construct leading and trailing lines
                # index of the current line (filtered `MethodCall`) in the list of method lines 
                current_line = str(filtered_methodcall.calls[i].call)
                linenr = methodcallitem.linenr
                idx_line = self.idx_methodcallitem(linenr)
                # idx_line = method_lines_list.index(current_line)
                lines_before, lines_after = Util.surrounding_elements_from_list(method_lines_list, idx_line, cnt_surrounding_lines)
                
                surrounding_lines = NodeAttributes.NPATTERN_SURROUND_LINES % (Util.strlist_to_str(lines_before), current_line, Util.strlist_to_str(lines_after))
                methodcall_attr_dict = {NodeAttributes.NATTR_METHOD_SURROUNDING_LINES % cnt_surrounding_lines : surrounding_lines}
                
                methodcall_attr_dict.update(methodcallitem.get_gexf_viz_attr_dict())
                
                methodcall_calls_attr_list_dict.append(methodcall_attr_dict)
        
        # add method signature to list of method lines 
        method_lines_list.insert(0, filtered_methodcall.format_head() + ":\n")
        
        # construct sender attribute dictionary
        method_lines = Util.strlist_to_str(method_lines_list)
        methodcall_sender_attr_dict = {NodeAttributes.NATTR_METHOD : method_lines, NodeAttributes.NATTR_ASM_CODE : asm_lines}
        
        return (methodcall_sender_attr_dict, methodcall_calls_attr_list_dict)
   
#####################################################################################
# AddToGraphInterface                                                               #
#####################################################################################
    
    def add_to_graph(self, graph, methodcall_sender_attr_dict = None, methodcall_calls_attr_list_dict = None, sender_methodcall_edge_attr_dict = None):
        ''' Add the `MethodCall` to the graph
        
        Parameters
        ----------
        methodcall_sender_attr_dict: dict, optional (Default {})
        methodcall_calls_attr_list_dict: dict, optional (Default {})
        methodcall_calls_attr_list_dict: dict, optional (Default {})
         '''
        
        if methodcall_sender_attr_dict is None:
            methodcall_sender_attr_dict = {}
        if methodcall_calls_attr_list_dict is None:
            methodcall_calls_attr_list_dict = []
        if sender_methodcall_edge_attr_dict is None:
            sender_methodcall_edge_attr_dict = {}
            
        if len(self) > 0:
            key = self.sender
            graph.add_node(key)
            graph.add_attributes(key, methodcall_sender_attr_dict)
            for idx, methodcallitem in enumerate(self):
                # only set the next attribute dictionary if list is not empty
                if methodcall_calls_attr_list_dict:
                    methodcall_attr_dict = deepcopy(methodcall_calls_attr_list_dict[idx])
                else:
                    methodcall_attr_dict = {}
                    
                edge_label = methodcallitem.call
                graph.add_node(edge_label)
                graph.add_edge(self.sender, edge_label, key = None, attr_dict = deepcopy(sender_methodcall_edge_attr_dict))
                methodcall_attr_dict.update({NodeAttributes.NATTR_LINENUMBER : str(methodcallitem.linenr)}) 
                methodcall_attr_dict.update({NodeAttributes.NATTR_ADDRESS : str(hex(methodcallitem.address))}) 
                graph.add_attributes(edge_label, methodcall_attr_dict)
