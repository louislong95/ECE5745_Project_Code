#=========================================================================
# step test
#=========================================================================

from pymtl3             import *
from pymtl3.passes.backends.verilog import \
    VerilatorImportConfigs, TranslationConfigs
from pymtl3.stdlib.test import run_test_vector_sim, config_model
#need to change the name of the module
#from lab1_imul.IntMulVarLatCalcShamtRTL import IntMulVarLatCalcShamtRTL
from submodule.IyRTL import IyVRTL
import random
#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------

def test_basic( dump_vcd, test_verilog ):
  #dut = IntMulVarLatCalcShamtRTL()     #need to change the name
  dut = IyVRTL(3)

  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    #('req_msg_a      req_msg_b    presum       resp_msg*   a_shift*'),
    ('image_in[0]  image_in[1] image_in[2] image_in[3] image_in[4] image_in[5] image_in[6] image_in[7] image_in[8] image_in[9] image_in[10] image_in[11] image_in[12] image_in[13] image_in[14]   image_in[15]   image_in[16]   image_in[17]   image_in[18]   image_in[19]   image_in[20]   image_in[21]   image_in[22]    image_in[23]   image_in[24]   image_out[0]* image_out[1]* image_out[2]* image_out[3]* image_out[4]* image_out[5]* image_out[6]* image_out[7]* image_out[8]*'),
    [b32(0),       b32(1),     b32(2),     b32(3),     b32(4),     b32(5),     b32(6),     b32(7),     b32(8),     b32(9),     b32(10),     b32(11),     b32(12),     b32(13),     b32(14),       b32(15),       b32(16),       b32(17),       b32(18),       b32(19),       b32(20),       b32(21),       b32(22),        b32(23),       b32(24),       b32(10),      b32(10),      b32(10),      b32(10),      b32(10),      b32(10),      b32(10),      b32(10),      b32(10)],
    #[b32(0),       b32(1),     b32(7),     b32(3),     b32(0),     b32(5),     b32(6),     b32(7),     b32(8),     b32(8),     b32(4),      b32(2),      b32(9),      b32(6),      b32(3),                                    b32(6),       b32(6),       b32(1),       b32(5),       b32(4),       b32(-3),      b32(3),       b32(-1),       b32(-5)],
  ] )

def test_random( dump_vcd, test_verilog ):
  nvectors  = 10                      #numer of the random vectors
  side      = 3
  bits_type = mk_bits(32)
  width     = side+2

  hd_str  = ' '.join( [ f"image_in[{i}]" for i in range((side+2)*(side+2)) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"image_out[{i}]*" for i in range(side*side) ] )

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    for j in range((side+2)*(side+2)):
      vector.append( bits_type( random.randint(0, 1024) ) )
    # Add output data
    for k in range(0,side):
      for l in range(0,side):
        vector.append(vector[(k+2)*width+l+1] -vector[k*width+l+1] )


    tvectors.append( vector )

  run_test_vector_sim( IyVRTL(3), tvectors, dump_vcd, test_verilog )

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