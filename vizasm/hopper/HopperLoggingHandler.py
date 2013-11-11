'''
VizAsm

Created on 23.10.2013

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

class HopperLoggingHandler(logging.StreamHandler):
    '''Logging handler for Hopper. Redirects the output to the log function of `Document`
   
    Parameters
    ----------
    doc: Document (see Hopper api)
    '''

    def __init__(self, stream = None, doc = None):
        logging.StreamHandler.__init__(self, stream)
        self.__doc = doc

    def get_doc(self):
        return self.__doc

    def set_doc(self, value):
        self.__doc = value
        
    def emit(self, record):
        try:
            msg = self.format(record)
            fs = "%s"
            self.doc.log(fs % msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    doc = property(get_doc, set_doc, None, "doc(Document) -- (see Hopper api)")
