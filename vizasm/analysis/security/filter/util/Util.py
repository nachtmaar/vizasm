'''
VizAsm

Created on 18.10.2013

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

from vizasm.util import Util


def ut_search_string(string, ut_search_string, search_substring = False, ignore_case = True):
    '''
    Check if `string` is equal to `ut_search_string` or
    if `search_substring` `string` contains `search_substring`.
    
    Parameters
    ----------
    string: string
    ut_search_string: string
    search_substring: bool (default is False)
        If True match even if just substring found (`find`).
        Otherwise check for exact equality via `==`.    
    ignore_case: bool
        ignore case if enabled
    '''
    if ignore_case:
        return Util.ignore_case_find(string, ut_search_string) if search_substring else str(string).upper() == ut_search_string.upper()
    return string.find(search_substring) != -1 if search_substring else str(string) == ut_search_string
