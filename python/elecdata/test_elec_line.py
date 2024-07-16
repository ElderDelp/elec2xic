#!/bin/env python3
# --------------------------------------------------------------------
#  E L E C D A T A / t e s t _ e l e c _ l i n e . p y
#  created Thu Jul  4, 2024  4:33 pm by: Gary Delp <Gary.Delp@slsmn.com>
# --------------------------------------------------------------------
#   Copyright (c) 2024 SilverLoonSystems. All Rights Reserved
#    Worldwide. Licensed under the Apache License, Version 2.0
# --------------------------------------------------------------------
"""Commentary:

"""

# --------------------------------------------------------------------
#  (Last Emacs Update:  Tue Jul 16, 2024  5:45 pm by Gary Delp v-0.1.12)
#
# Sat Jul 13, 2024 10:09 pm by Gary Delp v-0.1.4:
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: ELECDATA/test_elec_line.py
import unittest
from io import StringIO
from __init__ import (
    ElecLine, ElecBase, ElecReadException,
    JeLIB,
    )

class TestElecLine(unittest.TestCase):
    """Collect the ElecLine unit tests.
    """

    jelib_lines = """
# header information:
Hconductors|9.08e

# Views:
Vicon|ic
Vlayout|lay
Vschematic|sch

# Tools:
Ouser|DefaultTechnology()Sjosephson-5ee-v1|PSubstrateProcess()BF|SchematicTechnology()Sjosephson-5ee-v1|SoftTechnologies()S"\\\\millenium\\Contracts\\Prairie2_0024\\RgFon01\\work\\delp\\gits\\theGood\\2023-10-16-delp-elec\\SFQ5ee\\josephson-5ee-v1.xml"

# Cell AGallery;1{ic}
CAGallery;1{ic}||artwork|1604241019401|1604241081665|E
Ngeneric:Facet-Center|art@0||0|0||||AV
NOpened-Thicker-Polygon|art@1||0|0|6|10|||SCHEM_function(D5G1.5;)SAGallery|trace()V[-3/-5,-3/5,3/5,3/-5,-3/-5]
Ngeneric:Invisible-Pin|pin@0||0|-2|||||ART_message(D5G1;)S[of bias,conductors]
X

# Cell AGallery;1{lay}
CAGallery;1{lay}||josephson-5ee-v1|1605553286109|1638116795609|E|DRC_last_good_drc_area_date()G1638116799113|DRC_last_good_drc_bit()I34|DRC_last_good_drc_date()G1638116799113
Ngeneric:Facet-Center|art@0||0|0||||AV
Ibias0p5;1{lay}|bias0p5@0||-204.5|0|||D5G4;
Ibias0p7;1{lay}|bias0p7@0||-185|0|||D5G4;
Ibias1p0;2{lay}|bias1p0@0||-166|0|||D5G4;
Ibias1p4;3{lay}|bias1p4@0||-147|0|||D5G4;
Ibias1p7;1{lay}|bias1p7@0||-90|0|||D5G4;
Ibias1p7w;1{lay}|bias1p7w@0||37|0|||D5G4;
Ibias1p55;1{lay}|bias1p55@0||-128|0|||D5G4;
Ibias1p66;1{lay}|bias1p66@0||-109|0|||D5G4;
Ibias2p8;1{lay}|bias2p8@0||-33|0|||D5G4;
Ibias2p8w;2{lay}|bias2p8w@0||94|0|||D5G4;
Ibias2p414;2{lay}|bias2p41@0||-52|0|||D5G4;
Ibias2p414w;2{lay}|bias2p41@1||75|0|||D5G4;
Ibias3p414w;3{lay}|bias3p41@0||113|0|||D5G4;
Ibias4p242;1{lay}|bias4p24@0||132|0|||D5G4;
Icon1p0w;1{lay}|con1p0w@0||-1|0|||D5G4;
Icon1p4w;2{lay}|con1p4w@0||18|0|||D5G4;
Ibias2p0;2{lay}|con2p0@0||-71|0|||D5G4;
Ibias2p0w;2{lay}|con2p0w@0||56|0|||D5G4;
Ngeneric:Invisible-Pin|pin@5||-63|99|||||ART_message(D5G15;)SAGallery
Ngeneric:Invisible-Pin|pin@6||-60.5|82|||||ART_message(D5G8;)S[of bias conductors,NOT damping resistors]
Ngeneric:Invisible-Pin|pin@7||-61.5|68|||||ART_message(D5G8;)Ssee 2020-is65 for information
X

# Cell AGallery;1{sch}
CAGallery;1{sch}||schematic|1604239895796|1681918119906|E
IAGallery;1{ic}|AGallery@0||16.5|38|||D5G4;
IanyBiasConductor;1{ic}|anyBiasC@1||-12|16|||D5G4;|ATTR_Lk(D5G1.5;NOJPX-0.5;)S1@Lk
Ngeneric:Facet-Center|art@0||0|0||||AV
Ibias0p5;1{ic}|bias0p5@0||-42|24|||D5G4;
Ibias1p0;1{ic}|bias1p0@0||-30|24|||D5G4;
Ibias0p7;1{ic}|bias1p0@1||-36|24|||D5G4;
Ibias1p4V;1{ic}|bias1p4@0||-24|24|||D5G4;
Ibias2p0V;1{ic}|bias2p0@0||-28.5|17|||D5G4;
Ibias2p0V;1{ic}|bias2p0@1||-18|24|||D5G4;
Ibias2p8;1{ic}|bias2p8@0||-12|24|||D5G4;
Ibias2p414;1{ic}|bias2p41@0||-6|24|||D5G4;
Ibias3p414;1{ic}|bias3p41@0||0|24|||D5G4;
IanyBias;1{ic}|normaliz@0||-21|17|||D5G4;|ATTR_Lk(D5G1.5;NOJPX0.5;Y0.5;)S1.12
IanyBiasConductor;1{ic}|normaliz@1||4.5|23.5|||D5G4;|ATTR_Lk(D5G1.5;NOJPX-0.5;)S4
IanyBiasConductor;1{ic}|normaliz@2||4.5|23.5|||D5G4;|ATTR_Lk(D5G1.5;NOJPX-0.5;)S4
Ngeneric:Invisible-Pin|pin@0||-15.5|44.5|||||ART_message(D5G6;)SAGallery
Ngeneric:Invisible-Pin|pin@1||-15.5|39.5|||||ART_message(D5G3;)Sof Bias Conductors
Ngeneric:Invisible-Pin|pin@2||-17|32|||||ART_message(D5G3;)Sies 27 February 2021
Ngeneric:Invisible-Pin|pin@3||-15|36|||||ART_message(D5G3;)Ssee memo 2020-65
X
"""

    def test_elec_line_class(self):
        """The class is an instance of itself.
        """

        self.assertIsInstance(
            ElecLine(
                "CAGallery;1{sch}||schematic|1604239895796|1681918119906|E",
                container=ElecBase.ElecNone), ElecLine)
    def test_jelib_read_loop_fail(self):
        """Does JeLIB fail if input does not start with an H line."""
        inp = StringIO("#\nAGallery\n")
        def err() -> JeLIB:
            nonlocal inp
            return JeLIB(inp, "err", "should", "fail")

        self.assertRaises(ElecReadException, err)

# --------------------------------------------------------------------
# Local Variables:
# compile-command: "python -m unittest"
# End:
# --------------------------------------------------------------------
# test_elec_line.py ends here.
