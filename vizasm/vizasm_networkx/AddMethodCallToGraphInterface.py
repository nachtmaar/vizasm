'''
VizAsm

Created on 19.04.2013

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

class AddMethodCallToGraphInterface:
    r'''
    Interface for adding a `MethodCall` to a graph.
    '''
    
    def add_to_graph(self, graph, methodcall_sender_attr_dict = None, methodcall_calls_attr_list_dict = None,
                      sender_methodcall_edge_attr_dict = None):
        r'''
        Add the contents of the `MethodCall` to a graph.
        
        Parameters
        ----------
        graph : Graph
        methodcall_sender_attr_dict: dict<object>, optional
            dictionary of attributes for the sender of a `MethodCall
        methodcall_calls_attr_list_dict: list<dict<object>>, optional
            list of attribute dictionaries for the calls of a `MethodCall
            each dict in the list is supposed for the corresponding call of the `MethodCall`
        sender_methodcall_edge_attr_dict: dict<object> optional
            dictionary specifying the edge between the sender and the methodcall  
        '''
        raise NotImplementedError

