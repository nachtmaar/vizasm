'''
VizAsm

Created on 19.07.2013

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

import os
import sys
from traceback import format_exception

try:
    doc = Document.getCurrentDocument()
    doc.log("\nVizAsm Hopper")
    
    #####################################################################################
    # VizAsm Settings                                                                   #
    #####################################################################################
    
    # the directory where VizAsm is located
    # e.g
    # VIZASM_FILEAPTH = '/Users/.../vizasm'
    VIZASM_FILEAPTH = None
    if VIZASM_FILEAPTH is None:
        raise Exception('The path to VizAsm needs to be specified!')

    # write read messages to file (None disables)
    VIZASM_METHODCALL = 'methodcall_hopper.txt'
    # specifiy filters as list of strings, the module name of the filter has to be the same name as the class ! (None disables)
    VIZASM_FILTERS = None  # ['NSUserDefaultsFilter', 'SSLConnectionFilter', 'RandomFuncFilter', 'FormatStringFilter']
    # set the working directory
    VIZASM_CWD = VIZASM_FILEAPTH
    
    # boolean value, if true do not only read Objective-C method implementations 
    VIZASM_READ_ALL_METHODS = True
    # by default, if an error occurrs while reading a method, the whole method will be skipped,
    # if disabled, only the current line where the error occurred will be skipped
    # this can lead to wrong results! use with care! 
    VIZASM_DONT_SKIP_EXCEPTION = False
    # if enabled, all standard filters will be used
    VIZASM_USE_ALL_STANDARD_FILTERS = False
    # use heuristic to determine the arguments of a c function call (~2x slower)
    VIZASM_USE_HEURISTIC_FOR_C_FUNC_CALLS = False
    
    # set the verbosity ('' - 'vvvv')
    VIZASM_VERBOSITY = ''
    # suppress normal output
    VIZASM_QUIET = False
    # specify a log file as string (disable logging to file with None) 
    VIZASM_LOGFILE = None
    
    # where to write the graph (None disables)
    VIZASM_GRAPH = 'methodcall_hopper.gexf'
    # number of surrounding lines graph
    VIZASM_CNT_SURROUNDING_LINES = 5
    
    # annotate hopper
    # if enabled do not run VizAsm on the commented document again! 
    # Beause it will lead to a unexpected behavior of VizAsm (VizAsm also interprets the comments) 
    
    # annotate objc_msgSend* and other calls
    VIZASM_ANNOTATE_CALLS = False
    
    # annotate the method head.
    # This means to write a summary of the method calls etc.
    VIZASM_ANN_METHOD_HEAD = False
    
    # annotate registers (takes much longer!)
    VIZASM_ANNOTATE_REGISTERS = False  
    
    #####################################################################################
    # Debug stuff                                                                       #
    #####################################################################################
    
    DEBUG = False  # enable to use pydev debugger
    # set path to pydevd
    # e.g.
    DEBUG_PYDEVD = '/Applications/pyclipse/plugins/org.python.pydev_2.8.2.2013090511/pysrc/'
    if DEBUG:
        sys.path.append(DEBUG_PYDEVD)
        import pydevd; pydevd.settrace()
      
    #####################################################################################
    # Private -- Do not modify this section unless you know what you are doing!         #
    #####################################################################################  
    
    PATH = os.path.abspath(VIZASM_FILEAPTH)
    doc.log('appending %s to search path' % PATH)
    sys.path.append(PATH)
    os.chdir(VIZASM_CWD)
    
    import VizAsm as va
    from vizasm.hopper.hopannotate import hopanno
    from vizasm.Settings import *
    
    seg = doc.getCurrentSegment()
    
    def selected_lines():
        ''' Get the selected lines of the Hopper `Document` '''
        return doc.getRawSelectedLines()
    
    def lines_for_segment(segment):
        ''' Get the lines for the specified `segment` '''
        start_addr = segment.getStartingAddress()
        _range = [start_addr, start_addr + segment.getLength() - 1]
    
        doc.selectAddressRange(_range)
        return selected_lines()
    
    def asmfile_iterator():
        ''' Iterator over the whole asm file  (all segments) '''
        for seg in doc.getSegmentsList():
            seg_it = lines_for_segment(seg)
            for elm in seg_it:
                yield elm
          
    def get_arch_str():
        ''' Get the architecture from Hopper '''
        start_addr = seg.getStartingAddress()
        instr = seg.getInstructionAtAddress(start_addr)
        arch_str = instr.stringForArchitecture(instr.getArchitecture())
        doc.log('architecture: %s' % arch_str)
        return arch_str
    
    # set up annotation
    hopanno.set_seg(seg)
    hopanno.annotate_registers = VIZASM_ANNOTATE_REGISTERS
    hopanno.annotate_calls = VIZASM_ANNOTATE_CALLS
    hopanno.ann_method_head = VIZASM_ANN_METHOD_HEAD
    
    choice = doc.ask('Do you only want to analyze the selected method ? (Y/N)')
    if choice is not None:
        selected_method_only = False
        it = None
        # selection only
        if choice.upper() in ('Y', 'YES', 'JA'):
            it = list(selected_lines())
            selected_method_only = True
        else:
            doc.moveCursorAtEntryPoint()
            it = list(asmfile_iterator())
        arch = Archs.transform_hopper_arch(get_arch_str())
          
       
        # init VizAsm
        filters = va.init(arch, filters = VIZASM_FILTERS, use_all_filters = VIZASM_USE_ALL_STANDARD_FILTERS,
                           verbosity = VIZASM_VERBOSITY.count('v'),
                           quiet = VIZASM_QUIET, graphpath = VIZASM_GRAPH, vlog = VIZASM_LOGFILE, doc = doc)
          
        SETTINGS = {SETTINGS_ASM_FILEPATH: None,
                SETTINGS_OUTPUT_FILEPATH: VIZASM_METHODCALL,
                SETTINGS_GRAPH_FILEPATH: VIZASM_GRAPH,
                SETTINGS_ARCHITECTURE: arch,
                SETTINGS_C_FUNC_HEURISTIC: VIZASM_USE_HEURISTIC_FOR_C_FUNC_CALLS,
                SETTINGS_CNT_SURROUNDING_LINES: VIZASM_CNT_SURROUNDING_LINES,
                SETTINGS_FILTERS : filters,
                SETTINGS_READ_ALL_METHODS : VIZASM_READ_ALL_METHODS,
                SETTINGS_READ_SINGLE_PROCEDURE: selected_method_only,
                SETTINGS_DONT_SKIP_EXCEPTION : VIZASM_DONT_SKIP_EXCEPTION
                }
        set_defaul_settings(SETTINGS)
          
        # run VizAsm
        va.run_hopper(it, superclass_dict = None)
except Exception as e:
    t, v, tb = sys.exc_info()
    doc.log('\n'.join(format_exception(t, v, tb)))
