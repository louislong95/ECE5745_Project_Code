#=========================================================================
# step test
#=========================================================================

from pymtl3             import *
from pymtl3.passes.backends.verilog import \
    VerilatorImportConfigs, TranslationConfigs
from pymtl3.stdlib.test import run_test_vector_sim, config_model
#need to change the name of the module
#from lab1_imul.IntMulVarLatCalcShamtRTL import IntMulVarLatCalcShamtRTL
from submodule.ItRTL import ItVRTL
import random
#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------

def test_basic( dump_vcd, test_verilog ):
  #dut = IntMulVarLatCalcShamtRTL()     #need to change the name
  dut = ItVRTL(3)

  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    #('req_msg_a      req_msg_b    presum       resp_msg*   a_shift*'),
    ('current_frame[0]  current_frame[1] current_frame[2] current_frame[3] current_frame[4] current_frame[5] current_frame[6] current_frame[7] current_frame[8] current_frame[9] current_frame[10] current_frame[11] current_frame[12] current_frame[13] current_frame[14] current_frame[15] current_frame[16] current_frame[17] current_frame[18] current_frame[19] current_frame[20] current_frame[21] current_frame[22] current_frame[23] current_frame[24] next_frame[0] next_frame[1] next_frame[2] next_frame[3] next_frame[4] next_frame[5] next_frame[6] next_frame[7] next_frame[8] next_frame[9] next_frame[10] next_frame[11] next_frame[12] next_frame[13] next_frame[14] next_frame[15] next_frame[16] next_frame[17] next_frame[18] next_frame[19] next_frame[20] next_frame[21] next_frame[22] next_frame[23] next_frame[24] out[0]*   out[1]*   out[2]*   out[3]*   out[4]*   out[5]*   out[6]*   out[7]*   out[8]*'),
    [b32(0),            b32(1),          b32(2),          b32(3),          b32(4),          b32(5),          b32(6),          b32(7),          b32(8),          b32(9),          b32(10),          b32(11),          b32(12),          b32(13),          b32(14),          b32(15),          b32(16),          b32(17),          b32(18),          b32(19),          b32(20),          b32(21),          b32(22),          b32(23),          b32(24),          b32(24),      b32(23),      b32(22),      b32(21),      b32(20),      b32(19),      b32(18),      b32(17),      b32(16),      b32(15),      b32(14),       b32(13),       b32(12),       b32(11),       b32(10),       b32(9),        b32(8),        b32(7),        b32(6),        b32(5),        b32(4),        b32(3),        b32(2),        b32(1),        b32(0),        b32(12),  b32(10),  b32(8),   b32(2),  b32(0),   b32(-2),   b32(-8),  b32(-10), b32(-12),        ],
    #[b32(0),            b32(1),          b32(7),          b32(3),          b32(0),          b32(5),          b32(6),          b32(7),          b32(8),          b32(4),       b32(-1),      b32(5),       b32(7),        b32(0),      b32(2),       b32(1),       b32(-1),      b32(2),       b32(4),   b32(-2),  b32(-2),  b32(4),   b32(0),   b32(-3),  b32(-5),  b32(-8),  b32(-6),  ],  
  ] )

def test_random( dump_vcd, test_verilog ):
  nvectors = 100                     #numer of the random vectors
  side     = 3
  bits_type = mk_bits(32)
  width    = side+2

  hd_str  = ' '.join( [ f"current_frame[{i}]" for i in range((side+2)*(side+2)) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"next_frame[{i}]" for i in range((side+2)*(side+2)) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"out[{i}]*" for i in range(side*side) ] )

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    for j in range( (side+2)* (side+2)):
      vector.append( bits_type( random.randint(0, 1024) ) )
    for k in range( (side+2)* (side+2)):
      vector.append( bits_type( random.randint(0, 1024) ) )
    # Add output data
    for l in range(0,side):
      for m in range(0,side):
       #vector.append(vector[l]-vector[l+size*size])
        vector.append(vector[width*width+(l+1)*width+m+1]-vector[(l+1)*width+m+1])


    tvectors.append( vector )

  run_test_vector_sim( ItVRTL(3), tvectors, dump_vcd, test_verilog )

#def test_large_pos( dump_vcd, test_verilog ):
#  #dut = IntMulVarLatCalcShamtRTL()      #need to change the name 
#  dut = step()

#  config_model( dut, dump_vcd, test_verilog )

# run_test_vector_sim( dut, [
#    ('req_msg_a      req_msg_b    presum       resp_msg*   a_shift*'),
   # [ 0x7fff0000,      0,         0x00000000,  0x00000000,  0xfffe0000     ],
   # [ 0x7fff0001,      0,         0x00000011,  0x00000011,  0xfffe0002     ],
   # [ 0x7fff0000,      1,         0x00001000,  0x7fff1000,  0xfffe0000     ],
   # [ 0x4dff1000,      1,         0x00001100,  0x4dff2100,  0x9bfe2000     ],
#  ] )
#def Ixcal(image_in,image_out,size):
#  for i in range (0,size):
#    for j in range(0,size):
#      image_out.append(image_in[j+i*(size+2)+2]-image_in[j+(size+2)*i])
#  return

#image_in=[0,1,7,3,0,5,6,7,8,8,4,2,9,6,3]
#image_out=[]
#Ixcal(image_in,image_out,3)
#for i in image_out:
#  print(i)