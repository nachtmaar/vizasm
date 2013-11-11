'''
VizAsm

Created on 08.10.2013

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



Helper module for `SecurityFilter`s '''


from vizasm.Archs import ARCH_ARM, ARCH_ANYTHING
from vizasm.analysis.security.filter.BackgroundTasksFilter import \
    BackgroundTasksFilter
from vizasm.analysis.security.filter.CFStreamSSLLevelFilter import \
    CFStreamSSLLevelFilter
from vizasm.analysis.security.filter.CookiePolicyFilter import \
    CookiePolicyFilter
from vizasm.analysis.security.filter.DataProtectionFilter import \
    DataProtectionFilter
from vizasm.analysis.security.filter.FormatStringFilter import \
    FormatStringFilter
from vizasm.analysis.security.filter.GeoLocationFilter import GeoLocationFilter
from vizasm.analysis.security.filter.IPCFilter import IPCFilter
from vizasm.analysis.security.filter.KeyChainFilter import KeyChainFilter
from vizasm.analysis.security.filter.NSStreamSSLLevelFilter import \
    NSStreamSSLLevelFilter
from vizasm.analysis.security.filter.NSUserDefaultsFilter import \
    NSUserDefaultsFilter
from vizasm.analysis.security.filter.RandomFuncFilter import RandomFuncFilter
from vizasm.analysis.security.filter.SQLiteFilter import SQLiteFilter
from vizasm.analysis.security.filter.SeatBeltFilter import SeatBeltFilter
from vizasm.analysis.security.filter.UIPasteBoardFilter import \
    UIPasteBoardFilter
from vizasm.analysis.security.filter.UntrustedSSLCertsFilter import \
    UntrustedSSLCertsFilter
    
SECURITY_FILTERS = [NSUserDefaultsFilter, UntrustedSSLCertsFilter, RandomFuncFilter,
                        FormatStringFilter, CFStreamSSLLevelFilter, NSStreamSSLLevelFilter,
                        IPCFilter, SQLiteFilter, CookiePolicyFilter,
                        KeyChainFilter,
                        GeoLocationFilter, SeatBeltFilter,
                        DataProtectionFilter, UIPasteBoardFilter, BackgroundTasksFilter]        

def security_filters(arch):
    ''' Get the available `SecurityFilter`s for the specified architecture '''
    if arch == ARCH_ARM:
        return get_ios_filters()
    return get_mac_filters()

def get_all_std_security_filters():
    ''' Get all available standard `SecurityFilter`s independent of the platform '''
    return get_ios_filters() + get_mac_filters()

def get_ios_filters():
    ''' Get all available standard iOS filters '''
    return get_filters("config_ios_filter")

def get_mac_filters():
    ''' Get all available standard mac filters '''
    return get_filters("config_mac_filter")

def get_filters(func):
    ''' Get all available standard filters (filtered by `func`) '''
    return [f for f in SECURITY_FILTERS if getattr(f(), func)()]

def format_available_filters(arch):
    ''' Return a description of available filters.
    Available filters are currently those which are in the static field `SECURITY_FILTERS`
    '''
    filters = None
    if arch == ARCH_ANYTHING:
        filters = get_all_std_security_filters() 
    else:
        filters = security_filters(arch)
    return (2 * '\n').join(map(lambda f: f().description(), filters))
