'''
VizAsm

Created on 12.04.2013

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

from vizasm.RegEx import RegEx

class AsmRegEx(RegEx):
    ''' 
    This class contains regular expressions used for the reading of an asm file.

    Parameters
    ----------
    RE_SECTION_SPLIT
        use to split asm file into sections
        
    RE_PROCEDURE
        use to detect the beginning of a procedure, use with flag re.DOTALL and without re.VERBOSE !
    '''
    
    # ; Section __text ...
    # Use this re to split on section
    RE_SECTION_SPLIT = r'''
 Section\s+               # Section __
 (__.*)                   # first split is section name (text) and the rest is the section data
 \s+;\s+                  # remove the next line with whitespace and semicolon and whitespace
 '''          
    # ; Section __text ...
    RE_SECTION_GR_SECTION = 'section'
    RE_SECTION = r'''
     Section\s+              # Section __
     (?P<%s>__\w+)             # section name (e.g. text)
    ''' % RE_SECTION_GR_SECTION
    
    RE_PROCEDURE = r'================ B E G I N   O F   P R O C E D U R E ================'

