#=========================================================================
# SortXcelFL_test
#=========================================================================

import pytest
import random
import struct

random.seed(0xdeadbeef)

from pymtl3 import *
from pymtl3.stdlib.ifcs.xcel_ifcs import XcelMasterIfcCL
from pymtl3.stdlib.test import TestMasterCL, mk_test_case_table, run_sim, config_model
from pymtl3.stdlib.cl.MemoryCL import MemoryCL

from proc.XcelMsg import *

from lab2_xcel.SortXcelFL  import SortXcelFL

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, xcel ):

    s.tm   = TestMasterCL( XcelMsgs.req, XcelMsgs.resp, XcelMasterIfcCL )
    s.mem  = MemoryCL( 1 )
    s.xcel = xcel

    s.tm.master  //= s.xcel.xcel
    s.mem.ifc[0] //= s.xcel.mem

  def done( s ):
    return s.tm.done()

  def line_trace( s ):
    return "{}|{} > {}".format(
      s.tm.line_trace(), s.mem.line_trace(), s.xcel.line_trace()
    )

#-------------------------------------------------------------------------
# make messages
#-------------------------------------------------------------------------

def req( type_, raddr, data ):
  return XcelReqMsg(XCEL_TYPE_READ if type_ == 'rd' else XCEL_TYPE_WRITE, raddr, data)

def resp( type_, data ):
  return XcelRespMsg(XCEL_TYPE_READ if type_ == 'rd' else XCEL_TYPE_WRITE, data)

#-------------------------------------------------------------------------
# Xcel Protocol
#-------------------------------------------------------------------------
# These are the source sink messages we need to configure the accelerator
# and wait for it to finish. We use the same messages in all of our
# tests. The difference between the tests is the data to be sorted in the
# test memory.

def gen_xcel_protocol_msgs( base_addr, size ):
  return [
    req( 'wr', 1, base_addr ), resp( 'wr', 0 ),
    req( 'wr', 2, size      ), resp( 'wr', 0 ),
    req( 'wr', 0, 0         ), resp( 'wr', 0 ),
    req( 'rd', 0, 0         ), resp( 'rd', 1 ),
  ]

#-------------------------------------------------------------------------
# Test Cases
#-------------------------------------------------------------------------

mini          = [ 0x21, 0x14, 0x42, 0x03 ]
small_data    = [ random.randint(0,0xffff)     for i in range(32) ]
large_data    = [ random.randint(0,0x7fffffff) for i in range(32) ]
sort_fwd_data = sorted(small_data)
sort_rev_data = list(reversed(sorted(small_data)))
nonpow2_size  = [ random.randint(0,0xffff)     for i in range(35) ]

#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
                         #                delays   test mem
                         #                -------- ---------
  (                      "data            src sink stall lat"),
  [ "mini",               mini,           0,  0,   0,    0   ],
  [ "mini_delay_3x14x4",  mini,           3, 14,   0.5,  2   ],
  # [ "mini_delay_5x7",     mini,           5,  7,   0.5,  4   ],
  [ "small_data",         small_data,     0,  0,   0,    0   ],
  [ "large_data",         large_data,     0,  0,   0,    0   ],
  [ "sort_fwd_data",      sort_fwd_data,  0,  0,   0,    0   ],
  [ "sort_rev_data",      sort_rev_data,  0,  0,   0,    0   ],
  [ "nonpow2_size",       nonpow2_size,   0,  0,   0,    0   ],
  [ "small_data_3x14x0",  small_data,     3, 14,   0,    0   ],
  # [ "small_data_5x7x0",   small_data,     5,  7,   0,    0   ],
  [ "small_data_0x0x4",   small_data,     0,  0,   0.5,  4   ],
  [ "small_data_3x14x4",  small_data,     3,  14,  0.5,  4   ],
  # [ "small_data_5x7x4",   small_data,     5,  7,   0.5,  4   ],
])

#-------------------------------------------------------------------------
# run_test
#-------------------------------------------------------------------------

def run_test( pytestconfig, xcel, test_params, dump_vcd=False, test_verilog=False ):

  # Convert test data into byte array

  data = test_params.data
  data_bytes = struct.pack("<{}I".format(len(data)),*data)

  # Protocol messages

  xcel_protocol_msgs = gen_xcel_protocol_msgs( 0x1000, len(data) )

  # Create test harness with protocol messagse

  th = TestHarness( xcel )

  th.set_param( "top.tm.src.construct", msgs=xcel_protocol_msgs[::2],
    initial_delay=test_params.src+3, interval_delay=test_params.src )

  th.set_param( "top.tm.sink.construct", msgs=xcel_protocol_msgs[1::2],
    initial_delay=test_params.sink+3, interval_delay=test_params.sink )

  th.set_param( "top.mem.construct",
    stall_prob=test_params.stall, latency=test_params.lat+1 )

  # Run the test

  th.elaborate()

  # Load the data into the test memory

  th.mem.write_mem( 0x1000, data_bytes )

  config_model( th, dump_vcd, test_verilog, ['xcel'] )

  run_sim( th, pytestconfig=pytestconfig, max_cycles=20000 )

  # Retrieve data from test memory

  result_bytes = th.mem.read_mem( 0x1000, len(data_bytes) )

  # Convert result bytes into list of ints

  result = list(struct.unpack("<{}I".format(len(data)),result_bytes))

  # Compare result to sorted reference

  assert result == sorted(data)

#-------------------------------------------------------------------------
# run_test_multiple
#-------------------------------------------------------------------------
# We want to make sure we can use our accelerator multiple times, so we
# create an array of 32 elements and then we use the accelerator to sort
# the first four elements, the second four elements, etc.

def run_test_multiple( pytestconfig, xcel, dump_vcd=False, test_verilog=False ):

  # Convert test data into byte array

  random.seed(0xdeadbeef)

  data = [ random.randint(0,0xffff) for i in range(32) ]
  data_bytes = struct.pack("<{}I".format(len(data)),*data)

  # Protocol messages

  base_addr = 0x1000
  msgs = []

  for i in range(8):
    msgs.extend( gen_xcel_protocol_msgs( base_addr+i*16, 4 ) )

  # Create test harness with protocol messagse

  th = TestHarness( xcel )

  th.set_param( "top.tm.src.construct", msgs=msgs[::2],
    initial_delay=6, interval_delay=3 )

  th.set_param( "top.tm.sink.construct", msgs=msgs[1::2],
    initial_delay=10, interval_delay=7 )

  th.set_param( "top.mem.construct", stall_prob=0.5, latency=3 )

  # Run the test

  th.elaborate()

  # Load the data into the test memory

  th.mem.write_mem( 0x1000, data_bytes )

  config_model( th, dump_vcd, test_verilog, ['xcel'] )

  run_sim( th, pytestconfig=pytestconfig, max_cycles=20000 )

  # Retrieve data from test memory

  result_bytes = th.mem.read_mem( 0x1000, len(data_bytes) )

  # Convert result bytes into list of ints

  result = list(struct.unpack("<{}I".format(len(data)),result_bytes))

  # Compare result to sorted reference

  for i in range(8):
    assert result[i*4:i*4+4] == sorted(data[i*4:i*4+4])

#-------------------------------------------------------------------------
# Test cases
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test( pytestconfig, test_params ):
  run_test( pytestconfig, SortXcelFL(), test_params, dump_vcd=False, test_verilog=False )

def test_multiple( pytestconfig ):
  run_test_multiple( pytestconfig, SortXcelFL(), dump_vcd=False, test_verilog=False )

