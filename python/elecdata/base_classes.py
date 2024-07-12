#!/bin/env python3
# --------------------------------------------------------------------
#  E L E C D A T A / b a s e _ c l a s s e s . p y
#  created Mon Jun 24, 2024  7:15 pm by: Gary Delp <Gary.Delp@slsmn.com>
# --------------------------------------------------------------------
#   Copyright (c) 2024 SilverLoonSystems. All Rights Reserved
#    Worldwide. Licensed under the Apache License, Version 2.0
# --------------------------------------------------------------------
"""Commentary:

"""
# --------------------------------------------------------------------
#  (Last Emacs Update:  Fri Jul 12, 2024  5:50 pm by Gary Delp v-0.1.16)
#
# Fri Jul 12, 2024  5:50 pm by Gary Delp v-0.1.16:
#
# Thu Jul 11, 2024  5:11 pm by Gary Delp v-0.1.12:
#
# Tue Jul  9, 2024  3:57 pm by Gary Delp v-0.1.12:
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: ELECDATA/base_classes.py

import functools
import math
from pathlib import Path
from typing import Self, Any, IO
from dataclasses import dataclass

import re
jelib_path:Path = Path()

class ElecReadException(ValueError):
    """Various Elect errors."""
    pass

def gsd_init_class(klass):
    """Decorator to intialize class when defined."""
    klass.cls_init()
    return klass

# https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python
# https://docs.python.org/3/reference/compound_stmts.html#grammar-token-python-grammar-type_params
class Watcher(type):
    def __init__(cls, name, bases, clsdict):
        if len(cls.mro()) > 2:
            print("was subclassed by " + name)
        super(Watcher, cls).__init__(name, bases, clsdict)

class SuperClass:
    __metaclass__ = Watcher


print("foo")

class SubClass0(SuperClass):
  pass

print("bar")

class SubClass1(SuperClass):
  print("test")

######################################################################
@gsd_init_class
class ElecBase():
    """Base with lookup dicts. Init and lookup.  Holds a three tiered
    dict tree of all the elecBase-based instances using name, dtype,
    and version as keys.
    """

    #some useful types
    Tversion_dict = dict[str, Self]
    Tdtype_dict = dict[str, Tversion_dict]
    Tname_dict = dict[str, Tdtype_dict]
    Tlibrary_dict = dict[str, Tname_dict]
    # Base class variables
    dummy: Any = None
    ElecNone: Self = dummy
    init_needed: bool = True
    _serial: int = 1
    # the symbol db
    _name_dict: Tlibrary_dict = {}

    @classmethod
    def reset_name_dict(cls) -> None:
        """Clear the name_dict."""
        cls._name_dict = {}

    @classmethod
    def new_serial_no(cls) -> int:
        """Clear the name_dict."""
        cls._serial += 1
        return cls._serial

    @classmethod
    def register_element(
            cls, obj:Self, library:str ="",
            name:str = "", dtype:str = "",
            version:str = "") -> None:
        """ the_library: Tlibrary_dict = cls.dummy
         the_name: Tname_dict = cls.dummy
         the_dtype: Tdtype_dict = cls.dummy
         the_end: Self"""
        the_version: Self = cls.dummy
        obj.collide.add(obj)
        if library in cls._name_dict:
            the_library = cls._name_dict[library]
            if name in the_library:
                the_name = the_library[name]
                if dtype in the_name:
                    the_dtype = the_name[dtype]
                    if version in the_dtype:
                        the_version = the_dtype[version]
                        if the_version is not obj:
                            if isinstance(
                                    the_version,
                                    type(cls.ElecNone.__class__)):
                                the_version.collide.add(obj)
                            else:
                                the_version = obj
                                the_dtype[version] = obj
                    else:
                        the_version = obj
                        the_dtype[version] = obj
                else:
                    the_version = obj
                    the_dtype =  {version: obj}
                    the_name[dtype] = the_dtype
            else:
                the_version = obj
                the_dtype =  {version: obj}
                the_name = {dtype: the_dtype}
                the_library[name] = the_name
        else:
            the_version = obj
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
            cls, library:str, name:str, dtype:str,
            version:str) -> list[Self]:
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
                                            for objs in the_version.collide:
                                                ret.append(objs)
        return ret

    @classmethod
    def cls_init(cls) -> None:
        """Allocate the class constant instance: ElecNone."""
        if cls.init_needed:
            cls.ElecNone = cls("", "ElecNone", "")
            cls.reset_name_dict()

    def __init__(self, library:str, name:str, version:str = "") -> None:
        self.name_db: dict[str, tuple] = self.dummy
        self.collide: set[Self] = set()
        # pdb.set_trace()
        self.serial = self.new_serial_no()
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

