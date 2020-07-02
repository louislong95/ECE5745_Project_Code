#=========================================================================
# step test
#=========================================================================

from pymtl3             import *
from pymtl3.passes.backends.verilog import \
    VerilatorImportConfigs, TranslationConfigs
from pymtl3.stdlib.test import run_test_vector_sim, config_model
#need to change the name of the module
#from lab1_imul.IntMulVarLatCalcShamtRTL import IntMulVarLatCalcShamtRTL
from submodule.IxRTL import IxVRTL
import random
#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------

def test_basic( dump_vcd, test_verilog ):
  #dut = IntMulVarLatCalcShamtRTL()     #need to change the name
  dut = IxVRTL(3)

  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    #('req_msg_a      req_msg_b    presum       resp_msg*   a_shift*'),
    ('image_in[0]  image_in[1] image_in[2] image_in[3] image_in[4] image_in[5] image_in[6] image_in[7] image_in[8] image_in[9] image_in[10] image_in[11] image_in[12] image_in[13] image_in[14] image_out[0]* image_out[1]* image_out[2]* image_out[3]* image_out[4]* image_out[5]* image_out[6]* image_out[7]* image_out[8]*'),
    [b32(0),       b32(1),     b32(2),     b32(3),     b32(4),     b32(5),     b32(6),     b32(7),     b32(8),     b32(9),     b32(10),     b32(11),     b32(12),     b32(13),     b32(14),     b32(2),       b32(2),       b32(2),       b32(2),       b32(2),       b32(2),       b32(2),       b32(2),       b32(2)],
    [b32(0),       b32(1),     b32(7),     b32(3),     b32(0),     b32(5),     b32(6),     b32(7),     b32(8),     b32(8),     b32(4),      b32(2),      b32(9),      b32(6),      b32(3),      b32(7),       b32(2),       b32(-7),      b32(2),       b32(2),       b32(1),       b32(5),       b32(4),       b32(-6)],
  ] )

def test_zeros( dump_vcd, test_verilog ):
  #dut = IntMulVarLatCalcShamtRTL()     #need to change the name
  dut = IxVRTL(3)

  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    #('req_msg_a      req_msg_b    presum       resp_msg*   a_shift*'),
    ('image_in[0]  image_in[1] image_in[2] image_in[3] image_in[4] image_in[5] image_in[6] image_in[7] image_in[8] image_in[9] image_in[10] image_in[11] image_in[12] image_in[13] image_in[14] image_out[0]* image_out[1]* image_out[2]* image_out[3]* image_out[4]* image_out[5]* image_out[6]* image_out[7]* image_out[8]*'),
    [b32(0),       b32(0),     b32(0),     b32(0),     b32(0),     b32(0),     b32(0),     b32(0),     b32(0),     b32(0),     b32(0),      b32(0),      b32(0),      b32(0),      b32(0),      b32(0),       b32(0),       b32(0),       b32(0),       b32(0),       b32(0),       b32(0),       b32(0),       b32(0)],
    [b32(0),       b32(7),     b32(2),     b32(3),     b32(0),     b32(0),     b32(1),     b32(-6),    b32(5),     b32(0),     b32(0),      b32(-1),     b32(-2),     b32(0),      b32(0),      b32(2),       b32(-4),      b32(-2),      b32(-6),      b32(4),       b32(6),       b32(-2),      b32(1),       b32(2)],
  ] )

def test_small_pos( dump_vcd, test_verilog ):
  #dut = IntMulVarLatCalcShamtRTL()     #need to change the name
  dut = IxVRTL(3)

  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    #('req_msg_a      req_msg_b    presum       resp_msg*   a_shift*'),
    ('image_in[0]  image_in[1] image_in[2] image_in[3] image_in[4] image_in[5] image_in[6] image_in[7] image_in[8] image_in[9] image_in[10] image_in[11] image_in[12] image_in[13] image_in[14] image_out[0]* image_out[1]* image_out[2]* image_out[3]* image_out[4]* image_out[5]* image_out[6]* image_out[7]* image_out[8]*'),
    [b32(0),       b32(2),     b32(4),     b32(6),     b32(8),     b32(10),    b32(12),    b32(14),    b32(16),    b32(18),    b32(20),     b32(22),     b32(24),     b32(26),     b32(28),     b32(4),       b32(4),       b32(4),       b32(4),       b32(4),       b32(4),       b32(4),       b32(4),       b32(4)],
    [b32(5),       b32(1),     b32(7),     b32(1),     b32(3),     b32(9),     b32(9),     b32(3),     b32(5),     b32(2),     b32(0),      b32(1),      b32(2),      b32(4),      b32(3),      b32(2),       b32(0),       b32(-4),      b32(-6),      b32(-4),      b32(-1),      b32(2),       b32(3),       b32(1)],
  ] )

