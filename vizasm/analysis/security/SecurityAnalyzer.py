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

from vizasm.model.objc.methodcall.MethodCall import MethodCall
from vizasm.vizasm_networkx.AddMethodCallToGraphInterface import \
    AddMethodCallToGraphInterface

class SecurityAnalyzer(object, AddMethodCallToGraphInterface):
    ''' 
    Analyze a MethodCall with `SecurityFilter`s.
    
    Attributes
    ----------
    AVAILABLE_FILTERS: list<classobj<Filter>>
    
    Parameters
	----------
    _methodcall: MethodCall
        the MethodCall that shall be analyzed
	_filters: list<SecurityFilter>, optional
	    list of filters to use
    _filter_results: dict<SecurityFilter, list<MethodCall>>
        dict holding the results for each filter 
    '''
    
    def __init__(self, methodcall, filters = None):
        self._methodcall = methodcall
        if filters is None:
            filters = []
        self._filters = filters
        self._filter_results = dict(zip(filters, ([] for _ in range(len(filters)))))

    def get_filter_results(self):
        return self._filter_results

    def set_filter_results(self, value):
        self._filter_results = value

    def get_filters(self):
        return self._filters

    def set_filters(self, value):
        self._filters = value

    def get_methodcall(self):
        return self._methodcall

    def set_methodcall(self, value):
        self._methodcall = value
        
    methodcall = property(get_methodcall, set_methodcall, None, "_methodcall: MethodCall -- the MethodCall that shall be analyzed")
    filters = property(get_filters, set_filters, None, "_filters: list<SecurityFilter>, optional -- list of filters to use")
    filter_results = property(get_filter_results, set_filter_results, None, "_filter_results(dict<SecurityFilter, list<MethodCall>>) -- dict holding the results for each filter")
            
    def add_filter(self, security_filter):
        r'''
        Add a filter.
        
        Parameters
        ----------
        security_filter: SecurityFilter
            the filter to add
        '''
        self.get_filters().append(security_filter)
    
    def add_filters(self, security_filter_list):
        r'''
        Add a list of filters.
        
        Parameters
        ----------
        security_filter_list: list<SecurityFilter>
            the filters to add
        '''
        self.get_filters().extend(security_filter_list)
    
    def apply_filters(self, graph = None, methodcall_sender_attr_dict = None, methodcall_calls_attr_list_dict = None,
        sender_methodcall_edge_attr_dict = None):
        '''
        Apply all `SecurityFilter` and add all to the graph if not None.
        
        Parameters
        ----------
        graph: Graph
            the graph to which the `SecurityFilter` and its filtered content shall be added.
            if None, nothing will be added.
            
        Returns
        -------
        methodcall: MethodCall
            The filtered MethodCall after applying all filters.
            A new one will be constructed!
        '''
        calls = []
        for security_filter in self.get_filters():
            security_filter.set_methodcall(self.get_methodcall())
            security_filter.filter()
            if graph is not None:
                security_filter.add_to_graph(graph, methodcall_sender_attr_dict,
                                             methodcall_calls_attr_list_dict, sender_methodcall_edge_attr_dict)
            filtered_calls = security_filter.get_methodcall().get_calls()
            # `MethodCall` results for current `SecurityFilter`
            filtered_methodcall = MethodCall(self.get_methodcall().get_sender(), filtered_calls)
            filter_results = self.filter_results
            if len(filtered_methodcall) > 0:
                filter_results[security_filter].append(filtered_methodcall)
            calls.extend(filtered_calls)
        methodcall = MethodCall(self.get_methodcall().get_sender(), calls)
        return methodcall

    def format_filter_results(self):
        ''' If filtering enabled, format the results of each `SecurityFilter` and return it as string '''
        res = ''
        for security_filter, filter_results in self.filter_results.items():
            seperator = 150 * '=' + '\n'
            if filter_results:
                res += '%s\n%s' % (security_filter, seperator)
                res += '\n'.join((str(mcall) for mcall in filter_results))
                res += '%s%s' % (seperator, '\n' * 5)
        return res
            
#####################################################################################
# AddToGraphInterface                                                               #
#####################################################################################

    def add_to_graph(self, graph, methodcall_sender_attr_dict = None, methodcall_calls_attr_list_dict = None,
        sender_methodcall_edge_attr_dict = None):
        ''' Add the `SecurityFilter` and all its filtered content to the graph '''
        for security_filter in self.filters:
            # do not add empty filters
            if len(security_filter) > 0:
                security_filter.add_to_graph(graph, methodcall_sender_attr_dict,
                                         methodcall_calls_attr_list_dict, sender_methodcall_edge_attr_dict)
    
        
