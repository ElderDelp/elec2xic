#!/bin/env python3
# --------------------------------------------------------------------
#  W R X I C / w r _ l a y o u t . p y
#  created Thu Aug 15, 2024 11:15 pm by: Gary Delp <Gary.Delp@slsmn.com>
# --------------------------------------------------------------------
#   Copyright (c) 2024 SilverLoonSystems. All Rights Reserved
#    Worldwide. Licensed under the Apache License, Version 2.0
# --------------------------------------------------------------------
"""Commentary:

"""

# --------------------------------------------------------------------
#  (Last Emacs Update:  Sat Aug 17, 2024 12:44 am by Gary Delp v-0.1.10)
#
# Sat Aug 17, 2024 12:03 am by Gary Delp v-0.1.6:
#
# Thu Aug 15, 2024 11:16 pm by Gary Delp v-0.1.2:
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: WRXIC/wr_layout.py
# from typing import List
from base_classes import LBox
from time import gmtime

class WrLayout():
    """Write MIT-LL base library objects."""



    def __init__(self,
                 verss: str | None = None,
                 tm_str:str | None = None,
                 # *args, **kwargs
                 ) -> None:
        """Initialize the version and creation strings."""
        if verss is None:
            verss = '4.3.13 LinuxUbuntu22 x86_64 08/16/2024 02:58 GMT'
        if tm_str is None:
            gmt = gmtime(None)
            tm_str = f'{gmt.tm_mon:>2d}/{gmt.tm_mday:02d}/{gmt.tm_year:04d}'
            tm_str += f' {gmt.tm_hour:02d}:{gmt.tm_min:02d}:{gmt.tm_sec}'
            tm_str = f'CREATED {tm_str}, MODIFIED {tm_str}'
        self.verss:str = verss
        self.tm_str:str = tm_str

    def write_con(self, l1:LBox, i2:LBox, l3:LBox) -> str:
        """Return the string"""
        name:str = f'{l1.layer}-{l3.layer}-Con'
        ret:str = f'(Symbol {name});\n'
        ret += '($Id:$);\n'
        ret += f'(xic {self.verss});\n'
        ret += '(PHYSICAL);\n(RESOLUTION 10000);\n'
        ret += f'( {self.tm_str} );\n'
        ret += f'9 {name};\n'
        ret += 'DS 0 1 1;\n'
        for lay in (l1, i2, l3):
            w, h, x, y = lay[1:]
            if h is None:
                h = lay.w
            w, h = w * 2, h *2
            ret += f'L {lay.layer};\nB'
            for d in [w, h, x, y]:
                ret += f' {int(d* 1000):d}'
            ret += ';\n'
        ret += 'DF;\nE\n'
        return ret


# --------------------------------------------------------------------
# wr_layout.py ends here.
