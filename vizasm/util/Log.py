'''
VizAsm

Created on 04.04.2013

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

import logging
import sys

def get_cli_streamhandler():
    format_str = "%(message)s" 
    clilog_formatter = logging.Formatter(format_str)
    clilog_handler = logging.StreamHandler(sys.stdout)
    clilog_handler.setLevel(logging.INFO)
    clilog_handler.setFormatter(clilog_formatter)
    return clilog_handler


LEVEL_NOLOG = logging.CRITICAL + 1
log = logging.getLogger("vizasm")
log.setLevel(logging.DEBUG)

vizasm_format_str = "%(name)s:%(levelname)s:%(module)s.%(funcName)s:%(message)s"

clilog = logging.getLogger('cli_info_logger')
clilog.setLevel(logging.INFO)

def __get_log_steamhandler():
    formatter = logging.Formatter(vizasm_format_str)
    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(logging.DEBUG)
    streamhandler.setFormatter(formatter)
    return streamhandler

streamhandler = __get_log_steamhandler()

def clilog_set_level(log_level):        
    clilog.setLevel(log_level)

def log_set_level(log_level):
    log.setLevel(log_level)
    
def vizasm_add_file_handler(filename, loglevel):
    if filename is not None:
        handler_file = logging.FileHandler(filename)
        hff = logging.Formatter(vizasm_format_str)
        handler_file.setLevel(loglevel)
        handler_file.setFormatter(hff)
        log.addHandler(handler_file)
    
def disable_logger(logger):
    logger.setLevel(LEVEL_NOLOG)
    
def disable_std_loggers():
    disable_logger(log)
    disable_logger(clilog)

def log_info(msg):
    ''' Log with `clilog` and `log` (info level) ''' 
    _log_with_level(logging.INFO, msg)
    
def log_critical(msg):
    ''' Log with `clilog` and `log` (critical level) ''' 
    _log_with_level(logging.CRITICAL, msg)
    
def _log_with_level(level, msg):
    ''' Log with `clilog` and `log` ''' 
    clilog.log(level, msg)
    log.log(level, msg)
    
def log_exception(exception):
    ''' Log exception with `clilog` and `log` ''' 
    clilog.exception(exception)
    log.exception(exception)
