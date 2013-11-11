'''
VizAsm

Created on 27.03.2013

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

import sys

from vizasm.analysis.asm.cpu.AsmRegEx import AsmRegEx
from vizasm.hopper.HopperAnnotationInterface import HopperAnnotationInterface
from vizasm.model.objc.AsmParserInterface import AsmParserInterface
from vizasm.model.objc.arguments.Arguments import Arguments
from vizasm.model.objc.arguments.ArgumentsOverloadedException import \
    ArgumentsOverloadedException
from vizasm.model.objc.arguments.ArgumentsUnderloadedException import \
    ArgumentsUnderloadedException


class SelectorOverloadedException(ArgumentsOverloadedException):
    ''' Indicates that the selector has more arguments than it needs! '''
    
    
class SelectorUnderloadedException(ArgumentsUnderloadedException):
    ''' Indicates that the selector has less arguments than it needs! '''
    
class Selector(Arguments, AsmParserInterface, HopperAnnotationInterface):
    ''' 
    Represents an objective-c selector
     
    Parameters
    ----------
    selector_name: string
        the name of the selector (mapped to objc_name)
     '''
    
    SELECTOR_DELIMITER = ':'
    SELECTOR_INIT = 'init'
    SELECTOR_ALLOC = 'alloc'
    SELECTOR_NEW = 'new'
    SELECTOR_RETAIN = 'retain'
    SELECTOR_RELEASE = 'release'
    SELECTOR_AUTORELEASE = 'autorelease'
    
    def __init__(self, name, arguments = None, is_static = False):   
        if arguments is None:
            arguments = []
        Arguments.__init__(self, name, arguments, is_static)

    def __hash__(self):
        return Arguments.__hash__(self)

    def __eq__(self, other):
        return Arguments.__eq__(self, other)

    def get_selector_name(self):
        return self.get_objc_name()
    
    def set_selector_name(self, selname):
        self.set_objc_name(selname)
        
    def __str__(self):
        try:
            return self.__selector_filled_with_arguments_description()
        except RuntimeError:
            return self.get_obj_name()
    
    def __repr__(self):
        return '%s(%s, max. args: %d, arguments: %s' % (self.__class__.__name__, self.get_objc_name(), self.cnt_needs_arguments(), self.get_arguments())
    

    def __selector_filled_with_arguments_description(self):
        ''' 
        Return the selector if no arguments are available. 
        Otherwise return the selector filled with the arguments after each delimiter.
        If no argument is available n/a is used 
        
        Raises
        ------
        RuntimeError
            
        Returns
        -------
        string 
        '''
        selname = self.get_selector_name()
        # no argument available
        if self.cnt_needs_arguments() is 0:
            return selname
        # fill selector with arguments
        res = ''
        sel_split = self.sub_selectors()
        # remove stuff after last split
        sel_split.pop()
        for idx, sel in enumerate(sel_split):
            argument = self.get_argument_at_idx(idx)
            # add whitespace between splitted selectors, but not at end
            space = '' if idx is (self.cnt_needs_arguments() - 1) else ' '
            if argument is None:
                argument = 'n/a'
            arg_str = argument.__str__()
            res += sel + Selector.SELECTOR_DELIMITER + arg_str + space
        return res
    
    def add_argument(self, argument):
        ''' 
        Add an argument to the selector
         
        Raises
        ------
        SelectorOverloadedException
            if selector has more arguments than it needs
        '''
        try:
            Arguments.add_argument(self, argument)
        except ArgumentsOverloadedException:
            raise SelectorOverloadedException(self, argument), None, sys.exc_info()[2]
    
    def get_argument_at_idx(self, idx):
        ''' Return the argument at specified idx. If not found None will be returned '''
        if idx < self.cnt_has_arguments():
            return self.get_arguments()[idx]
        return None
   
    def sub_selectors(self):
        ''' Get a list of sub selector names '''
        return self.get_selector_name().split(Selector.SELECTOR_DELIMITER)
    
    def is_alloc(self):
        ''' Return if the selectorname is alloc '''
        return self.get_selector_name() == Selector.SELECTOR_ALLOC
   
    def is_kind_of_init(self):
        ''' Return if the selectorname begins with init '''
        return self.get_selector_name().find(Selector.SELECTOR_INIT) != -1
    
    def is_init(self):
        ''' Return if the selectorname is init '''
        return self.get_selector_name() == Selector.SELECTOR_INIT
    
    def is_new(self):
        ''' Return if the selectorname is new '''
        return self.get_selector_name().find(Selector.SELECTOR_NEW) != -1
    
    def is_retain(self):
        ''' Return if the selectorname is retain '''
        return self.get_selector_name() == Selector.SELECTOR_RETAIN
    
    def is_release(self):
        ''' Return if the selectorname is release '''
        return self.get_selector_name() == Selector.SELECTOR_RELEASE
    
    def is_autorelease(self):
        ''' Return if the selectorname is autorelease '''
        return self.get_selector_name() == Selector.SELECTOR_AUTORELEASE
    
    def does_retain(self):
        ''' Return if the selector increments the retain count '''
        return self.is_alloc() or self.is_new() or self.is_retain()
    
    def does_release(self):
        ''' Return if the selector decrements the retain count '''
        return self.is_release() or self.is_autorelease()
    
    def is_retain_count_important(self):
        ''' Return if the selector has an impact on the retain count '''
        return self.does_retain() or self.does_release()
    
    def fill_from_cpu(self, cpu, register_list = None):
        ''' 
        Fill the arguments of the selector from cpu (registers and stack)
        
        Parameters
        ----------
        register_list
            the list of register from which to fill (if None is passed, the default register list is used `Cpu.selector_arg_registers()`) 
    
        Raises
        ------
        SelectorUnderloadedException
            raised if more arguments than needed came from the cpu
        SelectorOverloadedException
            raised if not enough arguments came from the cpu
        '''
        if register_list is None:
            register_list = cpu.selector_arg_registers()
        try:
            Arguments.fill_from_cpu(self, cpu, register_list)
        except ArgumentsOverloadedException as e:
            raise SelectorOverloadedException(self, e._new_argument), None, sys.exc_info()[2]
        except ArgumentsUnderloadedException as e:
            raise SelectorUnderloadedException(self, cpu), None, sys.exc_info()[2]
        
               
    def _fill_remaining_args_from_stack(self, cpu):
        ''' 
        Fill the arguments of the selector from cpu stack
    
        Raises
        ------
        SelectorOverloadedException
            raised if more arguments than needed came from the stack of the cpu 
        SelectorUnderloadedException
            raised if not enough arguments came from the stack of the cpu
        '''
        try:
            Arguments._fill_remaining_args_from_stack(self, cpu)
        except ArgumentsOverloadedException as e:
            raise SelectorOverloadedException(self, e._new_argument), None, sys.exc_info()[2]
        except ArgumentsUnderloadedException:
            raise SelectorUnderloadedException(self, cpu), None, sys.exc_info()[2]
    
    def set_argument_for_sub_selector(self, subsel_name, argument):
        ''' Set the argument for the sub selector.
        
        Parameters
        ----------
        subsel_name: string
            name of the sub selector
        argument: object
            the argument to set for the sub selector
       '''
        sub_sels = self.sub_selectors()
        for idx, sub_sel in enumerate(sub_sels):
            if sub_sel == subsel_name:
                self.get_arguments()[idx] = argument
            
    def get_argument_for_sub_selector(self, subsel_name):
        ''' Get the argument for the sub selector.
        
        Parameters
        ----------
        subsel_name: string
            name of the sub selector
       '''
        sub_sels = self.sub_selectors()
        for idx, sub_sel in enumerate(sub_sels):
            if sub_sel == subsel_name:
                try:
                    return self.get_arguments()[idx]
                except IndexError:
                    return None
            
    @staticmethod
    def selector_from_delimiter(selectorname, delimiter = '_'):
        ''' 
        Return a Selector from a string like e.g. get_arg1_arg2_ where "_" is the delimiter 
        
        Parameters
        ----------
        selectorname: string
            selectorname like get_arg1_arg2_ 
        delimiter: string, optional
            delimits the selector (default is "_")
        '''
        selectorname = selectorname.replace(delimiter, Selector.SELECTOR_DELIMITER)
        return Selector(selectorname)
    
    @staticmethod
    def selector_from_underscore_delimiter(selectorname):
        ''' Return a Selector from a string like e.g. get_arg1_arg2_ where "_" is the delimiter '''
        return Selector.selector_from_delimiter(selectorname, delimiter = '_')
    
    def cnt_needs_arguments(self):
        ''' return the number of arguments the selector takes indicated by the number of ":" in the selector name '''
        return self.get_objc_name().count(Selector.SELECTOR_DELIMITER)
    
    def cnt_has_arguments(self):
        ''' 
        Return the number of arguments the selector has. 
            This is not the number of arguments the selector really (see cnt_needs_arguments()) needs! '''
        return len(self.get_arguments())
    
    selector_name = property(get_selector_name, set_selector_name, None, 'selector_name -- the name of the selector (mapped to objc_name)')

#####################################################################################
# AsmParserInterface                                                                #
#####################################################################################    
    @staticmethod
    def create_from_asm_line(asmline):
        ''' Create Selector from asm line like e.g. @selector(objectForKey:) '''
        selector_match = AsmRegEx.compiled_vre(AsmRegEx.RE_SELECTOR).search(asmline) 
        if selector_match is not None:
            selector = Selector(selector_match.group(AsmRegEx.RE_SELECTOR_GR_SELECTOR))
            return selector
        return None
    
#####################################################################################
# HopperAnnotationInterface                                                         #
#####################################################################################    

    def hopper_str(self):
        return '%s(%s)' % (self.__class__.__name__, self.get_objc_name())
    
if __name__ == '__main__':
    sel = Selector('objectForKey:')
    try:
        sel.add_argument('default1')
        sel.add_argument('default2')
    except SelectorOverloadedException as soe:
        print soe
    
    print sel

    selissel = Selector('objectForKey:')
    seldnargs = Selector('objectForKey::')
    seldname = Selector('standardUserDefaults:')
    print 'same address should be equal: %s' % (sel == sel)
    print 'equal sels should be equal: %s' % (sel == selissel)
    print 'unequal sel number of arguments should not be equal: %s' % (sel == seldnargs)
    print 'unequal sel name should not be equal: %s' % (sel == seldname)

    sel2 = Selector.create_from_asm_line('qword [ds:objc_sel_selfMethod] ; @selector(selfMethod)')
    print sel2
    print
    sel3 = Selector('obj1:obj2:obj3:obj4:', ['1', '2', '3'])
    print sel3
    
    underscore_sel = Selector.selector_from_underscore_delimiter('applicationDidFinishLaunching_')
    print underscore_sel
    
    print selissel == Selector('objectForKey:')
    
    alloc = Selector('alloc')
    init = Selector('init')
    print 'is_alloc: %s' % (alloc.is_alloc())
    print 'is_init: %s' % (init.is_kind_of_init())
