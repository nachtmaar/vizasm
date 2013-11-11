'''
VizAsm

Created on 30.03.2013

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

from os import path
from vizasm.util.ModuleClassNameException import ModuleClassNameException, \
    ModuleNotSameClassNameException
import collections
import random
import sys


def filter_not_none(sequence):
    return filter(lambda x: x is not None, sequence)    

def get_fst_not_none(sequence):
    ''' Get the first object that is not None.
    Returns None if nothing found '''
    res = filter_not_none(sequence)
    if res:
        return res[0]
    return None

def random_rgb_val():
    ''' Returns a random int in {0,...,255} '''
    return random.randint(0, 255)

def surrounding_elements_from_list(l, split_idx, cnt_sur_lines):
    ''' Returns the surrounding lists (before and after) the given index.
    
    Parameters
    ----------
    l: list
    split_idx: int
        the index at which to split in lines before and lines after
    cnt_sur_lines: int
        the number of lines before and after
        
    Returns
    -------
    surrounding lines: (list, list)
        tuple of surrounding lists
    '''
    lines_before, lines_after = [], [] 
    for i, line in enumerate(l):
        if i < split_idx:
            lines_before.append(line)
        elif i > split_idx:
            lines_after.append(line)
    lines_before = lines_before[-cnt_sur_lines:]
    lines_after = lines_after[:cnt_sur_lines]
    return lines_before, lines_after

def strlist_to_str(strlist):
    ''' Make a string out of a list of strings and add newlines. '''
    return '\n'.join(strlist)

def append_syspath(file_str):
    '''
    Append file to system path.
    
    Parameters
    ----------
    file_str: str
    '''
    print 'appending %s to sys path' % path.dirname(path.abspath(file_str))
    sys.path.append(path.dirname(path.abspath(file_str)))
    
def modulename_from_fqn(fqn):
    '''
    Get the module name from the fully qualified name.
    
    Parameters
    ----------
    fqn: str
        
    Returns
    -------
    module_name: str
    '''
    return fqn.split('.').pop()

def remove_py_extension(file_path):
    '''
    Remove the ".py" extension from the file path or filename.
    
    Parameters
    ----------
    file_path: str
        the filename or file_path
    '''
    return remove_file_extension(file_path, 'py')
    
def remove_file_extension(file_path, file_extension):
    '''
    Remove the file extension from the file_path or filename.
    
    Parameters
    ----------
    file_path: str
        the filename or file_path
    file_extension: str
        file extension, not starting with a "."
    '''
    return file_path.split('.%s' % file_extension)[0]
    
def class_for_filepath(fqn, class_name):
    ''' Return the class reference (not instantiated yet)
    
    Parameters
    ----------
    fqn: string
        fully qualified name
    class_name: str
        the name of the class to be loaded
        
    Raises
    ------
    ModuleClassNameException
        if the module does not have the specified class
    ImportError:
        if the fqn could not be imported
     '''
    __import__(fqn)
    if hasattr(sys.modules[fqn], class_name):
        return getattr(sys.modules[fqn], class_name)
    raise ModuleClassNameException(fqn, class_name)
    
def class_for_fqn_mod_eq_class(fqn):
    ''' 
    Get the class for the specified fully qualified name.
    The classname is assumed to be the same like the module name from the fqn. 
    
    Returns
    _______
    class: class
    
    Raises
    ------
    ModuleNotSameClassNameException
        if the module does not have the same name like the class
    ImportError:
        if the fqn could not be imported
    '''
    try:
        return class_for_filepath(fqn, modulename_from_fqn(fqn))
    except ModuleClassNameException as e:
        raise ModuleNotSameClassNameException(e.class_name), None, sys.exc_info()[2]

def is_iterable(iterable):
    ''' Check if `iterable` is iterable '''
    return isinstance(iterable, collections.Iterable)

def is_iterable_no_string(iterable):
    ''' Check if `iterable` is iterable and no python string '''
    from vizasm.model import ModelUtil
    return isinstance(iterable, collections.Iterable) and not ModelUtil.is_python_string(iterable)

def ignore_case_find(name, search_str):
    ''' Check if `name` contains `search_str` by ignoring case '''
    return name.upper().find(search_str.upper()) != -1 or name.lower().find(search_str.lower()) != -1

def hex_string_without_0x(number):
    ''' Return a string representation of the number and cut off the "0x" prefix.
    Returns None if something went wrong.
    
    Parameters
    ----------
    number: number
    '''
    try:
        # cut off the 0x prefix and use upper case for rest of address 
        return hex(number)[2:]
    except TypeError:
        return None
    
def str2int(int_str):
    ''' Convert the string to an int.
    If not possible, return none '''
    try:
        return int(int_str)
    except ValueError:
        return None
    
def hex2int(hex_str):
    ''' Convert the string (with or without 0x prefix) to hex.
    If not possible, return none '''
    zx_prefix = '0x'
    if hex_str.find(zx_prefix) != -1:
        hex_str = zx_prefix + hex_str
    try:
        return int(hex_str, 16)
    except ValueError:
        return None

def pretty_format_dict(dictionary, use_repr_for_value = False):
    '''
    Pretty print dictionary into multiple lines, each one containing one key and value.
    
    Parameters
    ----------
    dictionary: dict
    use_repr_for_value: bool, optional (default is False)
        if enabled use repr() instead of str() for formatting of dict values 
    '''
    res = ''
    for key, val in dictionary.items():
        value_str = str(val) if not use_repr_for_value else repr(val)
        res += '(%s, %s) \n' % (key, value_str)
    return res    

def format_dict_as_table(dictionary, columnname1 = None, columnname2 = None, v_delimiter = '-', h_delimiter = '|', column_delimiter = '+'):
    ''' Format a dictionary as table.
    If all of the column names are None, no header will be printed!
    
    Parameters
    ---------
    dictionary: dict
        the dictionary to print as table
    columnname1: string, optional (default is '') 
        name of the first column (will be printed in the header)
    columnname2: string, optional (default is '') 
        name of the first column (will be printed in the header)
    h_delimiter: string, optional (default is '-')
        the horizontal delimiter char
    v_delimiter: string, optional (default is '|')
        the vertical delimiter char
    column_delimiter: string, optional (default is '+')
        the column delimiter char
    '''
    res = ''

    print_header = all(column_name is not None for column_name in (columnname1, columnname2))
    if columnname1 is None:
        columnname1 = ''
    if columnname2 is None:
        columnname2 = ''
        
    cn1_len , cn2_len = len(columnname1), len(columnname2)
    # get max width
    max_width_key, max_width_val = cn1_len, cn2_len
    
    for key, val in dictionary.items():
        key_len, val_len = map(lambda x: len(str(x)), (key, val))
        max_width_key = max(max_width_key, cn1_len, key_len)
        max_width_val = max(max_width_val, cn2_len, val_len)
        
    delimiter_line = column_delimiter + v_delimiter * (max_width_key + 2) + column_delimiter + v_delimiter * (max_width_val + 2) + column_delimiter + '\n'
    
    # only print header if not all columnnames are None
    indent_string = '%s {0:<%d} %s {1:<%d} %s \n' % (h_delimiter, max_width_key, h_delimiter, max_width_val, h_delimiter)
    if print_header:
        res += delimiter_line
        res += indent_string.format(columnname1, columnname2)
        res += delimiter_line

    # actual dictionary formatting
    if dictionary:
        for key, val in dictionary.items():
            res += indent_string.format(key, val)
        res += delimiter_line
    return res   

def sorted_dict_values_it(dictionary):
    ''' Get a list of sorted dict values '''
    return (x[1] for x in sorted(dictionary.iteritems())) 

if __name__ == '__main__':
    print surrounding_elements_from_list((str(i) for i in range(10)), 0, 5)
    
