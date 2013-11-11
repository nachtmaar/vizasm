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

from os.path import abspath
import time

from vizasm.Settings import setting_for_key, SETTINGS_FILTERS, \
    filtering_enabled, SETTINGS_DONT_SKIP_EXCEPTION, SETTINGS_OUTPUT_FILEPATH, \
    SETTINGS_GRAPH_FILEPATH, is_x86, is_x86_64, is_arm
from vizasm.analysis.asm.cpu.AsmRegEx import AsmRegEx
from vizasm.analysis.asm.cpu.arm.Cpu_arm import Cpu_arm
from vizasm.analysis.asm.cpu.exceptions.CpuException import CpuException
from vizasm.analysis.asm.cpu.x86.Cpu_x86 import Cpu_x86
from vizasm.analysis.asm.cpu.x86_64.Cpu_x86_64 import Cpu_x86_64
from vizasm.analysis.security.SecurityAnalyzer import SecurityAnalyzer
from vizasm.hopper.hopannotate import hopanno
from vizasm.model.asm import Segments
from vizasm.model.objc.object.nsobject.objcclass.ObjcClass import ObjcClass
from vizasm.util import Util
from vizasm.util.Log import clilog, log, log_info
from vizasm.vizasm_networkx.GraphUtil import GraphUtil
from vizasm.vizasm_networkx.Graph import Graph


HOPANNO_EXCEPTION_STR = '!! Exception occurred !!'
# length of exception msg (annotated in hopper)
HOPPER_EXCEPTION_LENGTH = 120

