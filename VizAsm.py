#!/usr/bin/env python
# encoding: utf-8

'''

VizAsm

@author:     Nils Schmidt
        
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

# import os, sys and then append the path of this script to sys.path
# if this is not done in this order or anything will be reorganized this might lead to an error  

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import logging
import os
import sys

PATH = os.path.dirname(os.path.abspath('.'))
sys.path.append(PATH)

from vizasm.Archs import ARCH_X86, ARCH_X86_64, ARCH_ARM
from vizasm.Settings import *
from vizasm.analysis.asm.asmanalyzer.AsmAnalyzerCli import AsmAnalyzerCli
from vizasm.analysis.asm.asmanalyzer.AsmAnalyzerHopper import AsmAnalyzerHopper
from vizasm.analysis.security import SecurityFilters
from vizasm.analysis.security.filter import SecurityFilter
from vizasm.hopper.HopperLoggingHandler import HopperLoggingHandler
from vizasm.util import Util
from vizasm.util.Log import log, clilog, vizasm_add_file_handler, \
    disable_std_loggers, clilog_set_level, \
    get_cli_streamhandler, log_set_level, streamhandler
from vizasm.util.ModuleClassNameException import ModuleNotSameClassNameException

__version__ = '0.1.1'
__date__ = '2013-04-10'
__updated__ = '2014-02-02'
__author__ = 'Nils Schmidt'

DEBUG = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors and print the help menu afterwards'''
    
    def __init__(self, msg, argparser = None):
        super(CLIError).__init__(type(self))
        help_msg = '%s\n' % argparser.format_help() if argparser else '' 
        self.msg = "%sError: %s" % (help_msg, msg)
        
    def __str__(self):
        return self.msg
    
    def __unicode__(self):
        return self.msg

def main(argv = None):  # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_license = '''
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

    try:
        # Setup argument parser
        action_parser = __create_action_parser()
        
        action_args, _ = action_parser.parse_known_args()
        
        # None value indicates to list filters but real value is arch
        list_filters_arch = action_args.list_filters
        if action_args.list_filters is not None:    
            print SecurityFilters.format_available_filters(list_filters_arch)
        else:
            parser = __create_argument_parser(program_license, program_version_message)
            # process arguments
            args = parser.parse_args()

            arch_str = args.arch
            
            filters = init(arch_str, args.filters, args.all_filters, args.verbosity, args.quiet, args.graph, args.vlog, parser)
            # store settings
            asmfile = args.asmfile
            SETTINGS = {SETTINGS_ASM_FILEPATH: asmfile,
                        SETTINGS_OUTPUT_FILEPATH: args.output,
                        SETTINGS_GRAPH_FILEPATH: args.graph,
                        SETTINGS_ARCHITECTURE: arch_str,
                        SETTINGS_C_FUNC_HEURISTIC:args.c_func_heuristic,
                        SETTINGS_CNT_SURROUNDING_LINES: args.surrounding_lines,
                        SETTINGS_FILTERS : filters,
                        SETTINGS_READ_ALL_METHODS : args.read_all_methods,
                        SETTINGS_READ_SINGLE_PROCEDURE :args.read_single_procedure,
                        SETTINGS_DONT_SKIP_EXCEPTION : args.dont_skip_exception
                        }
            set_defaul_settings(SETTINGS)
            if DEBUG:
                print Util.pretty_format_dict(SETTINGS)
            
            # run program
            clilog.info('architecture: %s' % arch_str)
            clilog.info('analyzing file %s ...\n' % asmfile)
            
            asm_ana = AsmAnalyzerCli()
            asm_ana.analyze()                
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except CLIError as e:
        clilog.exception(e)        
    except Exception, e:
        log.exception(e)
        clilog.exception(e)
        return 2

def run_hopper(asmfile_iterator, superclass_dict = None):    
    '''
    Use this method to run VizAsm from Hopper.
    
    Parameters
    ----------
    asmfile_iterator: iterator<tuple<int, string>>
        iterator over the lines
    superclass_dict: dict<ObjcClass, ObjcClass>, optional (default is {})
        a dictionary holding the base classes as values
    '''
    # run program
    asm_ana = AsmAnalyzerHopper(asmfile_iterator, superclass_dict = superclass_dict)
    clilog.info('Hopper reads the whole asm file into memory first and freezes while its doing this. So do not wonder!')
    asm_ana.analyze()

