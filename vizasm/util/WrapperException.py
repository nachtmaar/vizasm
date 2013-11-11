'''
VizAsm

Created on 10.04.2013

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

class WrapperException(Exception):
    r''' 
    Exception for wrapping up exceptions.
    
    Parameters
    ----------
    _caused_by: Exception
        exception that caused this one to raise
    '''
    
    def __init__(self, caused_by):
        Exception.__init__(self)
        self._caused_by = caused_by
        
    def __str__(self):
        return 'Caused by: %s:%s' % (self._caused_by.__class__.__name__, str(self._caused_by))
            
        
