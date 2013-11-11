'''
VizAsm

Created on 11.10.2013

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



Stores the user supplied settings and servers functions to set and retrieve these settings.

Parameters
----------
asm_filepath: string
    the path and/or file name of the .asm file
architecture: string (see `Archs`)
    the architecture
c_func_heuristic: bool
    if enabled use heuristic to determine arguments for c function calls
read_single_procedure: boolean, optional (default is False)
    if the asm only consists of one procedure without any section    
read_all_methods: boolean, optional
    read all methods, even those that can not be matched to a type    
filters: list<SecurityFilter>, optional
    list of filters to use, if None do not filter at all
cnt_surrounding_lines: int, optional (default is 5)
    number of surrounding messages
dont_skip_exception: bool, optional (default is False)
    If enabled and and error occurrs while reading a line of assembler code, don't skip the whole method.
    This might lead to errors!    
output_filepath: string, optional
    where the output of the read messages shall be written,
    if None do not write
graph_filepath: string, optional
    where to write the graph, if None do not write    
'''

from vizasm import Archs

class Settings:
    
    # store the settings in the dict
    settings = {}
    
    def __init__(self):
        pass
    
    def __getitem__(self, key):
        return self.settings.get(key)
    
    def __setitem__(self, name, value):
        self.settings[name] = value
        
    def set_default_settings(self, default_settings_dict):
        ''' Set the default settings with `default_settings_dict`.
        Overwrites all other settings.
        Parameters
        ----------
        default_settings_dict: dict
            dictionary with SETTINGS_ keys
        '''
        self.settings = default_settings_dict

# the default `Settings` object        
settings = Settings()

# available keys
SETTINGS_ASM_FILEPATH = 'asm_filepath'
SETTINGS_OUTPUT_FILEPATH = 'output_filepath'
SETTINGS_GRAPH_FILEPATH = 'graph_filepath'
SETTINGS_C_FUNC_HEURISTIC = 'c_func_heuristic'
SETTINGS_ARCHITECTURE = 'architecture'
SETTINGS_READ_SINGLE_PROCEDURE = 'read_single_procedure'
SETTINGS_READ_ALL_METHODS = 'read_all_methods'
SETTINGS_FILTERS = 'filters'
SETTINGS_CNT_SURROUNDING_LINES = 'cnt_surrounding_lines'
SETTINGS_DONT_SKIP_EXCEPTION = 'dont_skip_exception'

def setting_for_key(key):
    ''' Get the setting for the specified `key` '''
    return settings[key]

def set_setting_for_key(key, value):
    ''' Set the `value` for the specified `key` '''
    settings[key] = value
    
def set_defaul_settings(default_settings_dict):
    ''' Set the default settings. This overwrites the existing keys.
    
    Parameters
    ----------
    default_settings_dict: dict
        dict with the settings keys
    '''
    settings.set_default_settings(default_settings_dict)
    
def is_arm():
    ''' Check if arch is arm '''
    return setting_for_key(SETTINGS_ARCHITECTURE) == Archs.ARCH_ARM

def is_x86():
    ''' Check if arch is x86 '''
    return setting_for_key(SETTINGS_ARCHITECTURE) == Archs.ARCH_X86

def is_x86_64():
    ''' Check if arch is x86_64 '''
    return setting_for_key(SETTINGS_ARCHITECTURE) == Archs.ARCH_X86_64

def filtering_enabled():
    ''' Check if filtering is enabled '''
    return setting_for_key(SETTINGS_FILTERS) is not None
