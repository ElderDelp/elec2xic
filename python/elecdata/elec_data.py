#!/bin/env python3
# --------------------------------------------------------------------
#  P Y T H O N / e l e c _ d a t a . p y
#  created Wed Jun 26, 2024  7:27 pm by: Gary Delp <Gary.Delp@slsmn.com>
# --------------------------------------------------------------------
#   Copyright (c) 2024 SilverLoonSystems. All Rights Reserved
#    Worldwide. Licensed under the Apache License, Version 2.0
# --------------------------------------------------------------------
"""Commentary:
Classes for holding the various electric objects and their properties,
"""
# --------------------------------------------------------------------
#  (Last Emacs Update:  Sun Aug  4, 2024  6:42 pm by Gary Delp v-0.1.22)
#
# Sun Aug  4, 2024  6:42 pm by Gary Delp v-0.1.22:
#
# Sat Aug  3, 2024 10:48 pm by Gary Delp v-0.1.18:
#
# Tue Jul  9, 2024  3:46 pm by Gary Delp v-0.1.16:
#
# Wed Jul  3, 2024  8:52 pm by Gary Delp v-0.1.12:
#
# Tue Jul  2, 2024  9:26 pm by Gary Delp v-0.1.12:
#     Tests passes this version
# Fri Jun 28, 2024 10:04 pm by Gary Delp v-0.1.6:
#     got much of the baseclass written
# Wed Jun 26, 2024  9:06 pm by Gary Delp v-0.1.2:
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: PYTHON/elec_data.py
# from functools import wraps
# from dataclasses import dataclass
from base_classes import (
    ElecReadException,
    ElecBase, ElecLine, ElecCell, Parms,
    elec_add_line_Parser,
)
from elec_jelib import JeLIB

class ElecCellLayout(ElecCell):
    """Class for Cell BodyLayout.."""

    def __init__(self, library:str, name:str, version:str = "") -> None:
        super().__init__(library, name, version)


class ElecCellSchematic(ElecCell):
    """Class for Cell BodyCircuit.."""

    def __init__(self, library:str, name:str, version:str = "") -> None:
        super().__init__(library, name, version)


class ElecCellIcon(ElecCell):
    """Class for Cell BodyIcon.."""

    def __init__(self, library:str, name:str, version:str = "") -> None:
        super().__init__(library, name, version)

class ElecCellDocumentation(ElecCell):
    """Class for Cell BodyIcon.."""

    def __init__(self, library:str, name:str, version:str = "") -> None:
        super().__init__(library, name, version)


class ElecCellUnknown(ElecCell):
    """Class for Cell BodyIcon.."""

    def __init__(self, library:str, name:str, version:str = "") -> None:
        super().__init__(library, name, version)

@elec_add_line_Parser("C")
class ElecLineC_ell(ElecLine):
    """C<name> | <group> | <tech> | <creation> | <revision> | <flags> [ | <variable> ]*
    <name>      the name of the cell in the form "NAME;VERSION{VIEW}".
    <group>     the name of this cell's group (if different than expected).
                  This field may be omitted in earlier-format libraries.
    <tech>      the technology of the cell.
    <creation>  the creation date of the cell (Java format).
    <revision>  the revision date of the cell (Java format).
    <flags>     flags for the cell.
    <variable>  a list of variables on the cell (see Section 10-4-1).

    The Java format for dates (the creation and revision dates) is in
    milliseconds since the "epoch" (Midnight on January 1, 1970, GMT).

    The <flags> field consists of any of the following letters,
       (sorted alphabetically):

    "C" if this cell is part of a cell-library.
    "E" if the cell should be created "expanded".
    "I" if instances in the cell are locked.
    "L" if everything in the cell is locked.
    "T" if this cell is part of a technology-library.
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

@elec_add_line_Parser("N")
class ElecLineN_ode(ElecLine):

    def proc_line(self):
        # err_str: str = ''
        if isinstance(self.container, ElecCell):
            cell: ElecCell = self.container
            cell.node.append(self)

@elec_add_line_Parser("I")
class ElecLineI_nstance(ElecLine):

    def proc_line(self):
        # err_str: str = ''
        if isinstance(self.container, ElecCell):
            cell: ElecCell = self.container
            cell.nodes.append(self)

@elec_add_line_Parser("A")
class ElecLineA_rc(ElecLine):

    def proc_line(self):
        # err_str: str = ''
        if isinstance(self.container, ElecCell):
            cell: ElecCell = self.container
            cell.arcs.append(self)

@elec_add_line_Parser("E")
class ElecLineE_xport(ElecLine):

    def proc_line(self):
        # err_str: str = ''
        if isinstance(self.container, ElecCell):
            cell: ElecCell = self.container
            cell.xport.append(self)

# --------------------------------------------------------------------
# elec_data.py ends here.
