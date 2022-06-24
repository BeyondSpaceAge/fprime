# ===============================================================================
# NAME: GTestWriter.py
#
# DESCRIPTION: A writer for generating gtest base header files
#
# AUTHOR: Jordan Ishii
# EMAIL:  jordan.ishii@jpl.nasa.gov
# DATE CREATED  : July 8, 2019
#
# Copyright 2015, California Institute of Technology.
# ALL RIGHTS RESERVED. U.S. Government Sponsorship acknowledged.
# ===============================================================================
import sys

from fprime_ac.generators.writers import GTestWriterBase

try:
    from fprime_ac.generators.templates.gtest import hpp
except ImportError:
    print("ERROR: must generate python templates first.")
    sys.exit(-1)


class GTestHWriter(GTestWriterBase.GTestWriterBase):
    """
    A writer for generating gtest header files.
    """

    FILE_NAME = "GTestBase.hpp"

    def __init__(self):
        super().__init__()
        self.initBase("GTestH")

    def emitHppParams(self, params):
        return self.emitNonPortParamsHpp(10, params)

    def emitMacroParams(self, params):
        str = ""
        for param in params:
            name = param[0]
            str += f", _{name}"
        return str

    def _initFilesWrite(self, obj):
        self.openFile(self.FILE_NAME)

    def _startSourceFilesWrite(self, obj):
        c = hpp.hpp()
        self.initGTest(obj, c)
        c.emit_hpp_params = self.emitHppParams
        c.emit_macro_params = self.emitMacroParams
        c.file_message = '    << "  File:     " << __FILE__ << "\\n" \\\n'
        c.line_message = '    << "  Line:     " << __LINE__ << "\\n"'
        c.failure_message = '<< "\\n" \\\n' + c.file_message + c.line_message
        c.LTLT = "<<"
        self._writeTmpl(c, "startSourceFilesWrite")

    def write(self, obj):
        """
        Calls all of the write methods so that full file is made
        """
        self._initFilesWrite(obj)
        self._startSourceFilesWrite(obj)
        self.includes1Write(obj)
        self.includes2Write(obj)
        self.namespaceWrite(obj)
        self.publicWrite(obj)
        self.protectedWrite(obj)
        self.privateWrite(obj)
        self.finishSourceFilesWrite(obj)

    def toString(self):
        return self.FILE_NAME
