#!/bin/env python3
# --------------------------------------------------------------------
#  E L E C D A T A / e l e c _ j e l i b . p y
#  created Thu Jul  4, 2024  5:04 pm by: Gary Delp <Gary.Delp@slsmn.com>
# --------------------------------------------------------------------
#   Copyright (c) 2024 SilverLoonSystems. All Rights Reserved
#    Worldwide. Licensed under the Apache License, Version 2.0
# --------------------------------------------------------------------
"""Commentary:
The header has these elements:

H       Header information; variable fields are allowed
V       View information
L       External library information
R       External cell in the above external library
F       External export in the above external cell
T       Technology information; variable fields are allowed
O       Tool information; variable fields are allowed

The cells have these elements:

C       Cell header; variable fields are allowed
N       Primitive node information in the current cell; variable fields are allowed
I       Cell instance information in the current cell; variable fields are allowed
A       Arc information in the current cell; variable fields are allowed
E       Export information in the current cell; variable fields are allowed
X       Cell termination

The trailer has this optional element:

G       Group information
"""

# --------------------------------------------------------------------
#  (Last Emacs Update:  Sun Jul 14, 2024  7:47 pm by Gary Delp v-0.1.6)
#
# Sun Jul 14, 2024  7:47 pm by Gary Delp v-0.1.6:
#
# Thu Jul 11, 2024  1:37 pm by Gary Delp v-0.1.4:
#
# Thu Jul  4, 2024  5:23 pm by Gary Delp v-0.1.2:
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: ELECDATA/elec_jelib.py
from typing import Self, IO, Any
from pathlib import Path
from base_classes import ElecBase, ElecReadException, ElecLine, Parms, jelib_path
from collections import namedtuple

LibRefInfo = namedtuple('LibRefInfo', ['name', 'filename', 'fromfile', 'line'])

class JeLIB(ElecBase):
    """In the context of elec_data and the structure of ElecBase, an
    object containing the data from a single .jelib file.  It will
    potentially contain references to other JeLIBs.
    """

    libs_read: dict[str, Self] = {}

    # (name, filename, fromfile, line_no)
    lib_call_stack: list[LibRefInfo] = [
        LibRefInfo('base', 'stdin', '', 0)]

    @classmethod
    def stack_str(cls, name: str, filename: str, line_no: int, mark: int = -1) -> str:
        """Return a string representing the cls.lib_call_stack"""
        j = 0
        ret_str = f"{cls.__name__}.lib_call_stack:\n"
        for (j, ent) in enumerate(cls.lib_call_stack):
            ret_str += f"{j}:{ent.fromfile}:{ent.line}: reading "
            if mark == j:
                ret_str += "*prev* "
            ret_str += f"{ent.name} from {ent.filename}\n"
        if name != '' and filename != '':
            ret_str += f"{j+1}:{cls.lib_call_stack[-1][2]}:{line_no} "
            ret_str += f"reading *this* {name} from {filename}\n"
        return ret_str

    @classmethod
    def read_lib(cls, name: str, filename:str, line_no: int) -> Self:
        """Check the name (has it or is it been/being loaded?) raising
        ElecReadException on a loop. If all OK returns a read instance.
        name: str: the name of the library to read
        """
        i = -1
        # If already read, then just return the instance
        if name in cls.libs_read:
            ret = cls.libs_read[name]
            caller = cls.lib_call_stack[-1]
            ret.called_from.append(caller)

        # check for a read loop
        # lib A reads lib B which reads lib C which comes back and reads lib A
        this_read = (name, filename)
        for (i, already) in enumerate(cls.lib_call_stack):
            if this_read == (already.name, already.filename):
                # already reading this file, there is a loop!
                err_str = f"ElecReadException: opening '{filename}' "
                err_str += cls.stack_str(name, filename, line_no, i)
                raise ElecReadException(err_str)

        # check file exists
        filep = Path(filename)
        if not filep.exists:
            err_str = f"ElecReadException: '{filename}' does not exist."
            err_str += cls.stack_str(name, filename, line_no, i)
            raise ElecReadException(err_str)
        cls.stack_str.append(
            LibRefInfo(name, filename, cls.lib_call_stack[-1].fromfile, line_no))
        with filep.open(filename) as lib_fp:
            ret = cls(lib=name, name="libRoot",
                      version=filename, source=lib_fp)
        cls.lib_call_stack.pop()
        return ret


    def __init__(self, source: IO[Any], lib: str, name:str, version:str) -> None:
        """Read line by line, pushing into other libraries referenced,
        reading them in before continuing to the next line.
        """
        super().__init__(lib, name, version)
        self.lines: dict[str,list[ElecBase]] = {}
        self.cells: dict[str, ElecBase] = {}
        self.called_from: list[LibRefInfo] = []
        ElecLine.read_loop(self, source)





# --------------------------------------------------------------------
# elec_jelib.py ends here.
