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
#  (Last Emacs Update:  Mon Jul  1, 2024  9:00 pm by Gary Delp v-0.1.24)
#
# Mon Jul  1, 2024  9:00 pm by Gary Delp v-0.1.24:
#
# Sun Jun 30, 2024  8:12 pm by Gary Delp v-0.1.24:
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
import pprint

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
            ["conductors", 'm4wire', '1']
        ],
        'elec_base_str': [
            ["lib1", 'bert', 'v1'],
            ["lib1", 'ernie', 'v1'],
            ["lib1", 'cookiemonster', 'v1']
        ]
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
        sep = "', '"
        tlist = self._elec_test_data['elec_base_str']
        objs = []
        for (i, names) in enumerate(tlist):
            check = ElecBase(*names)
            objs.append(check)
            should = f"<<ElecBase library={names[0]}, name={names[1]}, "
            should += f"dtype=ElecBase, version={names[2]}>>"
            self.assertEqual(
                f'{str(check)}',
                should,
                f"Loop {i}: '{sep.join(names)}'")


    def test_symbols_1(self):
        """try the lookups 1."""
        sep = "', '"
        tlist = self._elec_test_data['elec_base_str']
        lookup = ElecBase.lookup_symbol(*self.wild_card)
        self.assertEqual(0, len(lookup))
        for (i, names) in enumerate(tlist):
            check = ElecBase(*names)
            lib_dict = check._name_dict[names[0]]
            self.assertEqual(
                lib_dict,
                check.name_db['library'][1],
                f"Loop {i}: '{sep.join(names)}'")
            name_dict = lib_dict[names[1]]
            self.assertEqual(
                name_dict,
                check.name_db['name'][1],
                f"Loop {i}: '{sep.join(names)}'")
            name_dict = lib_dict[names[1]]
            self.assertEqual(
                name_dict,
                check.name_db['name'][1],
                f"Loop {i}: '{sep.join(names)}'")
            name_dict = lib_dict[names[1]]
            self.assertEqual(
                name_dict,
                check.name_db['name'][1],
                f"Loop {i}: '{sep.join(names)}'")

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
            # self.assertEqual(i, len(lookup))
            lookup = ElecBase.lookup_symbol(
                names[0], names[1], '.*', names[2])
            if len(lookup) == 0:
                pprint.pprint(ElecBase._name_dict)
            elif len(lookup) > 1:
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
