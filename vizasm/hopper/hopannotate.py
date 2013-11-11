'''
VizAsm

Created on 19.08.2013

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

from vizasm.hopper.HopperAnnotationInterface import HopperAnnotationInterface as hai

class HopperAnnotater(object):
    '''
    This class is used for annotating Hopper.
    Be sure to set `seg`. This is the bridge to Hopper needed for annotation.
    Set it before you annotate anything.
    
    The first time this module gets imported, an instance of `HopperAnnotater` will be created and stored in `hopanno`.
    
    Parameters
    ----------
    __cur_meth_impl_start: int
        The address of the method implementation. Has to be set externally.
    __seg: Segment (see Hopper scripting api)
        object of Hopper which holds the function for annotation
    __not_annotated_registers_list: list<tuple<str, int>>
        if the annotation of registers is enabled, 
        all registers that will be annotated are stored in this list and annotated if `clear()` gets called. 
        Messages with None address, will be annotated at the method head.
    __annotate_calls: bool, optional (default is False)
        enable annotation of calls
    __annotate_assignments: bool, optional (default is False)
        enable annotation of registers
    __ann_method_head: bool, optional (default is False)
        write a summary to the beginning of the method implementation.
    '''
    
    def __init__(self, seg = None, annotate_calls = False, ann_method_head = False, annotate_assignments = False):
        self.__cur_meth_impl_start = None
        self.__seg = seg
        self.__not_annotated_registers_list = []
        self.__annotate_calls = annotate_calls 
        self.__annotate_assignments = annotate_assignments
        self.__ann_method_head = ann_method_head 

    def __str__(self):
        return repr(self) 
    
    def __repr__(self):
        return '%s(%s, %s, %s, %s)' % (self.__class__.__name__, self.seg, self.annotate_calls, self.ann_method_head, self.annotate_registers)

    def is_hopper_annotation_enabled(self):
        ''' Check if annotation is enabled.
        To enable it, set the `seg` value.
        '''
        return self.seg is not None
    
    def get_ann_method_head(self):
        return self.__ann_method_head

    def get_not_annotated_registers_list(self):
        return self.__not_annotated_registers_list

    def set_not_annotated_registers_list(self, value):
        self.__not_annotated_registers_list = value

    def set_ann_method_head(self, value):
        self.__ann_method_head = value
    
    def get_seg(self):
        return self.__seg

    def set_seg(self, value):
        self.__seg = value

    def get_cur_meth_impl_start(self):
        return self.__cur_meth_impl_start

    def set_cur_meth_impl_start(self, value):
        self.__cur_meth_impl_start = value
    
    def get_annotate_calls(self):
        return self.__annotate_calls

    def set_annotate_calls(self, value):
        self.__annotate_calls = value

    def get_annotate_registers(self):
        return self.__annotate_assignments
    
    def set_annotate_registers(self, value):
        self.__annotate_assignments = value
        
    def annotate_from_methodcall(self, methodcall):
        '''
        Annotate the calls stored in the `MethodCall`.
        If `ann_method_head` write a summary of the calls to the beginning of the method implementation.
        
        The hopper representation will be used if available (see `HopperAnnotationInterface`)
         
        Parameters
        ----------
        methodcall: MethodCall
            the `MethodCall` to annotate
        '''
        if self.is_hopper_annotation_enabled() and self.annotate_calls:
            methods = ''
            for methodcallitem in methodcall:
                int_addr = methodcallitem.address
                msg = hai.try_get_hopper_string(methodcallitem.call)
                methods += msg + '\n'
                self.annotate(int_addr, msg)
    
            if self.ann_method_head and self.cur_meth_impl_start is not None:
                head_msg = '\n' + methodcall.format_head() + '\n' + methods
                self.annotate_method_head_beginning(head_msg)
            
    def annotate_assignment(self, lval, rval, address):
        '''
        Annotate the current assignments (if enabled)
        E.g. annotate the current register value.
        
        The messages will not get annotated instantly.
        They will be collected and annotated at once if `clear()` gets called.
        Seems to improve performance. 
        
        The hopper representation will be used if available (see `HopperAnnotationInterface`)
        
        Parameters
        ----------
        lval: object
            left value of the assignment
        rval: object
            right value of the assignment
        address: int
        ''' 
        if self.is_hopper_annotation_enabled():
            register_hop, value_hop = hai.try_get_hopper_string(lval), hai.try_get_hopper_string(rval)
            msg = '%s = %s' % (register_hop, value_hop)
            self.annotate_other_assignment(msg, address)
            
    def annotate_other_assignment(self, msg, address):
        '''
        Annotate the current assignment (if enabled).
        E.g. annotate the current register value.
        
        The messages will not get annotated instantly.
        They will be collected and annotated at once if `clear()` gets called.
        Seems to improve performance. 
        
        The hopper representation will be used if available (see `HopperAnnotationInterface`)
        
        Parameters
        ----------
        address: int
        msg: string
        ''' 
        if self.is_hopper_annotation_enabled():
            msg = hai.try_get_hopper_string(msg)
            if self.annotate_registers:
                self.not_annotated_registers_list.append((msg, address))
    
    def annotate_assignment_method_head(self, msg):    
        '''
        Annotate the current assignment at the method head.
        
        The messages will not get annotated instantly.
        They will be collected and annotated at once if `clear()` gets called.
        Seems to improve performance. 
        
        Parameters
        ----------
        msg: string
        ''' 
        if self.is_hopper_annotation_enabled():
            self.not_annotated_registers_list.append((msg, None))
        
    def annotate(self, address, msg):
        ''' 
        Annotate the specified message at given address if not None.
        
        Parameters
        ----------
        msg: str
        address: int

        '''
        if self.is_hopper_annotation_enabled() and address is not None:
            seg = self.seg
            comment = str(msg)
            seg.setCommentAtAddress(address, comment)
            
    def annotate_inline(self, address, msg, keep_orig_msg = False):
        ''' 
        Annotate the specified message inline at given address if not None.
        
        Parameters
        ----------
        msg: str
        address: int
        keep_orig_msg: bool, optional (default is False)
            if True keep the original message in new comment
        '''
        if self.is_hopper_annotation_enabled() and address is not None:
            seg = self.seg
            old_comment = seg.getInlineCommentAtAddress(address) if keep_orig_msg and isinstance(address, int) else None
            comment = str(msg)
            if old_comment is not None:
                comment = '%s - %s' % (comment, old_comment)
            seg.setInlineCommentAtAddress(address, comment)
    
    def annotate_method_head_beginning(self, msg):
        '''
        Annotate at beginning of the meth_impl head.
        
        Parameters
        ----------
        msg: str
        '''
        self.__annotate_method_head(msg, end = False)
    
    def annotate_method_head_end(self, msg):
        '''
        Annotate at end of the meth_impl head.
        
        Parameters
        ----------
        msg: str
        '''
        self.__annotate_method_head(msg, end = True)
    
    def __annotate_method_head(self, msg, end = True):
        ''' Annotate the head of the meth_impl.
        
        Parameters
        ----------
        msg: str
        end: bool
            if true annotate at end of head, otherwise at the beginning
        '''
        if self.is_hopper_annotation_enabled() and self.ann_method_head:
            method_head_addr = self.cur_meth_impl_start
            cur_head_msg = self.__get_current_head_msg()
            if method_head_addr is not None:
                head_msg_it = [msg]
                if cur_head_msg:
                    if end:
                        head_msg_it.insert(0, cur_head_msg)
                    else:
                        head_msg_it.append(cur_head_msg)
                head_msg = '\n'.join(head_msg_it)
                self.annotate(method_head_addr, head_msg)

    def __get_current_head_msg(self):
        ''' Get the current head msg as string. Returns an empty string if not set (None). '''
        method_head_addr = self.cur_meth_impl_start
        cur_head_msg = ''
        if method_head_addr is not None:
            head_msg = self.seg.getCommentAtAddress(method_head_addr)
            if head_msg is not None:
                cur_head_msg = head_msg
        return cur_head_msg
    
    def reset(self):
        ''' Reset and annotate all messages which have not been annotated '''
        head_address = self.cur_meth_impl_start
        ann_method_head = []
        # annotate messages that have an address and store the others in ann_method_head
        for msg, addr in self.not_annotated_registers_list:
            address = addr
            if address is None:
                ann_method_head.append(msg)
            else:
                self.annotate_inline(address, msg, keep_orig_msg = True)
        # annotate messages that had no address at head (if head address set)
        if head_address is not None and ann_method_head:
            self.annotate_method_head_end('\n'.join(ann_method_head))
        # clear
        self.clear()
        
    def clear(self):
        ''' Clear the system '''
        self.__init__(self.seg, self.annotate_calls, self.ann_method_head, self.annotate_registers)
        
    cur_meth_impl_start = property(get_cur_meth_impl_start, set_cur_meth_impl_start, None, "__cur_meth_impl_start(int) -- The address of the method implementation. Has to be set externally.")
    seg = property(get_seg, set_seg, None, "__seg(Segment see Hopper scripting api) -- object of Hopper which holds the function for annotation")
    not_annotated_registers_list = property(get_not_annotated_registers_list, set_not_annotated_registers_list, None, "__not_annotated_registers_list(list<tuple<str, int>>) -- if the annotation of registers is enabled, all registers that will be annotated are stored in this list and annotated if `clear()` gets called.")
    annotate_calls = property(get_annotate_calls, set_annotate_calls, None, "__annotate_calls(bool, optional (default is False)) -- enable annotation of calls")
    annotate_registers = property(get_annotate_registers, set_annotate_registers, None, "__annotate_assignments(bool, optional (default is False)) -- enable annotation of registers")
    ann_method_head = property(get_ann_method_head, set_ann_method_head, None, "__ann_method_head(bool, optional (default is False)) -- write a summary of the calls to the beginning of the method implementation.")                
    
hopanno = HopperAnnotater()
