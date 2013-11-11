'''
VizAsm

Created on 02.04.2013

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

from vizasm.model.asm.imp.Imp import Imp

class ImpGot(Imp):
    '''
    Imp got examples:
    
    imp___got__
        imp___got__NSStreamSocketSecurityLevelKey
        imp___got__NSStreamSocketSecurityLevelNone
        imp___got__NSURLAuthenticationMethodServerTrust
        imp___got__kSecRandomDefault
        imp___got__CGAffineTransformIdentity
        imp___got__CGPointZero
        imp___got__CGRectNull
        imp___got__CGRectZero
        imp___got__CGSizeZero
        imp___got__NSDefaultRunLoopMode
        imp___got__NSFileSize
        imp___got__NSFileSystemFreeSize
        imp___got__NSFontAttributeName
        imp___got__NSInternalInconsistencyException
        imp___got__NSLocalizedDescriptionKey
        imp___got__NSParagraphStyleAttributeName
        imp___got__QTMovieDidEndNotification
        imp___got__QTMovieEditableAttribute
        imp___got__QTMovieLoopsAttribute
        imp___got__QTMovieOpenAsyncRequiredAttribute
        imp___got__free
        imp___got__glGetProgramInfoLog
        imp___got__glGetProgramiv
        imp___got__glGetShaderInfoLog
        imp___got__glGetShaderiv
        imp___got__kUTTypeJPEG
        imp___got__kUTTypePNG
        imp___got__objc_autoreleasePoolPush
        imp___got__objc_msgSend
        imp___got__objc_release
        imp___got__objc_retain    
    
    imp___got___
        imp___got___DefaultRuneLocale
        imp___got___NSConcreteStackBlock
    
    imp___got____
        imp___got____gxx_personality_v0
        imp___got____objc_personality_v0
        imp___got____stack_chk_guard
        imp___got____stderrp
        imp___got____stdinp
        imp___got____stdoutp
    '''
    def __init__(self, imp_stub):
        Imp.__init__(self, imp_stub)
