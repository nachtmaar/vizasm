'''
VizAsm

Created on 11.04.2013

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

from vizasm.analysis.asm.cpu.AsmRegEx import AsmRegEx as anare
from vizasm.reader.asm.AsmRegEx import AsmRegEx
from vizasm.util.Log import log


class AsmReader(object):
    ''' 
    Reader for an asm file.

    Parameters
    ----------
    __abs_file_path: string
        absolute file path of the asm file 
    __file_obj: file
        the opened file object
    '''
    
    def __init__(self, file_path):
        self.__abs_file_path = abspath(file_path)
        # set None to use the `reopen_file` method
        self.__file_obj = None
        log.debug('file path: %s' % (self.get_abs_file_path()))
        self.reopen_file()
        
    def __del__(self):
        self.close_file()
        
    def reopen_file(self):
        ''' Reopen the file '''
        self.close_file()
        self.__file_obj = open(self.get_abs_file_path(), 'r')

    def close_file(self):
        ''' Close the current opened file '''
        # close file
        file_obj = self.file_obj
        if file_obj is not None:
            file_obj.close
        
    def get_file(self):
        return self.__file_obj

    def set_file(self, value):
        self.__file_obj = value
        
    def get_abs_file_path(self):
        return self.__abs_file_path

    def set_abs_file_path(self, value):
        self.__abs_file_path = value

    abs_file_path = property(get_abs_file_path, set_abs_file_path, None, "__abs_file_path(string) -- absolute file path of the asm file")
    file_obj = property(get_file, set_file, None, "__file_obj(file) -- the opened file object")
    
    @staticmethod
    def sections_it(file_iterator, section_list):
        ''' 
        Read the lines for the specified sections.
        Returns an iterator over the lines and line numbers.  
        
        Text before the first occurrence of the specific section is omitted ! 
        
        Parameters
        ----------
        file_iterator: iterator<string>
            iterator over the asm file
        section_list: list<str>
            list of section names
        
        Returns
        -------
        iterator<tuple<int, string>>
            the sections
        empty iterator
            if an io error occurred
        '''
        try:
            section_re = AsmRegEx.compiled_vre(AsmRegEx.RE_SECTION)
            sections_found = []
            cur_section = None
            for linenr, line in enumerate(file_iterator, 1):
                section_match = section_re.search(line)
                if section_match is not None:
                    cur_section = section_match.group(AsmRegEx.RE_SECTION_GR_SECTION)
                    # all sections found ?
                    sections_found = section_list == sections_found
                    if cur_section in section_list and not sections_found:
                        sections_found = True
                    # iterated over all sections -> done
                    elif sections_found:
                        return 
                if sections_found:
                    yield (linenr, line.rstrip())
        except IOError as e:
            log.critical(e)
            
    @staticmethod
    def methods_it(file_iterator, read_all_procedures = False):
        '''
        Returns an iterator running over the methods.
        For each method a dictionary is yield with the line number as key and the method line as value. 
        
        Parameters
        ----------
        read_all_procedures: boolean, optional (default is False)
            If True, all procedures will be read.
            If False, only those recognized as a `CategoryClass` or method implementation
            will be read. 
            See `AsmRegEx.is_method_implementation` for details.
        file_iterator: iterator<tuple<int, string>>
            the iterator to use
              
        Returns
        -------
        method_dict iterator: iterator<dict<int, string>>
        '''
        re_procedure = AsmRegEx.compiled_re(AsmRegEx.RE_PROCEDURE)
        # list of lines of the current method
        method_dict = {}
        first_method_found = False
        
        def init_proper_method():
            ''' indicates if the method is a method implementation or a category method '''
            return True if read_all_procedures else False
        
        proper_method = init_proper_method()
        
        first_method_fix = False
        for linenr, line in file_iterator:
            procedure_match = re_procedure.search(line)
            # `sections_it` cuts the lines before the first occurrence of section
            # use this pattern to detect first method anyway
            if not first_method_fix:
                first_method_fix = line.find('; Section') != -1
            # check if proper method
            if not read_all_procedures and not proper_method:
                proper_method = any((anare.is_method_implementation(line), anare.is_entrypoint(line)))
            # procedure found
            if procedure_match is not None:
                # not the first method_dict
                if proper_method:
                        yield method_dict
                method_dict = {}
                first_method_found = True
                proper_method = init_proper_method()
            # start collecting the lines of a method after the first method pattern has been found
            if first_method_found or (first_method_fix and proper_method):            
                method_dict.update({linenr : line})
        # yield rest
        if proper_method and method_dict:
            yield method_dict
    
    @staticmethod       
    def linenr_it(it):
        '''
        Returns an iterator counting the lines.
        
        Parameters
        ----------
        it: iterator<str>
            the iterator to add line numbers to
            
        Returns
        -------
        method_dict: iterator<tuple<int, string>>
        '''
        for linenr, line in enumerate(it, 1):
            yield linenr, line.rstrip()
        
    @staticmethod       
    def single_method_it(it):
        '''
        Returns an iterator running over a single method/procedure.
        Yields a dictionary with the line number as key and the method line as value. 
        
        Parameters
        ----------
        it: iterator<str>
            iterator over the procedure lines
            
        Returns
        -------
        method_dict: iterator<dict<int, string>>
        '''
        method_dict = {}
        for linenr, line in enumerate(it, 1):
            method_dict.update({linenr: line.rstrip()})
        yield method_dict
            
    def single_method_it_asm_file(self):
        '''
        Returns an iterator running over a single method/procedure from the asm file.
        Yields a dictionary with the line number as key and the method line as value. 
        
        Returns
        -------
        method_dict: iterator<dict<int, string>>
        '''
        file_obj = None
        try:
            self.reopen_file()
            file_obj = self.file_obj
            return AsmReader.single_method_it(file_obj)
        except IOError as e:
            log.critical(e)
        
if __name__ == '__main__':
    filename = '../../../files/asm/x86_64/method/CocoaObjectCallSelfMethodArg.asm'
    # filename = 'test_data/CocoaObjectCallSelfMethodArgNSLog.asm'
    asmreader = AsmReader(filename) 
    methods_it = asmreader.section_text_method_it(read_all_procedures = False)
    for method in methods_it:
        for linenr, line in sorted(method.items()):
            print '%d: %s' % (linenr, line)
        print
        pass
    # meth_impls = asmreader.read_methods()
