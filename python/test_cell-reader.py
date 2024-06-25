#!/bin/env python3
# --------------------------------------------------------------------
#  P Y T H O N / t e s t _ c e l l - r e a d e r . p y
#  created Mon Jun 24, 2024  8:28 pm by: Gary Delp <Gary.Delp@slsmn.com>
# --------------------------------------------------------------------
#   Copyright (c) 2024 SilverLoonSystems. All Rights Reserved
#    Worldwide. Licensed under the Apache License, Version 2.0
# --------------------------------------------------------------------
"""Commentary:

"""

# --------------------------------------------------------------------
#  (Last Emacs Update:  Mon Jun 24, 2024  8:28 pm by Gary Delp v-0.1.2)
#
#  Mon Jun 24, 2024  8:28 pm by Gary Delp v-0.1.0:
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: PYTHON/test_cell-reader.py
import unittest
from cell-reader import Cell-Reader

class TestCell-Reader(unittest.TestCase):
    """Collect the Cell-Reader unit tests.
    """

    def test_cell-reader_class(self):
        """The class is an instance of itself.
        """

        self.assertIsInstance(Cell-Reader(), Cell-Reader)

# --------------------------------------------------------------------
# test_cell-reader.py ends here.
