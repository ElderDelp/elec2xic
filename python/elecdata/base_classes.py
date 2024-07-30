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
#  (Last Emacs Update:  Mon Jul 29, 2024  9:44 pm by Gary Delp v-0.1.26)
#
# Mon Jul 29, 2024  9:44 pm by Gary Delp v-0.1.26:
#
# Sun Jul 28, 2024 10:57 pm by Gary Delp v-0.1.26:
#
# Sat Jul 27, 2024  7:49 pm by Gary Delp v-0.1.26:
#
# Tue Jul 16, 2024  5:22 pm by Gary Delp v-0.1.20:
#
# Mon Jul 15, 2024  8:39 pm by Gary Delp v-0.1.18:
#
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: ELECDATA/base_classes.py

import functools
import math
from pathlib import Path
from typing import Self, Any, IO, Final
# from dataclasses import dataclass

import re
jelib_path:Path = Path()

class ElecReadException(ValueError):
    """Various Elect errors."""
    pass

def gsd_init_class(klass):
    """Decorator to intialize class when defined."""
    klass.cls_init()
    return klass

### ------------------------------------------------------------------
## Decorator def moved to below class ElecLine declaration
# def elec_add_line_Parser(key:str):
#     """A decorator for subclasses of ElecLine to let them register for
#     handling their "letter".
#     """
#  ...
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
class ElecLine():
    """One of these objects for every non-comment Line in JELIB."""

    reader_d: dict[str, type] = {}

    @classmethod
    def register_reader(cls, letter: str, reader: type) -> None:
        """Register a Reader subclass for lines starting with a given letter."""
        cls.reader_d[letter] = reader

    @classmethod
    def get_reader(cls, letter: str) -> type:
        """Return the Reader subclass for lines starting with a given letter."""
        if letter in cls.reader_d:
            return cls.reader_d[letter]
        err_str = f"No reader registered for {letter=}"
        raise ElecReadException(err_str)

    @classmethod
    def cls_init(cls) -> None:
        pass

    def __init__(self, text: str, container: ElecBase, line_no: int = 0) -> None:
        """Process the text and store the references."""
        self.text = text
        self.container = container
        self.line_no = line_no
        self.proc_line()

    def proc_line(self):
        pass

def elec_add_line_Parser(key:str):
    """A decorator for subclasses of ElecLine to let them register for
    handling their "letter".
    """
    the_key: str = key
    def register(klass):
        nonlocal key
        if ElecLine in klass.__bases__:
            klass.register_reader(the_key, klass)
        else:
            err_str = 'Tried to add a reader class that is not a subclass '
            err_str += f'ElecLine, new class "{klass.__name__}" is '
            err_str += f'{klass.__bases__}'
            raise ElecReadException(err_str)
        return klass
    return register


@gsd_init_class
class Location():
    """Holds (X, Y)."""

    dummy: Any = None
    small: Final[float] = math.ldexp(0.5, -24)
    this_class: type = dummy

    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y

    def shift_scale(self, shift: Self, scale: Self) -> Self:
        return type(self)((self.x + shift.x) * scale.x,
                          (self.y + shift.y) * scale.y)

    def __add__(self, other: Self) -> Self:
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Self) -> Self:
        return type(self)(self.x * other.x, self.y * other.y)

    def __truediv__(self, other: Self) -> Self:
        return type(self)(self.x / other.x, self.y / other.y)

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

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            if math.isclose(self.x, other.x, rel_tol=1e-9, abs_tol=1e-9):
                if math.isclose(self.y, other.y, rel_tol=1e-9, abs_tol=1e-9):
                    return True
            return False
        return NotImplemented

    def __neg__(self) -> Self:
        return type(self)(-self.x, -self.y)

    def flip_v(self, other: Self) -> Self:
        return type(self)(self.x, 2 * other.y - self.y )

    def flip_h(self, other: Self) -> Self:
        return type(self)(2 * other.x - self.x, self.y)

    def rot_deg(self, deg: float) -> Self:
        (c, s) = self.rot_deg_coef(deg)
        return type(self)(c * self.x - s * self.y, s * self.x + c * self.y)

    def rot_rad(self, rad: float) -> Self:
        (c, s) = self.rot_rad_coef(rad)
        return type(self)(c * self.x - s * self.y, s * self.x + c * self.y)

    @classmethod
    def round_0_000001(cls, inp: float) -> float:
        """Return a float that is rounded to 24 fractional bits."""
        if math.fabs(inp) < cls.small:
            return 0.0
        return inp

    @staticmethod
    @functools.cache
    def rot_rad_coef(rad: float) -> list[float]:
        ret = [math.cos(rad), math.sin(rad)]
        return ret

    @classmethod
    @functools.cache
    def rot_deg_coef(cls, deg: float) -> list[float]:
        c, s = cls.rot_rad_coef(math.radians(deg))
        return [cls.round_0_000001(c), cls.round_0_000001(s) ]

    @classmethod
    def cls_init(cls) -> None:
        """Allocate the class constant instance: ElecNone."""
        cls.this_class = cls
        assert [1, 0] == cls.rot_deg_coef(0)
        assert [1, 0] == cls.rot_deg_coef(360)
        assert [0, 1] == cls.rot_deg_coef(90)
        assert [0, -1] == cls.rot_deg_coef(270)
        assert [-1, 0] == cls.rot_deg_coef(180)


class ElecCellRef(ElecBase):
    """Class for Cell References."""

    def __init__(self, library:str, name:str, version:str = "") -> None:
        super().__init__(library, name, version)

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
