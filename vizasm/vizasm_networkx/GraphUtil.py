'''
VizAsm

Created on 28.07.2013

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

from vizasm.util.Log import log_exception, log_critical
from vizasm.vizasm_networkx.GexfConstants import TAG_VIZ, TAG_COLOR, \
    TAG_COLOR_TRANSPARENCY, TAG_COLOR_RED, TAG_COLOR_BLUE, TAG_COLOR_GREEN, TAG_SIZE, \
    TAG_EDGE_WEIGHT
import networkx as nx

class GraphUtil:
    ''' Utility for a graph ''' 
    
    @staticmethod
    def viz_dict(transparency = 1.0, red = 255, green = 219, blue = 73, size = 1.0):
        '''
        Returns an attribute dictionary that can be directly used for a node in networkx.
        
        Parameters
        ----------
        transparency: double
            value in [0, 1]
        red, green, blue: int, optional (default is yellow)
            value in {0, ..., 255}
            
        Returns
        -------
        dict: dict
            dictionary of attributes according to the gexf extension Visualization 
            Example: {'viz': {'color': {'a': 1.0, 'r': 0, 'b': 0, 'g': 0}, 'size': 1.0}}
        '''
        return {TAG_VIZ : 
                    {TAG_COLOR : {TAG_COLOR_TRANSPARENCY : transparency,
                                  TAG_COLOR_RED : red,
                                  TAG_COLOR_BLUE : blue,
                                  TAG_COLOR_GREEN : green},
                    TAG_SIZE : size
                    }
                }
        
    @staticmethod
    def edge_weight_attr_dict(weight):
        '''
        Returns a dictionary specifying the weight of an edge.
        
        Parameters
        ----------
        weight: float
            weight of the edge
            
        Returns
        -------
        edge_attr_dict: dict
        '''
        return {TAG_EDGE_WEIGHT : weight}        

    @staticmethod
    def subdict_kstruct_with_key(attr_dict, key):
        ''' Return a dictionary only containing the entry with the specified key,
        but keeping the structure. 
        Meaning that structure above the key will be still present in the returned subdict.
        
        Parameters
        ----------
        attr_dict: dict
        key: hashable
        '''
        return {key : attr_dict[key]}
    
    @staticmethod
    def subdict_kstruct_with_keys(attr_dict, key_list):
        ''' Return a dictionary only containing the entry with the specified keys,
        but keeping the structure. 
        Meaning that structure above the keys will be still present in the returned subdict.
        
        If no keys are given, an empty dict will be returned.
        
        Parameters
        ----------
        attr_dict: dict
        key_list: list
        '''
        val = attr_dict
        sub_dict = {}
        struct_dict = sub_dict
        cnt_keys = len(key_list)
        
        if key_list:
            last_key = None
            for idx, key in enumerate(key_list):    
                val = val[key]
                sub_dict[key] = {}
                # go in front of the dict with the last key 
                if idx < cnt_keys - 1:
                    sub_dict = sub_dict[key]
                last_key = key
            sub_dict[last_key] = val
        return struct_dict
        
    @staticmethod
    def get_viz_color_dict(viz_dict):    
        ''' Returns the subdictionary with the color key keeping structure of the dictionary '''
        return GraphUtil.subdict_kstruct_with_keys(viz_dict, [TAG_VIZ, TAG_COLOR])
    
    @staticmethod
    def get_size(viz_dict):
        ''' Returns the subdictionary with the size key keeping structure of the dictionary '''
        return GraphUtil.subdict_kstruct_with_keys(viz_dict, [TAG_VIZ, TAG_SIZE])
    
    @staticmethod
    def update_color(viz_dict, update_dict):
        ''' Update the color without overwriting/erasing the size attribute '''
        size = None
        if TAG_VIZ in update_dict and TAG_SIZE in update_dict[TAG_VIZ]: 
            size = update_dict[TAG_VIZ][TAG_SIZE]
            
        if not TAG_VIZ in viz_dict:
            viz_dict[TAG_VIZ] = {}
            
        viz_dict.update(update_dict)
        if size is not None:
            viz_dict[TAG_VIZ][TAG_SIZE] = size
            
        return viz_dict
        
    @staticmethod
    def write_gexf(graph, graph_filepath):
        ''' Write the graph to the specified file '''
        try:
            if graph_filepath is not None:
                nx.write_gexf(graph, graph_filepath, encoding = 'utf-8')
        except Exception as e:
            log_critical('Gexf file not completely written !\n')
            log_exception(e)
            
if __name__ == '__main__':
    attr_dict = {'viz': {'color': {'a': 1.0, 'r': 0, 'b': 0, 'g': 0}, 'size': 1.0}}
    print GraphUtil.subdict_kstruct_with_keys(attr_dict, ['viz', 'color'])
    print GraphUtil.subdict_kstruct_with_keys(attr_dict, [])
    print GraphUtil.get_viz_color_dict(attr_dict)
    print GraphUtil.get_size(attr_dict)
         