def init(arch, filters = None, use_all_filters = False, verbosity = 0, quiet = False, graphpath = None, vlog = None, parser = None, doc = None):
    ''' 
    Use to configure logging, do a few checks and load the filters.
    
    Parameters
    ----------
    arch_str: string (see `Archs`)
        architecture
    filters: list<str>, optional (default is None and disables filtering)
    use_all_filters: bool, optional (default is False)
    verbosity: int, optional (default is 0)
        the verbosity level ( 0 <= v <= 4, 0 -> CRITICAL, 1 -> ERROR, 2 -> WARN, 3 -> INFO, 4 -> DEBUG)
    quiet: bool, optional (default is False)
        if nothing shall be logged (does not affect file logging)
    graphepath: string, optional (default is None and disables graph writing)
        where to write the graph, if None do not write
    vlog: str, optional (default is None and disables logging to file)
        filename of the logging file
    argparser: ArgumentParser, optional (default is None)
    doc: Document
        The Hopper Document. If given log to Hopper.

    Raises
    ------
    CLIError
    
    Returns
    -------
    filters: list<SecurityFilter>
        list of loaded filters
    '''
    if verbosity < 0 or verbosity > 4:
        raise CLIError('Verbosity has to be 0 <= v <= 4, is: %d' % verbosity)
    __configure_logging(quiet, verbosity, vlog, doc)
    if graphpath is not None:
        __check_graph_file_extensions(graphpath, parser)
    
    flist = __load_filters(filters, use_all_filters, arch)
    # if filter list is empty, disable filtering
    if not flist:
        flist = None
    return flist
    
def __create_action_parser():
    ''' Creates the action parser which is intended to be used for actions that do not require the positional arguments '''
    action_parser = ArgumentParser(add_help = False)
    # architecture
    
    action_parser.add_argument("-lf", "--list-filters", dest = 'list_filters', help = "show available filters")
    return action_parser

def __create_argument_parser(program_license, program_version_message):
    ''' Creates the argument parser '''
    parser = ArgumentParser(description = program_license, formatter_class = RawDescriptionHelpFormatter)
    # positional arguments
    parser.add_argument("asmfile", help = "the .asm file you want to analyze")
    
    # architecture
    parser.add_argument("arch", choices = (ARCH_X86, ARCH_X86_64, ARCH_ARM), help = "set the architecture")
    
    # optional arguments
    parser.add_argument("-o", "--output", dest = "output", help = "the file to which the read methods will be written")
    parser.add_argument("-ram", "--read-all-methods", dest = "read_all_methods", action = 'store_true', help = "read all methods (not only Objective-C ones)")
    parser.add_argument("-rsp", "--read-single-procedure", dest = "read_single_procedure", action = 'store_true', help = "use if the asm file only contains of a single procedure and does not have any section. ")
    parser.add_argument("-dse", "--dont-skip-exception", dest = "dont_skip_exception", action = 'store_true', default = False, help = "if enabled the analysis of the current method will not be skipped if any exception occurs [default: %(default)s]")
    parser.add_argument("-cfh", "--c-func-heuristic", dest = "c_func_heuristic", action = 'store_true', default = False, help = "use a heuristic to determine the arguments for a c function call (~2x slower) [default: %(default)s]")
    
    # graph stuff
    graphgr = parser.add_argument_group('graph')
    graphgr.add_argument("-g", "--graph", dest = "graph", help = "filename of the graph in gexf file format, do not forget the .gexf extension !")
    graphgr.add_argument("-C", "--context", dest = "surrounding_lines", default = 5, help = "show number of surrounding lines (lines after and before actual match) in graph [default: %(default)s], only in use with filters!")
    
    # logging stuff
    log = parser.add_argument_group('logging')
    log.add_argument("-q", "--quiet", dest = "quiet", action = "store_true", default = False, help = "be quiet and do not log anything to stdout")
    log.add_argument("-v", "--verbose", dest = "verbosity", action = "count", default = 0, help = "set verbosity [default: %(default)s],  0 -> CRITICAL, 1 -> ERROR, 2 -> WARN, 3 -> INFO, 4 -> DEBUG")
    log.add_argument("-vl", "--verbose-log", dest = "vlog", help = "log to file")
    
    # filter stuff
    filtergr = parser.add_argument_group('filter')
    filtergr.add_argument("-lf", "--list-filters", dest = 'list_filters', action = 'store_true', help = "show available standard filters (%s)" % ', '.join(Archs.ARCHS))
    filtergr.add_argument("-af", "--all-filters", dest = 'all_filters', action = 'store_true', help = "use all standard filters")
    filtergr.add_argument("-sf", "--supply-filters", dest = 'filters', nargs = '+', help = "supply own filters (has to be last argument)")
    
    parser.add_argument('-V', '--version', action = 'version', version = program_version_message)
    return parser
        
        
