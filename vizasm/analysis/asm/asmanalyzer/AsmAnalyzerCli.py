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
from vizasm.reader.asm.AsmReader import AsmReader
from vizasm.Settings import *

class AsmAnalyzerCli(AsmAnalyzerBase):
    '''
    Assembler file analyzer to use from cli.
    
    Parameters
    ----------
    asmreader: AsmReader
        the asm file reader
    '''    
    def __init__(self):
        AsmAnalyzerBase.__init__(self)
        asm_filepath = setting_for_key(SETTINGS_ASM_FILEPATH)
        self.__asm_reader = AsmReader(asm_filepath)

    def get_asm_reader(self):
        return self.__asm_reader

    asm_reader = property(get_asm_reader, None, "asmreader(AsmReader) -- the asm file reader")

    def analyze(self):
        '''
        Analyze the assembler file.
        '''
        asmreader = self.asm_reader
        asmreader.reopen_file()
        
        self.log_n_read_superclasses()
        
        # choose method iterator
        asmreader.reopen_file()
        methods_it = None
        read_single_procedure = setting_for_key(SETTINGS_READ_SINGLE_PROCEDURE)
        read_all_methods = setting_for_key(SETTINGS_READ_ALL_METHODS)
        if read_single_procedure:
            methods_it = asmreader.single_method_it_asm_file()
        else:
            section_it = asmreader.sections_it(asmreader.file_obj, [Segments.SEGMENT_TEXT])
            methods_it = asmreader.methods_it(section_it, read_all_procedures = read_all_methods)
        
        try:
            self._analyze(methods_it)
        except Exception:
            asmreader.close_file()
            raise

    def read_superclasses(self):
        ''' 
        Read the super classes from the sections `Segments.SEGMENTS_SUPERCLASS_INFOS`.
        
        Returns
        -------
        dict<ObjcClass, ObjcClass>
            dict with object as key and the superclass as item
        ''' 
        asmreader = self.asm_reader
        asmreader.reopen_file()
        section_it = asmreader.sections_it(asmreader.file_obj, Segments.SEGMENTS_SUPERCLASS_INFOS)
        return self._read_superclasses(section_it)