class AsmAnalyzerBase(object):
    '''
    Base class for an assembler analyzer.
    Do not forget to set architecture to analyze !
    
    Parameters
    ----------
    superclass_dict: dict<ObjcClass, ObjcClass>, optional (default is {})
        a dictionary holding the base classes as values
    output_file: file
        the opened output file
    graph: Graph
        the `Graph` to which the methodcalls will be added
    _security_analyzer: SecurityAnalyzer
        the `SecurityAnalyzer` which does the filtering
    '''
    def __init__(self, superclass_dict = None):
        if superclass_dict is None:
            superclass_dict = {}
        self._superclass_dict = superclass_dict
        output_file = None
        output_filepath = setting_for_key(SETTINGS_OUTPUT_FILEPATH)
        if output_filepath:
            output_file = open(output_filepath, 'w')
        self._output_file = output_file
        self._graph = Graph()
        
        # do not forget to set `MethodCall` later
        filters = setting_for_key(SETTINGS_FILTERS)
        self._security_analyzer = SecurityAnalyzer(methodcall = None, filters = filters)

    def get_security_analyzer(self):
        return self._security_analyzer

    def set_security_analyzer(self, value):
        self._security_analyzer = value

    def get_graph(self):
        return self._graph

    def set_graph(self, value):
        self._graph = value

    def get_output_file(self):
        return self._output_file

    def set_output_file(self, value):
        self._output_file = value

    def get_superclass_dict(self):
        return self._superclass_dict

    def set_superclass_dict(self, value):
        self._superclass_dict = value

    superclass_dict = property(get_superclass_dict, set_superclass_dict, None, "superclass_dict(dict<ObjcClass, ObjcClass>, optional (default is {})) -- a dictionary holding the base classes as values")
    output_file = property(get_output_file, set_output_file, None, "output_file(file) -- the opened output file")
    graph = property(get_graph, set_graph, None, "graph(Graph) -- the `Graph` to which the methodcalls will be added")        
    security_analyzer = property(get_security_analyzer, set_security_analyzer, None, "security_analyzer(SecurityAnalyzer) -- the `SecurityAnalyzer` which does the filtering")
    
    def filtering_enabled(self):
        ''' Check if filtering is enabled '''
        return filtering_enabled()
    
    def analyze(self):
        ''' Analyze the asm file '''
        raise NotImplementedError
    
    def _analyze(self, methods_it):
        ''' 
        Analyze the assembler file.
        
        Parameters
        ----------
        methods_it: iterator<dict<int, string>>
        '''
        start = time.time()
        AsmAnalyzerBase.__check_dont_skip_exception(setting_for_key(SETTINGS_DONT_SKIP_EXCEPTION))
        
        output_filepath = setting_for_key(SETTINGS_OUTPUT_FILEPATH)
        graph_filepath = setting_for_key(SETTINGS_GRAPH_FILEPATH)
        if output_filepath:
            clilog.info('writing messages to %s' % abspath(output_filepath))
        if graph_filepath is not None:
            clilog.info('writing graph to %s\n' % abspath(graph_filepath))
            
        cnt_filtered_messages = cnt_total_messages = 0
        
        # base classes cannot be resolved 
        if not self.superclass_dict:
            log.critical('No information about superclasses given/read!\n Messages to super cannot be resolved! %s will be assumed as superclass!' % ObjcClass.nsobject)
        
        # create cpu
        cpu = None
        if is_x86():
            cpu = Cpu_x86(self.superclass_dict)
        elif is_x86_64():
            cpu = Cpu_x86_64(self.superclass_dict)
        elif is_arm():
            cpu = Cpu_arm(self.superclass_dict)
        
        try:
            for method_dict in methods_it:
                try:  
                    (cnt1, cnt2) = self.__analyze_inner(cpu, method_dict)
                    cnt_total_messages += cnt1
                    cnt_filtered_messages += cnt2
                except (CpuException, RuntimeError) as e:
                    log.exception(e)
                finally:
                    # reset cpu to read next method implementation
                    cpu.reset()
        except Exception:
            raise
        finally:
            if self.filtering_enabled():
                self.__write_filter_results()
            # close file            
            if self.output_file is not None:
                self.output_file.flush()  
                self.output_file.close()
            GraphUtil.write_gexf(self.graph, graph_filepath)
            
            # print infos
            self._print_info(start, cnt_filtered_messages, cnt_total_messages)

    def _print_info(self, start, cnt_filtered_messages, cnt_total_messages):
        ''' Print some statistics after the file has been analyzed '''
        duration = time.time() - start
        clilog.info("\nfiltered function calls: %d" % cnt_filtered_messages) 
        clilog.info("total number of function calls read: %d" % cnt_total_messages) 
         
        clilog.info('took: %dm, %fs' % (duration / 60, duration % 60))
        clilog.info('done')
        
    def __analyze_inner(self, cpu, method_dict):
        cnt_filtered_messages = cnt_total_messages = 0
        dont_skip_exception = setting_for_key(SETTINGS_DONT_SKIP_EXCEPTION)
        hopper_annotater = hopanno
        hopanno.reset()
        for linenr, line in sorted(method_dict.items()):
            try:
                cpu.read_line(line, linenr)
                if hopper_annotater is not None and hopper_annotater.cur_meth_impl_start is None and cpu.address is not None:
                    hopper_annotater.cur_meth_impl_start = cpu.address
            except (CpuException, RuntimeError) as e:
                # annotate exception
                hopanno.annotate(cpu.address, (HOPANNO_EXCEPTION_STR + (' <- %s: %s ...' % (e.__class__.__name__, str(e))))[:HOPPER_EXCEPTION_LENGTH])
                log.exception(e)
                if not dont_skip_exception:
                    raise
        methodcall = cpu.get_method_call()
        cnt_total_messages += len(methodcall.calls)
        
        sa = self.security_analyzer
        sa.set_methodcall(methodcall)
        
        filtered_methodcall = methodcall
        
        # build a list of method lines
        if self.filtering_enabled():
            # apply filters
            # do this after building the list of method lines, 
            # because the lines before and after refer to the unfiltered lines
            filtered_methodcall = sa.apply_filters()
            
        # method as assembler code (string)
        lines_str_list = list(Util.sorted_dict_values_it(method_dict))
        asm_lines = Util.strlist_to_str(lines_str_list)
        
        # create attribute dictionaries
        methodcall_sender_attr_dict, methodcall_calls_attr_list_dict = methodcall.create_gephi_attr_dicts(asm_lines, filtered_methodcall)
        
        # add to graph
        if self.filtering_enabled():
            sa.add_to_graph(self.graph, methodcall_sender_attr_dict, methodcall_calls_attr_list_dict, sender_methodcall_edge_attr_dict = None)
        else:
            methodcall_sender_attr_dict.update(GraphUtil.viz_dict(size = 50.0))
            methodcall.add_to_graph(self.graph, methodcall_sender_attr_dict, methodcall_calls_attr_list_dict, sender_methodcall_edge_attr_dict = None)
        
        cnt_filtered_messages += len(filtered_methodcall.calls)
        
        # write `MethodCall` to file
        if not self.filtering_enabled():
            self.__write_methodcall(filtered_methodcall)
        
        # annotate hopper
        if hopper_annotater is not None:
            hopper_annotater.annotate_from_methodcall(filtered_methodcall)
            hopper_annotater.reset()
            
        return (cnt_total_messages, cnt_filtered_messages)
    
    def log_n_read_superclasses(self):
        ''' Read and log the superclass information ''' 
        # reading superclasses is only supported for x86_64
        if is_x86_64():
            clilog.info('reading superclasses')
            self.superclass_dict = self.read_superclasses()
            log_info(Util.format_dict_as_table(self.superclass_dict, 'subclass', 'base class'))
            clilog.info('')
    
    def read_superclasses(self):
        ''' 
        Read the super classes from the sections `Segments.SEGMENTS_SUPERCLASS_INFOS`.
        Use `_read_superclasses` for implementation!
        
        Returns
        -------
        dict<ObjcClass, ObjcClass>
            dict with object as key and the superclass as item
        ''' 
        raise NotImplementedError
    
    def _read_superclasses(self, section_it):
        '''
        Helper method for `read_superclasses`.
        
        Parameters
        ----------
        section_it: iterator<tuple<int, string>>
            iterator over the sections where the superclass infos are stored
        '''
        segments = Segments.SEGMENTS_SUPERCLASS_INFOS
        clilog.info('reading from segments %s' % segments)
        superclazz_dict = AsmAnalyzerBase.__read_superclasses_from_sections(section_it)
        return superclazz_dict
        
    @staticmethod
    def __read_superclasses_from_sections(section_it):
        '''
        Read the superclasses from the specified section name 
        
        Parameters
        ----------
        section_it: iterator<tuple<int, string>>
            iterator over the sections where the superclass infos are stored
        
        Returns
        -------
        dict<ObjcClass, ObjcClass>
            dict with object as key and the superclass as item
        '''
        superclasses_dict = {}
        for (_, i) in section_it:
            CLASS_PARENT_MATCH = AsmRegEx.compiled_vre(AsmRegEx.RE_CLASS_PARENT).search(i)
            if CLASS_PARENT_MATCH is not None:
                clazzname = CLASS_PARENT_MATCH.group(AsmRegEx.RE_CLASS_PARENT_GR_CLASS)
                superclazz_name = CLASS_PARENT_MATCH.group(AsmRegEx.RE_CLASS_PARENT_GR_PARENT)
                superclasses_dict[ObjcClass(clazzname)] = ObjcClass(superclazz_name)
        return superclasses_dict
        
    def __write_methodcall(self, methodcall):
        ''' Write the complete (unfiltered) `MethodCall` to file.
        Use if filtering is not enabled. '''
        outputfile = self.output_file
        if not methodcall.is_empty() and outputfile is not None:
            outputfile.write(str(methodcall) + '\n')
    
    def __write_filter_results(self):
        ''' Use if filtering is enabled. Writes the result of the `SecurityFilter`s
        to file ''' 
        outputfile = self.output_file
        if outputfile is not None:
            outputfile.write(self.get_security_analyzer().format_filter_results())
        
    @staticmethod
    def __check_dont_skip_exception(dont_skip_exception):
        ''' Check if option is turned on and warn user ''' 
        if dont_skip_exception:
            clilog.info(
'''"dont_skip_exception" is turned on.
This might lead to wrong results!
If any exception occurs while analyzing a method, the process will be continued!''')
