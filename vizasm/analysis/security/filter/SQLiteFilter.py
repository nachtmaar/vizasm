'''
VizAsm

Created on 12.09.2013

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

from vizasm.analysis.security.filter.SecurityFilter import SecurityFilter
import util
from vizasm.Settings import setting_for_key, SETTINGS_C_FUNC_HEURISTIC

class SQLiteFilter(SecurityFilter):
    ''' Sqlite3 filter '''

    def filter_method_call(self, function):
        has_format_string = util.mc_has_format_string(function)
        # only check for exploitable sql statement if the argument of the c function are available
        if setting_for_key(SETTINGS_C_FUNC_HEURISTIC):
            is_sqlite_func = util.mc_c_function_has_any_name(function, ['sqlite3_prepare'], search_substring = True)
            return is_sqlite_func and has_format_string
        # check for any sqlite3 call
        is_sqlite_func = util.mc_c_function_has_any_name(function, ['sqlite3'], search_substring = True)
        return is_sqlite_func
    
    def _description(self):
        return 'Filter exploitable sqlite3 calls (if the c function arguments heuristic is enabled!). Otherwise all sqlite3 calls will be filtered.'