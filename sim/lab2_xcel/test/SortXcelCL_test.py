#=========================================================================
# SortXcelCL_test
#=========================================================================

import pytest

from pymtl3               import *
from lab2_xcel.SortXcelCL import SortXcelCL

#-------------------------------------------------------------------------
# Reuse tests from FL model
#-------------------------------------------------------------------------

from .SortXcelFL_test import TestHarness, test_case_table
from .SortXcelFL_test import run_test, run_test_multiple

@pytest.mark.parametrize( **test_case_table )
def test( pytestconfig, test_params ):
  run_test( pytestconfig, SortXcelCL(), test_params, dump_vcd=False, test_verilog=False )

def test_multiple( pytestconfig ):
  run_test_multiple( pytestconfig, SortXcelCL(), dump_vcd=False, test_verilog=False )

