#=========================================================================
# SortXcelRTL_test
#=========================================================================

import pytest

from pymtl3                import *
from lab2_xcel.SortXcelRTL import SortXcelRTL

#-------------------------------------------------------------------------
# Reuse tests from FL model
#-------------------------------------------------------------------------

from .SortXcelFL_test import TestHarness, test_case_table
from .SortXcelFL_test import run_test, run_test_multiple

@pytest.mark.parametrize( **test_case_table )
def test( pytestconfig, test_params, dump_vcd, test_verilog ):
  run_test( pytestconfig, SortXcelRTL(), test_params, dump_vcd, test_verilog )

def test_multiple( pytestconfig, dump_vcd, test_verilog ):
  run_test_multiple( pytestconfig, SortXcelRTL(), dump_vcd, test_verilog )

