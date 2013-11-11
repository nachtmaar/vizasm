'''
VizAsm

Created on 20.04.2013

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

from vizasm.model.objc.methodcall.MethodCall import MethodCall
from vizasm.model.objc.methodcall.MethodCallItem import METHODCALLITEM_PSEUDO
from vizasm.util import Util
from vizasm.vizasm_networkx import NodeAttributes
from vizasm.vizasm_networkx.AddMethodCallToGraphInterface import \
    AddMethodCallToGraphInterface
from vizasm.vizasm_networkx.AttributeDictInterface import AttributeDictInterface
from vizasm.vizasm_networkx.AttributeNodeInterface import AttributeNodeInterface
from vizasm.vizasm_networkx.GexfConstants import TAG_VIZ, TAG_SIZE
from vizasm.vizasm_networkx.GraphUtil import GraphUtil


class SecurityFilter(object, AddMethodCallToGraphInterface, AttributeNodeInterface, AttributeDictInterface):
    '''
    BaseClass for a security filter.
     
    Parameters
    ----------
    _methodcall: MethodCall
        the MethodCall to analyze
    _name: string, optional
        the name of the SecurityFilter is used for the node representation in the graph.
        If no name is given, the class name will be used instead.
         
    
    -----
    Subclasses need to overwrite the following methods:
        filter_method_call or filter_method_definition
        config_ methods
        _description
    '''
    
    def __init__(self, name = None, methodcall = None):
        AttributeNodeInterface.__init__(self)
        if name is None:
            name = self.__class__.__name__
        if methodcall is None:
            methodcall = MethodCall(None)
        self._methodcall = methodcall
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    def get_methodcall(self):
        return self._methodcall

    def set_methodcall(self, value):
        self._methodcall = value
    
    def __str__(self):
        return self.description()
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if isinstance(other, SecurityFilter):
            return self is other or self.name == other.name
        return False
    
    def __hash__(self):
        return hash(self.name)
    
    def __len__(self):
        return len(self.methodcall)
    
    def __iter__(self):
        return iter(self.methodcall)
    
    methodcall = property(get_methodcall, set_methodcall, None, "_methodcall(MethodCall) -- the MethodCall to analyze")
    name = property(get_name, set_name, None, "_name(string) -- the name of the SecurityFilter is used for the node representation in the graph.")
    
    def description(self):
        ''' The full description of the filter '''
        return '%s:\n%s' % (self.name, self._description())

    def filter(self):
        ''' 
        Filter the `MethodCall` according to the filter and replace the old one with the filtered one.
        
        Define with the  `config_` methods if you want to filter on the method calls or the method definition (or both).
        
        If filtering on the method definition is successful, all function calls will be kept.
        Otherwise the function calls will be filtered.
        '''
        methodcall = self.methodcall
        
        filtered_methodcallitems = []
        filter_method, filter_call = self.config_filter_method_definition(), self.config_filter_method_call()
        
        # filter methods definition
        if filter_method:
            if self.filter_method_definition(self.get_methodcall().get_sender()):
                filtered_methodcallitems = methodcall.get_calls()
                filter_call = False
                if not filtered_methodcallitems:
                    # fix for displaying the `MethodCall` - add a pseudo method call
                    filtered_methodcallitems.append(METHODCALLITEM_PSEUDO)
                    
        # filter function call if not already method definition did match
        if filter_call:
            for methodcallitem in methodcall:
                if self.filter_method_call(methodcallitem.get_call()):
                    filtered_methodcallitems.append(methodcallitem)
        
        self.set_methodcall(MethodCall(methodcall.get_sender(), filtered_methodcallitems))
        
#####################################################################################
# Overwrite these in a subclass                                                     #
#####################################################################################    

    def filter_method_call(self, function):
        '''
        This method is used for the filtering and shall be overwritten by any subclass.
        It should return false for all the objects that shall be filtered out.
        The objects for which true is returned are the ones that will be kept.
        
        Parameters
        ----------
        function: FunctionInterface
            the `FunctionInterface` to filter
        
        Returns
        -------
        True
            if the object shall be kept
        False
            if the object is not of any relevance
        ''' 
        raise NotImplementedError
    
    def filter_method_definition(self, method):
        '''
        Filter on the method definition.
        
        Parameters
        ----------
        method: MsgSend
        '''
        raise NotImplementedError
    
    def config_filter_method_call(self):
        ''' Filter on a method call. A function call being made inside a method implementation.
        You can filter for method calls and method definition at the same time! '''
        return True
    
    def config_filter_method_definition(self):
        ''' Filter on the method definition.
        This means that all calls that are made in this method, will be kept.
        
        If you successfully filter on a method, no further filtering for method calls will be done.

        E.g. on "- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions)" (in the original source)
        '''
        return False

    def config_ios_filter(self):
        ''' Return if `SecurityFilters` is only for iOS '''
        return True
    
    def config_mac_filter(self):
        ''' Return if `SecurityFilters` is only for mac '''
        return True
    
    def _description(self):
        ''' The user supplied description of the filter '''
        raise NotImplementedError
    
#####################################################################################
# AddMethodCallToGraphInterface
#####################################################################################

    def add_to_graph(self, graph, methodcall_sender_attr_dict = None, methodcall_calls_attr_list_dict = None, sender_methodcall_edge_attr_dict = None):
        '''
        This method adds the `SecurityFilter` to the graph and configures its attributes.
        
        Moreover it configures the attributes for the sender and call nodes of the `MethodCall`.
        But the supplied attribute dictionaries may overwrite attributes specified here.
        
        The nodes, as well as the edges between them, are configured with the same color as the `SecurityFilter`.
        The weight of the edges are the sizes of the nodes. 
        '''
        if methodcall_sender_attr_dict is None:
            methodcall_sender_attr_dict = {}
        if sender_methodcall_edge_attr_dict is None:
            sender_methodcall_edge_attr_dict = {}
            
        methodcall = self.get_methodcall()
        
        # set the node attributes of the `SecurityFilter`  
        filter_name = self.get_name()
        graph.add_node(filter_name)
        graph.node[filter_name] = self.attribute_dictionary()      

        # specify attributes for the sender of a `MethodCall` (node)
        m_sender_methodcall_edge_attr_dict = GraphUtil.edge_weight_attr_dict(NodeAttributes.NVAL_METHODCALL_SIZE_CALL)
        m_sender_methodcall_edge_attr_dict.update(sender_methodcall_edge_attr_dict)
        
        # set up the attribute dictionaries and add the `MethodCall` to the graph
        if not methodcall.is_empty():
            # add connection between filter and sender of the message
            name = self.get_name()
            sender = methodcall.sender
            graph.add_node(sender)
            graph.add_edge(name, sender, key = None, attr_dict = GraphUtil.edge_weight_attr_dict(NodeAttributes.NVAL_METHODCALL_SIZE_SENDER))
            # add color
            m_methodcall_sender_attr_dict = deepcopy(self.get_gexf_viz_attr_dict())
            m_methodcall_sender_attr_dict[TAG_VIZ][TAG_SIZE] = NodeAttributes.NVAL_METHODCALL_SIZE_SENDER
            # can overwrite already specified attributes
            m_methodcall_sender_attr_dict.update(methodcall_sender_attr_dict)
            m_methodcall_calls_attr_list_dict = []
            # create an attribute dictionary for each call of a `MethodCall`
            for idx in range(len(methodcall.get_calls())):
                methodcall_calls_attr_dict = deepcopy(self.get_gexf_viz_attr_dict())
                methodcall_calls_attr_dict[TAG_VIZ][TAG_SIZE] = NodeAttributes.NVAL_METHODCALL_SIZE_CALL
                # update with given attribute dict
                if methodcall_calls_attr_list_dict:
                    given_methodcall_calls_attr_dict = methodcall_calls_attr_list_dict[idx] 
                    methodcall_calls_attr_dict.update(given_methodcall_calls_attr_dict)
                    # update color and keep size
                    methodcall_calls_attr_dict = GraphUtil.update_color(methodcall_calls_attr_dict, self.get_viz_color_dict())
                m_methodcall_calls_attr_list_dict.append(methodcall_calls_attr_dict)
            # let the `MethodCall` do the rest of the job -> add each call to the graph
            methodcall.add_to_graph(graph, m_methodcall_sender_attr_dict, m_methodcall_calls_attr_list_dict, m_sender_methodcall_edge_attr_dict)

#####################################################################################
# AttributeNodeInterface                                                            #
#####################################################################################

    def node_color_red(self):
        return Util.random_rgb_val()

    def node_color_green(self):
        return Util.random_rgb_val()

    def node_color_blue(self):
        return Util.random_rgb_val()

    def node_size(self):
        return 50.0

#####################################################################################
# AttibuteDictInterface                                                             #
#####################################################################################

    def attribute_dictionary(self):
        ''' Merge viz attributes and filter description and return the dictionary '''
        attr_dict = {NodeAttributes.NATTR_FILTER_DESCRIPTION : self.description()}
        attr_dict.update(self.get_gexf_viz_attr_dict())
        return attr_dict
