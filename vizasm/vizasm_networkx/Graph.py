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

from networkx import MultiDiGraph

class Graph(MultiDiGraph):

    def add_node(self, n, attr_dict = None, **attr):
        if attr_dict is None:
            attr_dict = {}
        # node ids seem to be important for drawing the connections between 2 equal functions
        attr_dict['id'] = hash(n)
        MultiDiGraph.add_node(self, n, attr_dict = attr_dict, **attr)
        
    def add_attributes(self, n, attribs):
        '''
        Add the attribute from the dictionary for `Node` n.
        
        Parameters
        ----------
        n: Node
        attribs: dict
        '''
        if not attribs is None:
            attr_dict = self.node[n]
            if attr_dict is None:
                attr_dict = {}
            attr_dict.update(attribs)
            