def test_large_pos( dump_vcd, test_verilog ):
  dut = IxVRTL(3)

  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    #('req_msg_a      req_msg_b    presum       resp_msg*   a_shift*'),
    ('image_in[0]  image_in[1] image_in[2] image_in[3] image_in[4] image_in[5] image_in[6] image_in[7] image_in[8] image_in[9] image_in[10] image_in[11] image_in[12] image_in[13] image_in[14] image_out[0]* image_out[1]* image_out[2]* image_out[3]* image_out[4]* image_out[5]* image_out[6]* image_out[7]* image_out[8]*'),
    [b32(255),     b32(255),   b32(255),   b32(255),   b32(255),   b32(255),   b32(255),   b32(255),   b32(255),   b32(255),   b32(255),    b32(255),    b32(255),    b32(255),    b32(255),    b32(0),       b32(0),       b32(0),       b32(0),       b32(0),       b32(0),       b32(0),       b32(0),       b32(0)],
    [b32(250),     b32(248),   b32(251),   b32(255),   b32(252),   b32(243),   b32(247),   b32(251),   b32(250),   b32(255),   b32(250),    b32(243),    b32(247),    b32(249),    b32(240),    b32(1),       b32(7),       b32(1),       b32(8),       b32(3),       b32(4),       b32(-3),      b32(6),       b32(-7)],
  ] )

def test_small_neg( dump_vcd, test_verilog ):
  dut = IxVRTL(3)

  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    #('req_msg_a      req_msg_b    presum       resp_msg*   a_shift*'),
    ('image_in[0]  image_in[1] image_in[2] image_in[3] image_in[4] image_in[5] image_in[6] image_in[7] image_in[8] image_in[9] image_in[10] image_in[11] image_in[12] image_in[13] image_in[14] image_out[0]* image_out[1]* image_out[2]* image_out[3]* image_out[4]* image_out[5]* image_out[6]* image_out[7]* image_out[8]*'),
    [b32(0),       b32(-2),    b32(-4),    b32(-6),    b32(-8),    b32(-10),   b32(-12),   b32(-14),   b32(-16),   b32(-18),   b32(-20),    b32(-22),    b32(-24),    b32(-26),    b32(-28),    b32(-4),      b32(-4),      b32(-4),      b32(-4),      b32(-4),      b32(-4),      b32(-4),      b32(-4),      b32(-4)],
    [b32(-5),      b32(-1),    b32(-7),    b32(-1),    b32(-3),    b32(-9),    b32(-9),    b32(-3),    b32(-5),    b32(-2),    b32(0),      b32(-1),     b32(-2),     b32(-4),     b32(-3),     b32(-2),      b32(0),       b32(4),       b32(6),       b32(4),       b32(1),       b32(-2),      b32(-3),      b32(-1)],
  ] )

def test_large_neg( dump_vcd, test_verilog ):
  dut = IxVRTL(3)

  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    #('req_msg_a      req_msg_b    presum       resp_msg*   a_shift*'),
    ('image_in[0]  image_in[1] image_in[2] image_in[3] image_in[4] image_in[5] image_in[6] image_in[7] image_in[8] image_in[9] image_in[10] image_in[11] image_in[12] image_in[13] image_in[14] image_out[0]* image_out[1]* image_out[2]* image_out[3]* image_out[4]* image_out[5]* image_out[6]* image_out[7]* image_out[8]*'),
    [b32(-255),    b32(-255),  b32(-255),  b32(-255),  b32(-255),  b32(-255),  b32(-255),  b32(-255),  b32(-255),  b32(-255),  b32(-255),   b32(-255),   b32(-255),   b32(-255),   b32(-255),   b32(0),       b32(0),       b32(0),       b32(0),       b32(0),       b32(0),       b32(0),       b32(0),       b32(0)],
    [b32(-250),    b32(-248),  b32(-251),  b32(-255),  b32(-252),  b32(-243),  b32(-247),  b32(-251),  b32(-250),  b32(-255),  b32(-250),   b32(-243),   b32(-247),   b32(-249),   b32(-240),   b32(-1),      b32(-7),      b32(-1),      b32(-8),      b32(-3),      b32(-4),      b32(3),       b32(-6),      b32(7)],
  ] )


def test_random( dump_vcd, test_verilog ):
  nvectors = 100                      #numer of the random vectors
  side     = 3
  bits_type = mk_bits(32)

  hd_str  = ' '.join( [ f"image_in[{i}]" for i in range(side*(side+2)) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"image_out[{i}]*" for i in range(side*side) ] )

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    for j in range(side*(side+2)):
      vector.append( bits_type( random.randint(0, 1024) ) )
    # Add output data
    for k in range(0,side):
      for l in range(0,side):
        vector.append(vector[l+k*(side+2)+2]-vector[l+(side+2)*k])


    tvectors.append( vector )

  run_test_vector_sim( IxVRTL(3), tvectors, dump_vcd, test_verilog )

