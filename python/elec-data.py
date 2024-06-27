#!/bin/env python3
# --------------------------------------------------------------------
#  P Y T H O N / e l e c - d a t a . p y
#  created Wed Jun 26, 2024  7:27 pm by: Gary Delp <Gary.Delp@slsmn.com>
# --------------------------------------------------------------------
#   Copyright (c) 2024 SilverLoonSystems. All Rights Reserved
#    Worldwide. Licensed under the Apache License, Version 2.0
# --------------------------------------------------------------------
"""Commentary:

"""

# --------------------------------------------------------------------
#  (Last Emacs Update:  Wed Jun 26, 2024  9:06 pm by Gary Delp v-0.1.2)
#
# Wed Jun 26, 2024  9:06 pm by Gary Delp v-0.1.2:
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: PYTHON/elec-data.py
#from functools import wraps

def gsd_init_class(klass):
    """Decorator to intialize class when defined."""
    klass
    klass.cls_init()

@gsd_init_class
class ElecBase():
    """Base with lookup dicts. Init and lookup.  Holds a three tiered
    dict tree of all the elecBase-based instances using name, type,
    and version as keys.
    """

    stable_hash: int = 0
    ElecNone: "ElecBase"
    init_needed: bool = True

name_dict: dict[str, dict[str, "ElecBase"]]
    @classmethod
    def register_element(cls, name:str,
    @classmethod
    def cls_init(cls) -> None:
        if cls.init_needed:
            cls.ElecNone = cls('ElecNone')

    @property
    @classmethod
    def ElecNone(cls):
        return cls.ElecNone

    def __init__(self, name:str, version:str) -> None:
        self.name = name
        self.type_name = self.type.__name__


# --------------------------------------------------------------------
# elec-data.py ends here.
