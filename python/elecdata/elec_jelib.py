#!/bin/env python3
# --------------------------------------------------------------------
#  E L E C D A T A / e l e c _ j e l i b . p y
#  created Thu Jul  4, 2024  5:04 pm by: Gary Delp <Gary.Delp@slsmn.com>
# --------------------------------------------------------------------
#   Copyright (c) 2024 SilverLoonSystems. All Rights Reserved
#    Worldwide. Licensed under the Apache License, Version 2.0
# --------------------------------------------------------------------
"""Commentary:
he header has these elements:

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
#  (Last Emacs Update:  Mon Jul 15, 2024  4:57 pm by Gary Delp v-0.1.8)
#
# Thu Jul 11, 2024  1:37 pm by Gary Delp v-0.1.4:
#
# Thu Jul  4, 2024  5:23 pm by Gary Delp v-0.1.2:
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: ELECDATA/elec_jelib.py
from typing import Self, IO, Any
from collections.abc import Generator
from pathlib import Path
from base_classes import (ElecBase, ElecReadException, ElecLine, Parms,
                          elec_add_line_Parser)

class JeLIB(ElecBase):
    """In the context of elec_data and the structure of ElecBase, an
    object containing the data from a single .jelib file.  It will
    potentially contain references to other JeLIBs.
    """

    libs_read: dict[str, Self] = {}
    # (name, filename, fromfile, line_no)
    lib_call_stack: list[tuple[str, str, str, int]] = [
        ('base', 'stdin', '', 0)]

    @classmethod
    def stack_str(cls, name: str, filename: str, line_no: int, mark: int = -1) -> str:
        """Return a string representing the cls.lib_call_stack"""
        j = 0
        ret_str = f"{cls.__name__}lib_call_stack:\n"
        for (j, ent) in enumerate(cls.lib_call_stack):
            ret_str += f"{j}:{ent[2]}:{ent[3]}: reading "
            if mark == j:
                ret_str += "*prev* "
            ret_str += f"{ent[0]} from {ent[1]}\n"
        if name != '' and filename != '':
            ret_str += f"{j+1}:{cls.lib_call_stack[-1][2]}:{line_no} "
            ret_str += f"reading *this* {name} from {filename}\n"
        return ret_str

    @classmethod
    def read_lib(cls, name: str, filename:str, line_no: int) -> Self:
        """Check the name (has it or is it been/being loaded?) raising
        ElecReadException on a loop. If all OK return a read instance.
        """
        i = -1
        # If already read, then just return the instance
        if name in cls.libs_read:
            return cls.libs_read[name]

        # check for a read loop
        this_read = (name, filename)
        for (i, already) in enumerate(cls.lib_call_stack):
            if this_read[:] == already[:2]:
                # already reading this file, there is a loop!
                err_str = f"ElecReadException: opening '{filename}' "
                err_str += cls.stack_str(name, filename, line_no, i)
                raise ElecReadException(err_str)
        filep = Path(filename)
        if not filep.exists:
            err_str = f"ElecReadException: '{filename}' does not exist."
            err_str += cls.stack_str(name, filename, line_no, i)
            raise ElecReadException(err_str)
        cls.stack_str.append(
            (name, filename, cls.lib_call_stack[-1][2], line_no))
        with filep.open(filename) as lib_fp:
            ret = cls(lib=name, name="libRoot", version=filename, source=lib_fp)
        cls.lib_call_stack.pop()
        return ret


    def __init__(self, source: IO[Any], lib: str, name:str, version:str) -> None:
        """Read line by line, pushing into other libraries referenced,
        reading them in before continuing to the next line.
        """
        super().__init__(lib, name, version)
        self.line_no: int = 0
        self.source: IO[Any] = source
        self.H_eader: list[ElecLine] = []
        self.V_iew: list[ElecLine] = []
        self.L_ibsibs: dict[str, ElecLine] = {}
        self.R_Cells: list[ElecLine] = []
        self.F_ext_cells: list[ElecLine] = []
        self.T_ech: list[ElecLine] = []
        self.O_tools: list[ElecLine] = []
        self.C_ells: list[ElecLine] = []
        self.G_roups: list[ElecLine] = []
        self.read_loop(source)

    def gline(self):
        while ret := self.source.readline():
            self.line_no +=1
            if ret[0] in " #":
                continue
            else:
                yield ret


    def read_loop(self) -> None:
        """Read the lines, keep track of line number, collect the cells."""
        rline: str = str(self.gline())
        ltype: str = rline[0]
        if ltype != "H":
            err_str = 'The source does not start with a header line:'
            err_str += f"{self.line_no}: is '{rline}'"
            raise ElecReadException(err_str)
        while rline := str(self.gline()):


@elec_add_line_Parser("H")
class ElecLineH_eader(ElecLine):
    """Hx<name> | <version> [ | <variable> ]*
    <name>  the name of the library.
    <version>       the version of Electric that wrote the library.
    <variable>      a list of variables on the library (see Section 10-4-1).

    The name of the library is used in the JELIB file to identify
    references to this library. The actual name of this library is
    obtained from the file path of this JELIB file.
    """
    pass



# --------------------------------------------------------------------
# elec_jelib.py ends here.