def __configure_logging(quiet, verbosity, logger_filename, doc = None):
    '''
    Configure the logging.
    
    If quiet, the logger will only log with the specified verbosity level to file (if given).
    
    If not quiet, the verbosity will be forwarded to the logger 
    
    Parameters
    ----------
    quiet: boolean
        if nothing shall be logged (does not affect file logging)
    verbosity: int
        the verbosity level
    logger_filename: str
        filename of the logging file
    doc: Document
        The Hopper Document. If given log to Hopper.
    '''
    LOG_LEVEL = logging.CRITICAL
    if verbosity is not None:
        if verbosity == 1:
            LOG_LEVEL = logging.ERROR
        elif verbosity == 2:
            LOG_LEVEL = logging.WARN
        elif verbosity == 3:
            LOG_LEVEL = logging.INFO
        elif verbosity >= 4:
            LOG_LEVEL = logging.DEBUG
            
    # hopper logging via doc.log()
    if doc is not None:
        clilog.addHandler(HopperLoggingHandler(doc = doc))
        log.addHandler(HopperLoggingHandler(doc = doc))
        doc.log('added Hopper LoggingHandler ...')
    else:
        clilog.addHandler(get_cli_streamhandler())
        log.addHandler(streamhandler)
        
    if quiet:
        disable_std_loggers()        
    else:
        log_set_level(LOG_LEVEL)
        clilog_set_level(logging.INFO)
        
    # write to file with specified log level
    vizasm_add_file_handler(logger_filename, LOG_LEVEL)
    
def __check_graph_file_extensions(graph_filename, argparser = None):
    ''' Check the extension of the graph file. Must be ".gexf"
    
    Parameters
    ----------
    graph_filename: str
        the name of the file to which the graph will be written 
    argparser: ArgumentParser, optional (default is None)
    
    Raises
    ------
    CLIError
        if the file does not end with ".gexf"
     '''
    if not graph_filename.endswith('.gexf'):
        raise CLIError('The graph file must end with .gexf!', argparser)        

def __load_filters(filtername_list, use_all_std_filters, arch):
    ''' 
    Load all standard filters as well as the user supplied ones.
    They are assumed to be in the directory where the `SecurityFilter` class is located.
    
    Parameters
    ----------
    filtername_list: list<str>
        list of filter names
    use_all_std_filters: boolean
        load all standard filters
    arch_str: string (see `Archs`)
        architecture    
    Returns
    -------
    installed_filters: list<SecurityFilter>
        all loaded filters
    []
        if no filter has been loaded
    '''
    flist = []
    if filtername_list:
        flist = []
        for f in filtername_list:
            base_fqn = SecurityFilter.__package__
            f = '%s.%s' % (base_fqn, Util.remove_py_extension(f))
            try:
                clazz = Util.class_for_fqn_mod_eq_class(f) 
                fclass = clazz()
                flist.append(fclass)
            except (ImportError, ModuleNotSameClassNameException) as e:
                raise CLIError(str(e)), None, sys.exc_info()[2]
    if use_all_std_filters:
        # use all standard filters
        # do not take duplicates
        flist = list(set(map(lambda f: f(), SecurityFilters.security_filters(arch)) + flist))
    fnames = map(lambda f: f.name, flist)
    if not fnames:
        clilog.info('no filters enabled')
    else:
        clilog.info('installed filters: %s' % ', '.join(fnames))
    return flist

if __name__ == "__main__":
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'vizasm.Main_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream = statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
