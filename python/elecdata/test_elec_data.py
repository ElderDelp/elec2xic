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
#  (Last Emacs Update:  Sun Aug  4, 2024  5:54 pm by Gary Delp v-0.1.58)
#
# Sun Aug  4, 2024  5:54 pm by Gary Delp v-0.1.58:
#
# Thu Aug  1, 2024  8:43 pm by Gary Delp v-0.1.56:
#
# Sun Jul 28, 2024 10:27 pm by Gary Delp v-0.1.56:
#
# Mon Jul 15, 2024  9:18 pm by Gary Delp v-0.1.56:
#     Tests pass this version
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: PYTHON/test_elec_data.py
import unittest
from typing import Final
from __init__ import (
    ElecBase, Parms, ElecLine, Location,
    ElecCell,
    ElecCellLayout, ElecCellSchematic, ElecCellIcon
)
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
            dtype_dict = name_dict[check.__class__.__name__]
            self.assertEqual(
                dtype_dict,
                check.name_db['dtype'][1],
                f"Loop {i}: '{sep.join(names)}'")
            version_set = dtype_dict[names[2]].collide
            self.assertTrue(
                check in version_set,
                f"Loop {i}: '{sep.join(names)}'")

    def test_symbols_2(self):
        """try the lookups 2."""
        check = ElecBase("lib1", "bert", "v1")
        should = "<<ElecBase library=lib1, name=bert, "
        should += "dtype=ElecBase, version=v1>>"
        self.assertEqual(f'{check}', should)
        lookup = check.lookup_symbol(*self.wild_card)
        self.assertEqual(1, len(lookup))

    def test_symbols_3(self):
        """Create 3 new entities, and then try the lookups."""
        for (i, names) in enumerate(self._elec_test_data['add4']):
            tmp = ElecBase(*names)
            print(f'\nloop {i} {str(tmp)=}')
            lookup = ElecBase.lookup_symbol(*self.wild_card)
            # self.assertEqual(i, len(lookup))
            lookup = ElecBase.lookup_symbol(
                names[0], names[1], '.*', names[2])
            if len(lookup) == 0:
                pprint.pprint(ElecBase._name_dict, indent=4, width=75)
            elif len(lookup) > 1:
                self.assertTrue(
                    tmp in lookup,
                    f'From loop {i} added {str(tmp)} returned {lookup=}')
            else:
                self.assertEqual(
                    tmp, lookup[0],
                    f'From loop {i} added {str(tmp)} returned {lookup=}')

class TestParms(unittest.TestCase):
    """Collect the ElecData unit tests.
    """

    def test_elec_parms_class(self):
        """The class is an instance of itself."""
        check = Parms("Lik", '', '1')
        print(f'{type(check)} {check=}')
        self.assertIsInstance(check, cls=Parms)


class TestElecLine(unittest.TestCase):
    """Collect the ElecData unit tests.
    """

    def test_elec_line(self):
        """The class produces an instance of itself."""
        check = ElecLine("Hconductors|9.08e", ElecBase.ElecNone)
        print(f'{type(check)} {check=}')
        self.assertIsInstance(check, cls=ElecLine)


class TestElecCell(unittest.TestCase):
    """Collect the ElecData unit tests.
    """

    def test_elec_cell_body(self):
        """The class produces an instance of itself."""
        check = ElecCell("conductors", "classtest", "v0")
        print(f'{type(check)} {check=}')
        self.assertIsInstance(check, cls=ElecCell)


class TestElecCellLayout(unittest.TestCase):
    """Collect the ElecCellLayout unit tests.
    """

    def test_elec_cell_body_layout(self):
        """The class produces an instance of itself."""
        check = ElecCellLayout("conductors", "classtest", "v0")
        print(f'{type(check)} {check=}')
        self.assertIsInstance(check, cls=ElecCellLayout)


class TestElecCellCircuit(unittest.TestCase):
    """Collect the ElecCellCircuit. unit tests.
    """

    def test_elec_cell_body_circuit(self):
        """The class produces an instance of itself."""
        check = ElecCellCircuit("conductors", "classtest", "v0")
        print(f'{type(check)} {check=}')
        self.assertIsInstance(check, cls=ElecCellCircuit)


class TestElecCellIcon(unittest.TestCase):
    """Collect the ElecCellIcon. unit tests.
    """

    def test_elec_cell_body_icon(self):
        """The class produces an instance of itself."""
        check = ElecCellIcon("conductors", "classtest", "v0")
        print(f'{type(check)} {check=}')
        self.assertIsInstance(check, cls=ElecCellIcon)


class TestLocation(unittest.TestCase):
    """Simple checks on location."""

    def setUp(self) -> None:
        """ Setup to ckeck scaling of a components."""
        self.component_points: list[Location] = [
            Location(-6, -6), Location(6, 6), Location(0, 0),
            Location(-6, -4), Location(-6, -2), Location(-6, 0),
            Location(-6, 2), Location(-6, 4),
            Location(6, -4), Location(6, -2), Location(6, 0),]
        return super().setUp()

    def test_location_xform(self):
        self.assertEqual([1, 0], Location.rot_deg_coef(0))
        self.assertEqual([1, 0], Location.rot_deg_coef(360))
        self.assertEqual([0, 1], Location.rot_deg_coef(90))
        self.assertEqual([0, -1], Location.rot_deg_coef(270))
        self.assertEqual([-1, 0], Location.rot_deg_coef(180))

    def test_location_scale(self):
        print('calling test_location_scale')
        result: list[Location] = []
        scale = Location(1, 1)
        for a in self.component_points:
            self.assertTrue(a == a*scale)
        for a in self.component_points:
            result.append(a)
        self.assertEqual(result, self.component_points)


# Local Variables:
# compile-command: "python -m unittest --verbose"
# End:
# --------------------------------------------------------------------
# test_elec_data.py ends here.
