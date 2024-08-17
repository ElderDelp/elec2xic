#!/bin/env python3
# --------------------------------------------------------------------
#  W R X I C / t e s t _ w r _ s h a p e s . p y
#  created Wed Aug  7, 2024  7:12 pm by: Gary Delp <Gary.Delp@slsmn.com>
# --------------------------------------------------------------------
#   Copyright (c) 2024 SilverLoonSystems. All Rights Reserved
#    Worldwide. Licensed under the Apache License, Version 2.0
# --------------------------------------------------------------------
"""Commentary:

"""

# --------------------------------------------------------------------
#  (Last Emacs Update:  Sat Aug 17, 2024 12:49 am by Gary Delp v-0.1.12)
#
# Sat Aug 17, 2024 12:03 am by Gary Delp v-0.1.10:
#
# Thu Aug 15, 2024 11:12 pm by Gary Delp v-0.1.6:
#
#  Wed Aug  7, 2024  7:12 pm by Gary Delp v-0.1.0:
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: WRXIC/test_wr_shapes.py
import unittest
from __init__ import WrLayout, LBox

class TestWrShapes(unittest.TestCase):
    """Collect the WrShapes unit tests.
    """

    def test_wr_shp_layout_cls(self):
        """The class is an instance of itself.
        """

        self.assertIsInstance(WrLayout(), WrLayout)

    def test_wr_via(self):
        """Check is a simple via stack as a component works.
        """
        t = ''
        self.assertMultiLineEqual(' ', ' ')
        t += """# Cell M3M5hole;1{lay}
        CM3M5hole;1{lay}||josephson-5ee-v1|1636582252407|1638370929302|E|DRC_last_good_drc_area_date()G1636641912623|DRC_last_good_drc_bit()I34|DRC_last_good_drc_date()G1638371069697
        Ngeneric:Facet-Center|art@0||0|0||||AV
        NM3-M4-Con|contact@0||0|-7|||R|
        NM4-M5-Con|contact@1||0|7|||R|
        NM4-Pin|pin@0||0|7|||R|
        NM4-Pin|pin@1||-14|-20|||R|
        NM4-Pin|pin@2||-14|21|||R|
        NM4-Pin|pin@3||14|21|||R|
        NM4-Pin|pin@5||14|-20|||R|
        NM5-Pin|pin@8||0|-6||||
        NM5-Node|plnode@0||0|0.5|27|7|R|
        NM3-Node|plnode@1||0|0|16|20|R|
        NM3-Node|plnode@2||0|0|20|20||
        AM4|net@0||8.5|S2700|contact@0||0|-7|pin@0||0|7
        AM4|net@1||10.5|S900|contact@1||0|7|pin@0||0|7
        AM4|net@2||0.5|S2700|pin@1||-14|-20|pin@2||-14|21
        AM4|net@3||0.5|S1800|pin@2||-14|21|pin@3||14|21
        AM4|net@6||0.5|S1800|pin@1||-14|-20|pin@5||14|-20
        AM4|net@7||0.5|S900|pin@3||14|21|pin@5||14|-20
        AM5|net@10|||S|contact@1||0|7|plnode@0||0|7
        AM3|net@11|||S2700|contact@0||0|-7|plnode@1||0|0
        AM5|net@12||7|S900|contact@1||0|7|pin@8||0|-6
        AM3|net@13|||S|contact@0||0|-7|plnode@2||0|-7
        Egnd4m|gnd_4m|D5G3;|pin@2||G
        Efnd_4m|gnd_4m_1|D5G3;|pin@5||G
        Egnd_4m_2||D5G2;|pin@1||G
        Egnd+4m|gnd_4m_3|D5G2;|pin@3||G
        EM5|vdd_M5|D5G4;X6.5;|plnode@0||P
        Evdd|vdd_m3|D5G10;|plnode@1||P
        """

    def test_write_con(self):
        """Does it work."""

        ref = """(Symbol M3-M4-Con);
($Id:$);
(xic 4.3.13 LinuxUbuntu22 x86_64 08/16/2024 02:58 GMT);
(PHYSICAL);
(RESOLUTION 10000);
( CREATED 8/16/2024 2:58:24, MODIFIED 8/16/2024 2:58:24 );
9 M3-M4-Con;
DS 0 1 1;
L M3;
B 12000 12000 0 0;
L I3;
B 6000 6000 0 0;
L M4;
B 12000 12000 0 0;
DF;
E
"""
        sstr = '4.3.13 LinuxUbuntu22 x86_64 08/16/2024 02:58 GMT'
        tsstr = 'CREATED 8/16/2024 2:58:24, MODIFIED 8/16/2024 2:58:24'
        wl = WrLayout(sstr, tsstr)
        self.assertEqual(wl.verss, sstr)
        self.assertEqual(wl.tm_str, tsstr)
        resp = wl.write_con(LBox("M3", 6), LBox("I3", 3), LBox("M4", 6))
        self.assertMultiLineEqual(resp, ref)


# Local Variables:
# compile-command: "python -m unittest --verbose"
# End:
# --------------------------------------------------------------------
# test_wr_shapes.py ends here.
