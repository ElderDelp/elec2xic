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
#  (Last Emacs Update:  Sat Aug  3, 2024 10:49 pm by Gary Delp v-0.1.16)
#
# Sat Aug  3, 2024 10:49 pm by Gary Delp v-0.1.16:
#
# Fri Aug  2, 2024  9:53 pm by Gary Delp v-0.1.16:
#
# Thu Aug  1, 2024  8:43 pm by Gary Delp v-0.1.16:
#
# Wed Jul 31, 2024  8:22 pm by Gary Delp v-0.1.14:
#
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: ELECDATA/elec_jelib.py
import re
from typing import Self, IO, Any
from pathlib import Path
from base_classes import (
    ElecBase, ElecReadException, ElecLine, Parms,
    elec_add_line_Parser
)
from collections import namedtuple

from elec_data import ElecCellBody

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
    def stack_str(cls, name: str, filename: str, line_no: int,
                  mark: int = -1) -> str:
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
        name: str: the name of the library to read.
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
        cls.lib_call_stack.append(
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
        self.line_no: int = 0
        self.source: IO[Any] = source
        self.view_d: dict[str, str] = {}
        self.lib_d: dict[str, Self] = {}
        self.tools_d: dict[str, list[Parms]] = {}
        self.called_from: list[LibRefInfo] = []
        self.cells: list[ElecCellBody] = []
        self.read_loop()

    def gline(self):
        while ret := self.source.readline():
            self.line_no +=1
            if ret[0] in " #\n":
                continue
            else:
                yield re.sub(r'(\S)\s*\Z', r'\1', ret, flags=re.MULTILINE)

    def read_loop(self) -> None:
        """Read the lines, keep track of line number, collect the cells."""
        need_header: bool = True
        in_cell: bool = False
        dummy: Any = None
        cur_cell: ElecCellBody = dummy
        for rline in  self.gline():
            rline = str(rline)
            ltype: str = rline[0]
            klass = ElecLine.get_reader(ltype)
            if need_header:
                # Header is first non-blank non-comment line
                need_header = False
                if ltype != "H":
                    err_str = 'The source does not start with a header line:'
                    err_str += f"{self.line_no}: is '{rline}'"
                    raise ElecReadException(err_str)
                klass(rline, self, self.line_no)
            elif in_cell:
                if ltype in "NIAE":
                    klass(rline, cur_cell, self.line_no)
                elif ltype not in "X":
                    err_str = f"{self.name_db['version'][0]}:{self.line_no}:"
                    err_str += f', *error* unknown cell line prefix "{ltype}", '
                    err_str += rline
                    raise ElecReadException(err_str)
                else:
                    in_cell = False
            elif ltype == 'C':
                # Process a cell
                in_cell = True
                cur_cell = klass(rline, self, self.line_no)
            elif ltype in 'VOLT':
                klass(rline, self, self.line_no)
            else:
                err_str = f"{self.name_db['version'][0]}:{self.line_no}:"
                err_str += f', *error* unknown ex-cell line prefix "{ltype}", '
                err_str += rline
                raise ElecReadException(err_str)

    def morph_fn(self, new_lib: str) -> str:
        """Relative to the current jelib, use NEW_LIB to return full filename."""
        ret = re.sub(
            pattern=self.name_db['name'][0] + r'\.jelib\Z',
            repl=new_lib + ".jelib",
            string=self.name_db['version'][0])
        return ret


@elec_add_line_Parser("H")
class ElecLineH_eader(ElecLine):
    """H<name> | <version> [ | <variable> ]*
    <name>  the name of the library.
    <version>       the version of Electric that wrote the library.
    <variable>      a list of variables on the library (see Section 10-4-1).

    The name of the library is used in the JELIB file to identify
    references to this library. The actual name of this library is
    obtained from the file path of this JELIB file.
    """
    def proc_line(self):
        err_str: str = ''
        if isinstance(self.container, JeLIB):
            jel = self.container
            elist = self.text[1:].split("|")
            if len(elist) < 2:
                err_str = f'The .jelib Header "{self.text}" is too short.'
                err_str += f", line:{self.line_no}"
                raise ElecReadException(err_str)
            if jel.name_db['library'][0] != elist[0]:
                err_str = f'The .jelib Header name line "H{elist[0]}|{elist[1]}"'
                err_str += 'does not match file basename '
                err_str += f"{jel.name_db['library'][0]}"
                err_str += f", line:{self.line_no}"
                raise ElecReadException(err_str)
            if '9.08e' != elist [1]:
                err_str = 'The .jelib file does not use version 9.08e, rather'
                err_str += f' "{elist[1]}", line:{self.line_no}'
                raise ElecReadException(err_str)


@elec_add_line_Parser("V")
class ElecLineV_iew(ElecLine):
    """Views

    All views used in the library must be declared.

    V<full name> | <name>
    <full name> the full name of the view.
    <name>      the abbreviation name of the view."""
    def proc_line(self):
        if isinstance(self.container, JeLIB):
            jel: JeLIB = self.container
            elist = self.text[1:].split("|")
            jel.view_d[elist[1]] = elist[0]


@elec_add_line_Parser("T")
class ElecLineT_echnology(ElecLine):
    """Process a technology line.  Not currently implemented."""
    pass

@elec_add_line_Parser("O")
class ElecLineO_tool(ElecLine):
    """Tools

    There is no need to declare all tools in the header. The only
    reason for a tool declaration to exist is if the tool has project
    setting variables stored on it. If there are multiple tool lines,
    they are sorted by the tool name. The syntax is:

    O<name> [ | <variable> ]*
    <name>      the name of the tool.
    <variable>  a list of preferences on the tool (stored as variables, see Section 10-4-1).

    Example:

    Ologeffort|GlobalFanout()D12.0
    Declares a project setting on the "Logical Effort" tool object. The
    "GlobalFanout" is set to the floating point value 12.
    """
    def proc_line(self):
        # err_str: str = ''
        if isinstance(self.container, JeLIB):
            jel: JeLIB = self.container
            elist = self.text[1:].split("|")
            plist: list[Parms] = []
            for p in elist[1:]:
                if m := re.match(r'\A([^(]+)\(([^)]*)\)(.*)\Z',p):
                    plist.append(
                        Parms(*m.group(1, 2, 3)))
            jel.tools_d['elist[0]'] = plist


@elec_add_line_Parser("L")
class ElecLineL_ibrary(ElecLine):
    """After the header line, all external libraries cells and exports
    must be declared. This allows the file reader to quickly find all
    libraries that will be needed for the design, and to reconstruct
    any missing cells and exports. The cells are listed under their
    libraries. The exports are listed under their cells. If there are
    multiple external library lines, they are sorted by library name;
    where there are multiple external cells in a library, they are
    sorted by their name; and where there are multiple external
    exports in a cell, they are sorted by their name.

    The syntax of an external library reference is:

    L<name> | <path>
    <name>  the name of the external library.
    <path>  the full path to the disk file with the library.

    The name of the library is used in JELIB file to references to
    this library. The actual name of this library is obtained from the
    path."""

    def proc_line(self):
        # err_str: str = ''
        if isinstance(self.container, JeLIB):
            jel: JeLIB = self.container
            elist = self.text[1:].split("|")
            jel.lib_d[elist[0]]  = jel.read_lib(
                elist[0], elist[1], self.line_no)



# --------------------------------------------------------------------
# elec_jelib.py ends here.
