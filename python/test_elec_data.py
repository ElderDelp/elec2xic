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
#  (Last Emacs Update:  Thu Jun 27, 2024 10:29 pm by Gary Delp v-0.1.16)
#
# Thu Jun 27, 2024 10:29 pm by Gary Delp v-0.1.16:
# --------------------------------------------------------------------
# Always start with all of the imports
# Here is the start of: PYTHON/test_elec_data.py
import unittest
from elec_data import ElecBase

class TestElecData(unittest.TestCase):
    """Collect the ElecData unit tests.
    """

    def test_elec_data_class(self):
        """The class is an instance of itself.
        """

        check = ElecBase("", "")
        print(f'{type(check)} {check=}')
        self.assertIsInstance(check, cls=ElecBase)


# Local Variables:
# compile-command: "python -m unittest"
# End:
# --------------------------------------------------------------------
# test_elec_data.py ends here.
