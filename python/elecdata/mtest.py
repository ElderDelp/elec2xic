#!/bin/env python3
# --------------------------------------------------------------------
#  E L E C D A T A / m t e s t . p y
#  created Mon Jul 22, 2024 10:11 pm by: Gary Delp <Gary.Delp@slsmn.com>
# --------------------------------------------------------------------
#   Copyright (c) 2024 SilverLoonSystems. All Rights Reserved
#    Worldwide. Licensed under the Apache License, Version 2.0
# --------------------------------------------------------------------
"""Commentary:

"""

# --------------------------------------------------------------------
#  (Last Emacs Update:  Sun Jul 28, 2024  9:44 pm by Gary Delp v-0.1.2)
#
# Sun Jul 28, 2024  9:44 pm by Gary Delp v-0.1.2:
#
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: ELECDATA/mtest.py
from io import StringIO
from __init__ import JeLIB
import pdb
inp = StringIO("Herr|9.08e|||\n")
pdb.set_trace()
j = JeLIB(inp, "err", "should", "work")
inp = StringIO("Her1r|9.08e|||\n")
j = JeLIB(inp, "err", "shouldnot", "work")
print(str(j))

# --------------------------------------------------------------------
# mtest.py ends here.
