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
#  (Last Emacs Update:  Fri Jul  5, 2024 10:53 pm by Gary Delp v-0.1.16)
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
from .base_classes import ElecBase

class ElecCellBody(ElecBase):
    """Class for Cell Bodies."""

    def __init__(self, library:str, name:str, version:str = "") -> None:
        super().__init__(library, name, version)
        self.parms: list[parms]= []



class ElecCellBodyLayout(ElecCellBody):
    """Class for Cell BodyLayout.."""

    def __init__(self, library:str, name:str, version:str = "") -> None:
        super().__init__(library, name, version)


class ElecCellBodyCircuit(ElecCellBody):
    """Class for Cell BodyCircuit.."""

    def __init__(self, library:str, name:str, version:str = "") -> None:
        super().__init__(library, name, version)


class ElecCellBodyIcon(ElecCellBody):
    """Class for Cell BodyIcon.."""

    def __init__(self, library:str, name:str, version:str = "") -> None:
        super().__init__(library, name, version)


# --------------------------------------------------------------------
# elec_data.py ends here.
