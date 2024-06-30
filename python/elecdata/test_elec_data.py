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
#  (Last Emacs Update:  Sat Jun 29, 2024 10:47 pm by Gary Delp v-0.1.22)
#
# Sat Jun 29, 2024 10:47 pm by Gary Delp v-0.1.22:
#
# Fri Jun 28, 2024 10:05 pm by Gary Delp v-0.1.22:
#
# Thu Jun 27, 2024 10:29 pm by Gary Delp v-0.1.16:
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: PYTHON/test_elec_data.py
import unittest
from typing import Final
from elec_data import ElecBase

class TestElecBase(unittest.TestCase):
    """Collect the ElecData unit tests.
    """

    # _elec_test_data:  dict[str, list[list[str]|int]] = {
    _elec_test_data: Final = {
        'short_list': [
            0, 1, 2],
        'add4': [
            ["conductors", 'm4wire', ''],
            ["inductors", 'm4wire', '1'],
            ["inductors", 'm4wire', '1'],
            ["conductors", 'm4wire', '1']]
        }

    wild_card = ['.*' for _ in range(4)]


    @classmethod
    def elec_test_data(cls, key) -> list:
        """Return the keyed sequence."""
        if key in cls._elec_test_data:
            return cls._elec_test_data[key]
        else:
            return []

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

    def test_symbols_1(self):
        """try the lookups 1."""
        lookup = ElecBase.lookup_symbol(*self.wild_card)
        self.assertEqual(0, len(lookup))

    def test_symbols_2(self):
        """try the lookups 2."""
        check = ElecBase("lib1", "bert", "v1")
        should = "<<ElecBase library=lib1, name=bert, "
        should += "dtype=ElecBase, version=v1>>"
        self.assertEqual(f'{check}', should)
        lookup = ElecBase.lookup_symbol(*self.wild_card)
        self.assertEqual(1, len(lookup))

    def test_symbols_3(self):
        """Create 3 new entities, and then try the lookups."""
        for (i, names) in enumerate(self._elec_test_data['add4']):
            tmp = ElecBase(*names)
            print(f'loop {i} {str(tmp)=}')
            lookup = ElecBase.lookup_symbol(*self.wild_card)
            self.assertEqual(i, len(lookup))
            lookup = ElecBase.lookup_symbol(
                names[0], names[1], '.*', names[2])
            if len(lookup) > 1:
                self.assertTrue(
                    tmp in lookup,
                    f'From loop {i} added {str(tmp)} returned {lookup=}')
            else:
                self.assertEqual(
                    tmp, lookup[0],
                    f'From loop {i} added {str(tmp)} returned {lookup=}')



# Local Variables:
# compile-command: "python -m unittest"
# End:
# --------------------------------------------------------------------
# test_elec_data.py ends here.
