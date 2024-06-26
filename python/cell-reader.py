#!/bin/env python3
# --------------------------------------------------------------------
#  P Y T H O N / c e l l - r e a d e r . p y
#  created Mon Jun 24, 2024  8:28 pm by: Gary Delp <Gary.Delp@slsmn.com>
# --------------------------------------------------------------------
#   Copyright (c) 2024 SilverLoonSystems. All Rights Reserved
#    Worldwide. Licensed under the Apache License, Version 2.0
# --------------------------------------------------------------------
"""Commentary:

"""

# --------------------------------------------------------------------
#  (Last Emacs Update:  Tue Jun 25, 2024  9:13 pm by Gary Delp v-0.1.2)
#
# Tue Jun 25, 2024  9:13 pm by Gary Delp v-0.1.2:
#
#  Mon Jun 24, 2024  8:28 pm by Gary Delp v-0.1.0:
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: PYTHON/cell-reader.py
import sys

class ElecLine:
    """Base Class for reading a line of a JELIB."""

    def __init__(self, line:str) -> None:
        self.type, self.parts = line[0], line[1:].split(sep='|')

class ElecCell():
    """The collection of the elements of a cell.
C       Cell header; variable fields are allowed
N       Primitive node information in the current cell; variable fields are allowed
I       Cell instance information in the current cell; variable fields are allowed
A       Arc information in the current cell; variable fields are allowed
E       Export information in the current cell; variable fields are allowed
X       Cell termination
"""
    pass

class ElecJELib():
    """The collection of all info in a JELIB file.
H       Header information; variable fields are allowed
V       View information
L       External library information
R       External cell in the above external library
F       External export in the above external cell
T       Technology information; variable fields are allowed
O       Tool information; variable fields are allowed
"""

# --------------------------------------------------------------------
# cell-reader.py ends here.
