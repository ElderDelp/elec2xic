#!/bin/env python3
# --------------------------------------------------------------------
#  P Y T H O N / t e s t _ e l e c _ d a t a . p y
#  created Thu Jun 27, 2024  5:18 pm by: Gary Delp <Delp.Gary@mayo.edu>
# --------------------------------------------------------------------
#   Copyright (c) 2024 by The Mayo Clinic, though its Special Purpose
#    Processor Development Group (SPPDG). All Rights Reserved
#    Worldwide. Licensed under the Apache License, Version 2.0
# --------------------------------------------------------------------
"""Commentary:

"""

# --------------------------------------------------------------------
#  (Last Emacs Update:  Fri Jun 28, 2024 10:05 pm by Gary Delp v-0.1.22)
#
# Fri Jun 28, 2024 10:05 pm by Gary Delp v-0.1.22:
#
# Thu Jun 27, 2024 10:29 pm by Gary Delp v-0.1.16:
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: PYTHON/test_elec_data.py
import unittest
from elec_data import ElecBase

class TestElecBase(unittest.TestCase):
    """Collect the ElecData unit tests."""

    _elec_test_data: dict[str, list] = {
        'short_list': [
            0, 1, 2]
        }

    @property
    @classmethod
    def elec_test_data(cls, key) -> list:
        """Return the keted sequence."""
        return cls._elec_test_data[key]

    def setUp(self) -> None:
        ElecBase.reset_name_dict()
        return super().setUp()

    def test_elec_base_class(self):
        """The class is an instance of itself."""
        check = ElecBase("", "")
        print(f'{type(check)} {check=}')
        self.assertIsInstance(check, cls=ElecBase)
        self.assertEqual(ElecBase.ElecNone, ElecBase.ElecNone)

    def test_elec_base_str(self):
        """Test the _str_ function."""
        check = ElecBase("lib1", "bert", "v1")
        should = "<<ElecBase library=lib1, name=bert, "
        should += "dtype=ElecBase, version=v1>>"
        self.assertEqual(f'{check}', should)


# Local Variables:
# compile-command: "python -m unittest"
# End:
# --------------------------------------------------------------------
# test_elec_data.py ends here.
