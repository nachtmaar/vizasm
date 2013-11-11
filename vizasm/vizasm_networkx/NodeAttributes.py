'''
VizAsm

Created on 27.07.2013

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


This module describes the attributes a node has in the graph (prefixed with NATTR) 
as well as the values of some attributes (prefixed with NVAL).
'''

# filter attributes
NATTR_FILTER_DESCRIPTION = 'filter description'

# node attributes 
NATTR_LINENUMBER = 'line number'
NATTR_ADDRESS = 'address'
NATTR_METHOD = 'method'
NATTR_ASM_CODE = 'assembler code'
NATTR_METHOD_LINES_BEFORE = 'lines before'
NATTR_METHOD_LINES_AFTER = 'lines after'
NATTR_METHOD_SURROUNDING_LINES = 'surrounding lines (n=%d)'

# values of node attributes
NVAL_METHODCALL_SIZE_SENDER = 25.0
NVAL_METHODCALL_SIZE_CALL = 15.0

# the pattern for the value of the NATTR_METHOD_SURROUNDING_LINES field
# arguments: lines before, line, line after
NPATTERN_SURROUND_LINES = '''Before:
%s

--> %s

After:
%s
'''