@gsd_init_class
class ElecLine(type):
    """One of these objects for every non-comment Line in JELIB."""

    the_readers: dict[str, Self] = {}

    @classmethod
    def read_lines(cls,lib: str, source: IO[Any]):
        pass

    @classmethod
    def register_reader(cls, letter: str, reader: Self) -> None:
        """Register a Reader subclass for lines starting with a given letter."""
        cls.the_readers[letter] = reader

    @classmethod
    def get_reader(cls, letter: str) -> Self:
        """Register a Reader subclass for lines starting with a given letter."""
        if letter in cls.the_readers:
            return cls.the_readers[letter]
        err_str = f"No reader registered for {letter=}"
        raise ElecReadException(err_str)

    @classmethod
    def cls_init(cls) -> None:
        pass

    def __init__(self, text: str, container: ElecBase) -> None:
        """Process the text and store the references."""
        self.text = text
        self.container = container

def elec_add_line_Parser(key:str):
    def decorator(klass):
        klass.register_reader(key, klass)
        return klass

@gsd_init_class
@dataclass
class Location():
    x: float = 0
    y: float = 0

    def shift_scale(self, shift: Self, scale: Self) -> Self:
        return Location((self.x + shift.x) * scale.x, (self.y + shift.y) * scale.y)

    def __add__(self, other: Self) -> Self:
        return Location(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return Location(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Self) -> Self:
        return Location(self.x * other.x, self.y * other.y)

    def __iadd__(self, other: Self) -> Self:
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other: Self) -> Self:
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other: Self) -> Self:
        self.x *= other.x
        self.y *= other.y
        return self

    def __neg__(self) -> Self:
        return Location(-self.x, -self.y)

    def flip_v(self, other: Self) -> Self:
        return Location(self.x, 2 * other.y - self.y )

    def flip_h(self, other: Self) -> Self:
        return Location(2 * other.x - self.x, self.y)

    def rot_deg(self, deg: float) -> Self:
        (c, s) = self.rot_deg_coef(deg)
        return Location(c * self.x - s * self.y, s * self.x + c * self.y)

    def rot_rad(self, rad: float) -> Self:
        (c, s) = self.rot_rad_coef(rad)
        return Location(c * self.x - s * self.y, s * self.x + c * self.y)

    @staticmethod
    def round_0_000001(inp: float) -> float:

    @staticmethod
    @functools.cache
    def rot_rad_coef(rad: float) -> list[float]:
        ret = [math.cos(rad), math.sin(rad)]
        return ret

    @classmethod
    @functools.cache
    def rot_deg_coef(cls, deg: float) -> list[float]:
        c, s = cls.rot_rad_coef(math.radians(deg))
        return ((int(c * (

    @classmethod
    def cls_init(cls) -> None:
        """Allocate the class constant instance: ElecNone."""

        print(f" {cls.rot_deg_coef(0)=}")
        print(f" {cls.rot_deg_coef(360)=}")
        print(f" {cls.rot_deg_coef(90)=}")
        print(f" {cls.rot_deg_coef(270)=}")
        print(f" {cls.rot_deg_coef(180)=}")
        assert (1, 0) == cls.rot_deg_coef(0)
        assert (1, 0) == cls.rot_deg_coef(360)
        assert (0, 1) == cls.rot_deg_coef(90)
        assert (0, -1) == cls.rot_deg_coef(270)
        assert (-1, 0) == cls.rot_deg_coef(180)

class Parms():
    """Named Parms."""

    symbols: dict[str, list[Self]] = {}

    @classmethod
    def clear_all(cls) -> None:
        cls.symbols: dict[str, list[Self]] = {}

    @classmethod
    def lookup(cls, name: str) -> list[Self]:
        if name not in cls.symbols:
            cls.symbols[name] = []
        return cls.symbols[name]

    @classmethod
    def add_symb(cls, inst: Self) -> list[Self]:
        name = inst.name
        if name not in cls.symbols:
            cls.symbols[name] = [inst]
        else:
            cls.symbols[name].append(inst)
        return cls.symbols[name]

    def __init__(self, name: str, val:Any, descr: str = "") -> None:
        self.name = name
        self.val = val
        self.descr = descr
        self.add_symb(self)

# --------------------------------------------------------------------
# ELECDATA/base_classes.py ends here.
