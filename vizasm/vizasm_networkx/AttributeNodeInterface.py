'''
VizAsm

Created on 09.06.2013

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

from vizasm.vizasm_networkx.GraphUtil import GraphUtil


class AttributeNodeInterface:
    '''
    Interface for customizing a node in the gexf file format 

    Parameters
    ----------
    __gexf_viz_attr_dict: dict
        dictionary holding the specified attributes of the viz extension 
    
    See Also
    --------
    http://gexf.net/format/viz.html
    '''
    
    def __init__(self):
        self.__gexf_viz_attr_dict = self.__create_gexf_viz_attr_dict()

    def get_gexf_viz_attr_dict(self):
        return self.__gexf_viz_attr_dict

    def set_gexf_viz_attr_dict(self, value):
        self.__gexf_viz_attr_dict = value

    gexf_viz_attr_dict = property(get_gexf_viz_attr_dict, set_gexf_viz_attr_dict, None, "__gexf_viz_attr_dict: dict -- dictionary holding the specified attributes of the viz extension")
        
    def node_color_transparency(self):
        ''' Transparency of the node 
        
        Returns
        -------
        transparancy: double
            t in [0, 1]
        '''
        return 1.0
    
    def node_color_red(self):
        ''' Red part of rgb color 
        
        Returns
        -------
        red: int
            r in {0, 1, ..., 255}
        '''
        return 0
    
    def node_color_green(self):
        ''' Green part of rgb color 
        
        Returns
        -------
        green: int
            g in {0, 1, ..., 255}
        ''' 
        return 0
    
    def node_color_blue(self):
        ''' Blue part of rgb color 
        
        Returns
        -------
        blue: int
            b in {0, 1, ..., 255}
        
        '''
        return 0
    
    def node_size(self):
        ''' Node Size
        
        Returns
        -------
        size: double
            default is 1.0
         '''
        return 1.0

    def get_viz_color_dict(self):    
        ''' Returns the subdictionary with the color key keeping structure of the dictionary '''
        return GraphUtil.get_viz_color_dict(self.get_gexf_viz_attr_dict())
    
    def get_size(self):
        ''' Returns the subdictionary with the size key keeping structure of the dictionary '''
        return GraphUtil.get_size(self.get_gexf_viz_attr_dict())
    
    def __create_gexf_viz_attr_dict(self):
        '''
        Returns an attribute dictionary that can be directly used for a node in networkx.
        
        Returns
        -------
        dict: dict
            dictionary of attributes according to the gexf extension Visualization 
            Example: {'viz': {'color': {'a': 1.0, 'r': 0, 'b': 0, 'g': 0}, 'size': 1.0}}
        '''
        return GraphUtil.viz_dict(self.node_color_transparency(),
                                  self.node_color_red(), self.node_color_green(),
                                  self.node_color_blue(), self.node_size())
    
    
