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

import re
class RegEx(object):
    
    @staticmethod 
    def compiled_vre(regex, flags = re.VERBOSE):
        ''' 
        Returns a compiled regex pattern object 
        Parameters
        ----------
        flags
            the flags to be passed to re (default is re.VERBOSE)
        '''
        return re.compile(regex, flags)        
    
    @staticmethod 
    def compiled_re(regex, flags = None):
        ''' 
        Returns a compiled regex pattern object
        Flags will only be passed if not None.
         
        Parameters
        ----------
        flags: optional
            the flags to be passed to re 
        '''
        if flags is None:
            return re.compile(regex)
        return re.compile(regex, flags)        
