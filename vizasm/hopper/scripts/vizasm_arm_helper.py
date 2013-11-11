'''
VizAsm

@author: Nils Schmidt

Helper for the arm architecture. Hopper currently does not annotate the instance variables as well as some classrefs.
Run it before you analyze the file with VizAsm
'''

from traceback import format_exception

# e.g
# VIZASM_FILEAPTH = '/Users/.../vizasm'
VIZASM_FILEAPTH = None
if VIZASM_FILEAPTH is None:
    raise Exception('The path to VizAsm needs to be specified!')

try:
    import sys, os
    
    PATH = os.path.abspath(VIZASM_FILEAPTH)
    sys.path.append(PATH)
    doc = Document.getCurrentDocument()
    doc.log('VizAsm arm helper')
    doc.log('appending %s to search path' % PATH)
    
    from vizasm.model.asm.Segments import *
    
    segments = doc.getSegmentsList()
    ivar_seg = segment_for_name(SEGMENT_OBJC_IVAR, segments)
    text_seg = segment_for_name(SEGMENT_TEXT, segments)
    classrefs_seg = segment_for_name(SEGMENT_OBJC_CLASSREFS, segments)
    superrefs_seg = segment_for_name(SEGMENT_OBJC_SUPERREFS, segments)
    
    ptr_size = 4
    if doc.is64Bits():
        ptr_size = 8
    
    def segment_addr_it(seg):  
        ''' Get an iterator over the segment address range '''
        if seg is None:
            return []
        return xrange(seg.getStartingAddress(), seg.getStartingAddress() + seg.getLength(), ptr_size)
    
    def find_last_name(addr, seg):        
        ''' Go back in the lines until the name for the address has been found.
        Returns None if not found at all ''' 
        for addr in xrange(addr, seg.getStartingAddress(), -ptr_size):
            name = seg.getNameAtAddress(addr)
            if name is not None:
                return name
        return None
    
    def annotate_ivars():
        for addr in segment_addr_it(ivar_seg):
            doc.log('references for %s:' % (hex(int(addr))))
            references = ivar_seg.getReferencesOfAddress(addr)
            if references is not None:
                for a in references:
                    hex_string = hex(int(a))
                    comment = 'IVAR_%s' % hex_string
                    doc.log('ivar at %s: %s' % (hex_string, comment))
                    text_seg.setInlineCommentAtAddress(a, comment)
                doc.log('')
    
    def annotate_classrefs():
        for addr in segment_addr_it(classrefs_seg):
            doc.log('references for %s:' % (hex(int(addr))))
            references = classrefs_seg.getReferencesOfAddress(addr)
            if references is not None:
                for a in references:
                    hex_string = hex(int(a))
                    name = find_last_name(addr, classrefs_seg)
                    if name is not None:
                        comment = '@%s' % name
                        doc.log('classref at %s: %s' % (hex_string, comment))
                        text_seg.setInlineCommentAtAddress(a, comment)
                doc.log('')
    
    annotate_classrefs()
    annotate_ivars()    
except Exception as e:
    t, v, tb = sys.exc_info()
    doc.log('\n'.join(format_exception(t, v, tb)))
 
