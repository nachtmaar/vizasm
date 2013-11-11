'''
VizAsm

Created on 02.10.2013

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

''' This module keeps the known segment names '''

SEGMENT_OBJC_IVAR = '__objc_ivar'
SEGMENT_TEXT = '__text'
SEGMENT_OBJC_CLASSREFS = '__objc_classrefs'
SEGMENT_OBJC_SUPERREFS = '__objc_superrefs'
SEGMENT_OBJC_DATA = '__objc_data'

''' the segments where the superclass infos are stored '''
SEGMENTS_SUPERCLASS_INFOS = [SEGMENT_OBJC_CLASSREFS, SEGMENT_OBJC_DATA]

def segment_for_name(name, segments):
    ''' Get the section from the list of available section '''
    for seg in segments:
        if seg.getName() == name:
            return seg
    return None