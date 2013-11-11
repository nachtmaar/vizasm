'''
VizAsm

Created on 21.08.2013

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

from vizasm.analysis.asm.asmanalyzer.AsmAnalyzerBase import AsmAnalyzerBase
from vizasm.model.asm import Segments
from vizasm.model.asm.Segments import SEGMENT_TEXT
from vizasm.reader.asm.AsmReader import AsmReader
from vizasm.util.Log import clilog
from vizasm.Settings import setting_for_key, SETTINGS_READ_SINGLE_PROCEDURE, \
    SETTINGS_READ_ALL_METHODS


class AsmAnalyzerHopper(AsmAnalyzerBase):
    '''
    Assembler analyzer which can be used from Hopper.
    
    Parameters
    ----------
    __asmline_list: list<dict<int, string>>
        iterator over the asm file
    '''
    def __init__(self, asmline_list, superclass_dict = None):
        AsmAnalyzerBase.__init__(self, superclass_dict)
        self.__asmline_list = asmline_list
        selected_method_only = setting_for_key(SETTINGS_READ_SINGLE_PROCEDURE)
        if selected_method_only:
            clilog.info('Only analyzing the selected lines!')
        
    def get_methods_it(self):
        return self.__asmline_list

    def set_methods_it(self, value):
        self.__asmline_list = value
    
    asmline_list = property(get_methods_it, set_methods_it, None, "__asmline_list(list<dict<int, string>>)")
    
    def analyze(self):
        '''
        Analyze the assembler file.
        '''
        methods_it = None
        selected_method_only = setting_for_key(SETTINGS_READ_SINGLE_PROCEDURE)
        if selected_method_only:
            methods_it = AsmReader.single_method_it(self.asmline_list)
        else:
            read_all_methods = setting_for_key(SETTINGS_READ_ALL_METHODS)
            self.log_n_read_superclasses()
            section_it = AsmReader.sections_it(self.asmline_list, [SEGMENT_TEXT])
            methods_it = AsmReader.methods_it(section_it, read_all_procedures = read_all_methods)
        self._analyze(methods_it) 
        
    def read_superclasses(self):
        ''' 
        Read the super classes from the sections `Segments.SEGMENTS_SUPERCLASS_INFOS`.
        
        Returns
        -------
        dict<ObjcClass, ObjcClass>
            dict with object as key and the superclass as item
        ''' 
        section_it = AsmReader.sections_it(self.asmline_list, Segments.SEGMENTS_SUPERCLASS_INFOS)
        return self._read_superclasses(section_it)        
