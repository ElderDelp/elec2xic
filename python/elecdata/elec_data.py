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
#  (Last Emacs Update:  Tue Jul  2, 2024  5:35 pm by Gary Delp v-0.1.12)
#
# Tue Jul  2, 2024  5:35 pm by Gary Delp v-0.1.12:
#
# Mon Jul  1, 2024  8:19 pm by Gary Delp v-0.1.10:
#
# Sun Jun 30, 2024  8:12 pm by Gary Delp v-0.1.10:
#
# Sat Jun 29, 2024 10:58 pm by Gary Delp v-0.1.8:
#
# Fri Jun 28, 2024 10:04 pm by Gary Delp v-0.1.6:
#     got much of the baseclass written
# Wed Jun 26, 2024  9:06 pm by Gary Delp v-0.1.2:
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: PYTHON/elec_data.py
# from functools import wraps
# from dataclasses import dataclass
import pdb
from typing import Self, Any
import re

def gsd_init_class(klass):
    """Decorator to intialize class when defined."""
    klass.cls_init()
    return klass

@gsd_init_class
class ElecBase():
    """Base with lookup dicts. Init and lookup.  Holds a three tiered
    dict tree of all the elecBase-based instances using name, dtype,
    and version as keys.
    """
    dummy: Any = None
    ElecNone: Self = dummy
    init_needed: bool = True

    #some useful types
    Tversion_dict = dict[str, Self]
    Tdtype_dict = dict[str, Tversion_dict]
    Tname_dict = dict[str, Tdtype_dict]
    Tlibrary_dict = dict[str, Tname_dict]

    # the symbol db
    _name_dict: Tlibrary_dict = {}
        # "": {                # library:
        #     "":              # name:
        #     {"":             # dtype:
        #      {"":            # version:
        #       dummy          # Value
        #       }}}}

    @classmethod
    def reset_name_dict(cls):
        """Clear the name_dict."""
        cls._name_dict = {}
            # "": {               # library:
            #     "":             # name:
            #     {"":            # dtype:
            #      {"":           # version:
            #       cls.dummy     # Value
            #       }}}}

    @classmethod
    def register_element(
            cls, obj:Self, library:str ="",
            name:str = "", dtype:str = "", version:str = ""):
        """ the_library: Tlibrary_dict = cls.dummy
         the_name: Tname_dict = cls.dummy
         the_dtype: Tdtype_dict = cls.dummy
         the_end: Self"""
        the_version: Self = cls.dummy
        if library in cls._name_dict:
            the_library = cls._name_dict[library]
            if name in the_library:
                the_name = the_library[name]
                if dtype in the_name:
                    the_dtype = the_name[dtype]
                    if version in the_dtype:
                        the_version = the_dtype[version]
                        if the_version is not obj:
                            if isinstance(the_version, type(cls._ElecNone)):
                                the_version.collide.add(obj)
                            else:
                                the_dtype[version] = obj
                    else:
                        the_dtype[version] = obj
                else:
                    the_dtype =  {version: obj}
                    the_name[dtype] = the_dtype
            else:
                the_dtype =  {version: obj}
                the_name = {dtype: the_dtype}
                the_library[name] = the_name
        else:
            the_dtype =  {version: obj}
            the_name = {dtype: the_dtype}
            the_library = {name: the_name}
            cls._name_dict[library] = the_library
        obj.name_db = {
            'library': (library, the_library),
            'name': (name, the_name),
            'dtype': (dtype, the_dtype),
            'version': (version, the_version)
            }

    @staticmethod
    def str_includes(general:str, specific:str) -> bool:
        return re.match(general, specific) is not None

    @classmethod
    def lookup_symbol(
            cls, library:str, name:str, dtype:str, version:str):
        """Return a list of the matching elements."""
        ret= []
        for a_library in cls._name_dict:
            if cls.str_includes(library, a_library):
                the_library = cls._name_dict[a_library]
                for a_name in the_library:
                    if cls.str_includes(name, a_name):
                        the_name = the_library[a_name]
                        for a_dtype in the_name:
                            if cls.str_includes(dtype, a_dtype):
                                the_dtype = the_name[a_dtype]
                                for a_version in the_dtype:
                                    if cls.str_includes(version, a_version):
                                        the_version = the_dtype[a_version]
                                        if isinstance(the_version, cls.ElecNone.__class__):
                                            ret.append(the_version)
                                            for others in the_version.collide:
                                                ret.append(others)
        return ret

    @classmethod
    def cls_init(cls) -> None:
        """Allocate the class constant instance: ElecNone."""
        if cls.init_needed:
            cls._ElecNone = cls("", "ElecNone", "")
            cls.register_element(
                cls._ElecNone,'ElecNone', type(cls).__name__,"")
            cls.reset_name_dict()

    # as shared in https://docs.python.org/3.11/library/functions.html#classmethod
    #  Class methods can no longer wrap other descriptors such as property().
    # @property
    # @classmethod
    # def ElecNone(cls) -> Self:
    #     return cls._ElecNone

    # @property
    # @classmethod
    # def master_name_dict(cls) -> Tlibrary_dict:
    #     return cls.name_dict

    def __init__(self, library:str, name:str, version:str = "") -> None:
        self.name_db: dict[str, tuple] = self.dummy
        self.collide: set[Self] = set()
        # pdb.set_trace()
        self.register_element(
            self, library, name, type(self).__name__, version)

    def __str__(self) -> str:
        ret = '<<' + type(self).__name__
        sep = ''
        for key in self.name_db:
            val = self.name_db[key]
            ret += f'{sep} {key}={val[0]}'
            sep = ','
        ret += '>>'
        return ret



# --------------------------------------------------------------------
# elec_data.py ends here.
