'''
VizAsm

Created on 16.09.2013

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

class GeoLocationFilter(SecurityFilter):
    '''
    Check which geo information are retrieved and which accuracy level is set. 
        
    See
    ---
    CCLocation.h
    https://developer.apple.com/library/ios/documentation/CoreLocation/Reference/CoreLocationConstantsRef/Reference/reference.html#//apple_ref/doc/uid/TP40010237-CH1-SW1
    https://developer.apple.com/library/mac/documentation/CoreLocation/Reference/CLLocationManagerDelegate_Protocol/CLLocationManagerDelegate/CLLocationManagerDelegate.html#//apple_ref/occ/intf/CLLocationManagerDelegate
    '''
    
    # available accuracy levels
    LOCATION_ACCURACY_LEVELS = ['kCLLocationAccuracyBestForNavigation', 'kCLLocationAccuracyBest',
                                'kCLLocationAccuracyNearestTenMeters', 'kCLLocationAccuracyHundredMeters',
                                'kCLLocationAccuracyKilometer', 'kCLLocationAccuracyThreeKilometers'
                                ]
    
    def filter_method_call(self, function):
        # check for CLLocationManagerDelegate
        location_manager_delegate_sel = 'locationManager:'
        
        # check if accuracy level has been set
        accuracy_sel = 'setDesiredAccuracy:'
        
        # match startUpdatingLocation and stopUpdatingLocation
        update_location_sel = 'UpdatingLocation' 
        
        sel_res = util.mc_has_any_selector(function, [accuracy_sel, location_manager_delegate_sel, update_location_sel], search_substring = True)
        
        # check for accuracy parameter
        accuracy_level = 'kCLLocationAccuracy'
        accuracy_level_set = util.mc_contains_imp_got(function, accuracy_level, search_substring = True)
        
        return sel_res or accuracy_level_set
    
    def _description(self):
        return 'Check which geo information are retrieved and which accuracy level is set. Available levels: %s' % ', '.join(self.LOCATION_ACCURACY_LEVELS)
        
