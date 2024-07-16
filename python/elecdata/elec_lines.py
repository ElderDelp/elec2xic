#!/bin/env python3
# --------------------------------------------------------------------
#  E L E C D A T A / e l e c _ l i n e s . p y
#  created Thu Jul  4, 2024  4:34 pm by: Gary Delp <Gary.Delp@slsmn.com>
# --------------------------------------------------------------------
#   Copyright (c) 2024 SilverLoonSystems. All Rights Reserved
#    Worldwide. Licensed under the Apache License, Version 2.0
# --------------------------------------------------------------------
"""Commentary:
a class for each line type in a .jelib file
 The JELIB file has 3 parts: the header, cells, and trailer.

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

Headers

The first line in the JELIB file should be the "H" header line. The syntax is:

H<name> | <version> [ | <variable> ]*
<name>  the name of the library.
<version>       the version of Electric that wrote the library.
<variable>      a list of variables on the library (see Section 10-4-1).

"""

# --------------------------------------------------------------------
#  (Last Emacs Update:  Mon Jul 15, 2024  2:08 pm by Gary Delp v-0.1.16)
#
# Mon Jul 15, 2024  2:07 pm by Gary Delp v-0.1.14:
#
# Fri Jul 12, 2024  5:50 pm by Gary Delp v-0.1.14:
#
# Thu Jul 11, 2024  5:11 pm by Gary Delp v-0.1.12:
#
# Fri Jul  5, 2024 11:04 pm by Gary Delp v-0.1.10:
#
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: ELECDATA/elec_lines.py
from base_classes import ElecBase, ElecLine, Parms, elec_add_line_Parserw
from elec_jelib import JeLIB

not_used

class ElecCellRef(ElecBase):
    """Class for Cell References."""

    def __init__(self, library:str, name:str, version:str = "") -> None:
        super().__init__(library, name, version)

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
# elec_lines.py ends here.
