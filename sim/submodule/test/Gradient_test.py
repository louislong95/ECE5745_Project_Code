#=========================================================================
#test
#=========================================================================

from pymtl3             import *
from pymtl3.passes.backends.verilog import \
    VerilatorImportConfigs, TranslationConfigs
from pymtl3.stdlib.test import run_test_vector_sim, config_model
#need to change the name of the module
#from lab1_imul.IntMulVarLatCalcShamtRTL import IntMulVarLatCalcShamtRTL
from submodule.GradientRTL import GradientVRTL
import random
#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------
INTMAX = 2147483647
INTMIN = -2147483648
def test_basic( dump_vcd, test_verilog ):
  nvectors = 1                     #numer of the random vectors
  side     = 3
  bits_type = mk_bits(32)
  width   =side+2

  hd_str  = ' '.join( [ f"en"])
  hd_str += ' '
  hd_str += ' '.join( [ f"current_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"next_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Ix[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Iy[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"It[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [f"valid*"])

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    vector.append(1)                        #en=1
    for j in range(width*width):
      vector.append( bits_type(j) )        #generate current frame
    for j in range(width*width):
      vector.append( bits_type(j))         #generate next frame
    # Add output data
    for k in range(0,side*side):           #check Ix results
      vector.append(2)
    for k in range(0,side*side):           #check Iy results
      vector.append(10)
    for k in range(0,side*side):
      vector.append(0)
    vector.append(1)                       #valid=1
  tvectors.append( vector )

  run_test_vector_sim( GradientVRTL(3), tvectors, dump_vcd, test_verilog )

def test_small_pos( dump_vcd, test_verilog ):
  nvectors   = 1                     #numer of the random vectors
  side       = 3
  bits_type  = mk_bits(32)
  width      = side+2

  hd_str  = ' '.join( [ f"en"])
  hd_str += ' '
  hd_str += ' '.join( [ f"current_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"next_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Ix[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Iy[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"It[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [f"valid*"])

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    vector.append(1)                        #en=1
    for j in range(width*width):
      vector.append( 5*j+1 )                #generate current frame
    for j in range(width*width):
      vector.append( 3*j-1)                 #generate next frame
    # Add output data
    for k in range(0,side):                 #check Ix results
      for l in range(0,side):
        vector.append (vector[width*(k+1)+l+3] - vector[width*(k+1)+l+1])
    for k in range(0,side):                 #check Iy results
      for l in range(0,side):
        vector.append(vector[(k+2)*width+l+1+1] -vector[k*width+l+1+1] )
    for k in range(0,side):
      for l in range(0,side):
        vector.append(vector[width*width+(k+1)*width+l+1+1]-vector[(k+1)*width+l+1+1])
    vector.append(1)                        #valid=1
  tvectors.append( vector )

  run_test_vector_sim( GradientVRTL(3), tvectors, dump_vcd, test_verilog )

def test_small_neg( dump_vcd, test_verilog ):
  nvectors   = 1                     #numer of the random vectors
  side       = 3
  bits_type  = mk_bits(32)
  width      = side+2

  hd_str  = ' '.join( [ f"en"])
  hd_str += ' '
  hd_str += ' '.join( [ f"current_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"next_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Ix[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Iy[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"It[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [f"valid*"])

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    vector.append(1)                        #en=1
    for j in range(width*width):
      vector.append( -5*j-1 )                #generate current frame
    for j in range(width*width):
      vector.append( -3*j-1)                 #generate next frame
    # Add output data
    for k in range(0,side):                 #check Ix results
      for l in range(0,side):
        vector.append (vector[width*(k+1)+l+3] - vector[width*(k+1)+l+1])
    for k in range(0,side):                 #check Iy results
      for l in range(0,side):
        vector.append(vector[(k+2)*width+l+1+1] -vector[k*width+l+1+1] )
    for k in range(0,side):
      for l in range(0,side):
        vector.append(vector[width*width+(k+1)*width+l+1+1]-vector[(k+1)*width+l+1+1])
    vector.append(1)                        #valid=1
  tvectors.append( vector )

  run_test_vector_sim( GradientVRTL(3), tvectors, dump_vcd, test_verilog )

def test_large_pos( dump_vcd, test_verilog ):
  nvectors   = 1                     #numer of the random vectors
  side       = 3
  bits_type  = mk_bits(32)
  width      = side+2

  hd_str  = ' '.join( [ f"en"])
  hd_str += ' '
  hd_str += ' '.join( [ f"current_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"next_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Ix[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Iy[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"It[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [f"valid*"])

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    vector.append(1)                        #en=1
    for j in range(width*width):
      vector.append( INTMAX-5*j )                #generate current frame
    for j in range(width*width):
      vector.append( INTMAX-3*j+6)               #generate next frame
    # Add output data
    for k in range(0,side):                 #check Ix results
      for l in range(0,side):
        vector.append (vector[width*(k+1)+l+3] - vector[width*(k+1)+l+1])
    for k in range(0,side):                 #check Iy results
      for l in range(0,side):
        vector.append(vector[(k+2)*width+l+1+1] -vector[k*width+l+1+1] )
    for k in range(0,side):
      for l in range(0,side):
        vector.append(vector[width*width+(k+1)*width+l+1+1]-vector[(k+1)*width+l+1+1])
    vector.append(1)                        #valid=1
  tvectors.append( vector )

  run_test_vector_sim( GradientVRTL(3), tvectors, dump_vcd, test_verilog )

def test_large_neg( dump_vcd, test_verilog ):
  nvectors   = 1                     #numer of the random vectors
  side       = 3
  bits_type  = mk_bits(32)
  width      = side+2

  hd_str  = ' '.join( [ f"en"])
  hd_str += ' '
  hd_str += ' '.join( [ f"current_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"next_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Ix[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Iy[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"It[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [f"valid*"])

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    vector.append(1)                        #en=1
    for j in range(width*width):
      vector.append( INTMIN+5*j )                #generate current frame
    for j in range(width*width):
      vector.append( INTMIN+3*j+6)               #generate next frame
    # Add output data
    for k in range(0,side):                 #check Ix results
      for l in range(0,side):
        vector.append (vector[width*(k+1)+l+3] - vector[width*(k+1)+l+1])
    for k in range(0,side):                 #check Iy results
      for l in range(0,side):
        vector.append(vector[(k+2)*width+l+1+1] -vector[k*width+l+1+1] )
    for k in range(0,side):
      for l in range(0,side):
        vector.append(vector[width*width+(k+1)*width+l+1+1]-vector[(k+1)*width+l+1+1])
    vector.append(1)                        #valid=1
  tvectors.append( vector )

  run_test_vector_sim( GradientVRTL(3), tvectors, dump_vcd, test_verilog )

def test_neg_pos_small( dump_vcd, test_verilog ):
  nvectors   = 1                     #numer of the random vectors
  side       = 3
  bits_type  = mk_bits(32)
  width      = side+2

  hd_str  = ' '.join( [ f"en"])
  hd_str += ' '
  hd_str += ' '.join( [ f"current_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"next_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Ix[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Iy[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"It[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [f"valid*"])

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    vector.append(1)                        #en=1
    for j in range(width*width):
      vector.append( 5*j )                #generate current frame
    for j in range(width*width):
      vector.append( -3*j+6)               #generate next frame
    # Add output data
    for k in range(0,side):                 #check Ix results
      for l in range(0,side):
        vector.append (vector[width*(k+1)+l+3] - vector[width*(k+1)+l+1])
    for k in range(0,side):                 #check Iy results
      for l in range(0,side):
        vector.append(vector[(k+2)*width+l+1+1] -vector[k*width+l+1+1] )
    for k in range(0,side):
      for l in range(0,side):
        vector.append(vector[width*width+(k+1)*width+l+1+1]-vector[(k+1)*width+l+1+1])
    vector.append(1)                        #valid=1
  tvectors.append( vector )

  run_test_vector_sim( GradientVRTL(3), tvectors, dump_vcd, test_verilog )

def test_neg_pos_large( dump_vcd, test_verilog ):
  nvectors   = 1                     #numer of the random vectors
  side       = 3
  bits_type  = mk_bits(32)
  width      = side+2

  hd_str  = ' '.join( [ f"en"])
  hd_str += ' '
  hd_str += ' '.join( [ f"current_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"next_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Ix[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Iy[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"It[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [f"valid*"])

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    vector.append(1)                        #en=1
    for j in range(width*width):
      vector.append( INTMAX-5*j )                #generate current frame
    for j in range(width*width):
      vector.append( INTMIN-3*j+6)               #generate next frame
    # Add output data
    for k in range(0,side):                 #check Ix results
      for l in range(0,side):
        vector.append (vector[width*(k+1)+l+3] - vector[width*(k+1)+l+1])
    for k in range(0,side):                 #check Iy results
      for l in range(0,side):
        vector.append(vector[(k+2)*width+l+1+1] -vector[k*width+l+1+1] )
    for k in range(0,side):
      for l in range(0,side):
        vector.append(vector[width*width+(k+1)*width+l+1+1]-vector[(k+1)*width+l+1+1])
    vector.append(1)                        #valid=1
  tvectors.append( vector )

  run_test_vector_sim( GradientVRTL(3), tvectors, dump_vcd, test_verilog )



def test_random_basic( dump_vcd, test_verilog ):
  nvectors = 100                     #numer of the random vectors
  side     = 3
  bits_type = mk_bits(32)
  width   =side+2

  hd_str  = ' '.join( [ f"en"])
  hd_str += ' '
  hd_str += ' '.join( [ f"current_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"next_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Ix[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Iy[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"It[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [f"valid*"])

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    vector.append(1)                        #en=1
    for j in range(width*width):
      vector.append( bits_type(random.randint(0, 100)) )        #generate current frame
    for j in range(width*width):
      vector.append( bits_type(random.randint(0, 100)))         #generate next frame
    # Add output data
    for k in range(0,side):                #check Ix results
      for l in range(0,side):
        vector.append (vector[width*(k+1)+l+3] - vector[width*(k+1)+l+1])
    for k in range(0,side):                #check Iy results
      for l in range(0,side):
        vector.append(vector[(k+2)*width+l+1+1] -vector[k*width+l+1+1] )
    for k in range(0,side):
      for l in range(0,side):
        vector.append(vector[width*width+(k+1)*width+l+1+1]-vector[(k+1)*width+l+1+1])

    vector.append(1)                       #valid=1


  tvectors.append( vector )

  run_test_vector_sim( GradientVRTL(3), tvectors, dump_vcd, test_verilog )

def test_random_small_pos( dump_vcd, test_verilog ):
  nvectors = 100                     #numer of the random vectors
  side     = 3
  bits_type = mk_bits(32)
  width   =side+2

  hd_str  = ' '.join( [ f"en"])
  hd_str += ' '
  hd_str += ' '.join( [ f"current_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"next_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Ix[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Iy[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"It[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [f"valid*"])

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    vector.append(1)                        #en=1
    for j in range(width*width):
      vector.append( bits_type(random.randint(0, 255)) )        #generate current frame
    for j in range(width*width):
      vector.append( bits_type(random.randint(0, 255)))         #generate next frame
    # Add output data
    for k in range(0,side):                #check Ix results
      for l in range(0,side):
        vector.append (vector[width*(k+1)+l+3] - vector[width*(k+1)+l+1])
    for k in range(0,side):                #check Iy results
      for l in range(0,side):
        vector.append(vector[(k+2)*width+l+1+1] -vector[k*width+l+1+1] )
    for k in range(0,side):
      for l in range(0,side):
        vector.append(vector[width*width+(k+1)*width+l+1+1]-vector[(k+1)*width+l+1+1])

    vector.append(1)                       #valid=1


  tvectors.append( vector )

  run_test_vector_sim( GradientVRTL(3), tvectors, dump_vcd, test_verilog )

def test_random_small_neg( dump_vcd, test_verilog ):
  nvectors = 100                     #numer of the random vectors
  side     = 3
  bits_type = mk_bits(32)
  width   =side+2

  hd_str  = ' '.join( [ f"en"])
  hd_str += ' '
  hd_str += ' '.join( [ f"current_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"next_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Ix[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Iy[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"It[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [f"valid*"])

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    vector.append(1)                        #en=1
    for j in range(width*width):
      vector.append( bits_type(random.randint(-255, 0)) )        #generate current frame
    for j in range(width*width):
      vector.append( bits_type(random.randint(-255, 0)))         #generate next frame
    # Add output data
    for k in range(0,side):                #check Ix results
      for l in range(0,side):
        vector.append (vector[width*(k+1)+l+3] - vector[width*(k+1)+l+1])
    for k in range(0,side):                #check Iy results
      for l in range(0,side):
        vector.append(vector[(k+2)*width+l+1+1] -vector[k*width+l+1+1] )
    for k in range(0,side):
      for l in range(0,side):
        vector.append(vector[width*width+(k+1)*width+l+1+1]-vector[(k+1)*width+l+1+1])

    vector.append(1)                       #valid=1


  tvectors.append( vector )

  run_test_vector_sim( GradientVRTL(3), tvectors, dump_vcd, test_verilog )

def test_random_large_pos( dump_vcd, test_verilog ):
  nvectors = 100                     #numer of the random vectors
  side     = 3
  bits_type = mk_bits(32)
  width   =side+2

  hd_str  = ' '.join( [ f"en"])
  hd_str += ' '
  hd_str += ' '.join( [ f"current_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"next_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Ix[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Iy[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"It[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [f"valid*"])

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    vector.append(1)                        #en=1
    for j in range(width*width):
      vector.append( bits_type(random.randint(INTMAX-255, INTMAX)) )        #generate current frame
    for j in range(width*width):
      vector.append( bits_type(random.randint(INTMAX-255, INTMAX)))         #generate next frame
    # Add output data
    for k in range(0,side):                #check Ix results
      for l in range(0,side):
        vector.append (vector[width*(k+1)+l+3] - vector[width*(k+1)+l+1])
    for k in range(0,side):                #check Iy results
      for l in range(0,side):
        vector.append(vector[(k+2)*width+l+1+1] -vector[k*width+l+1+1] )
    for k in range(0,side):
      for l in range(0,side):
        vector.append(vector[width*width+(k+1)*width+l+1+1]-vector[(k+1)*width+l+1+1])

    vector.append(1)                       #valid=1


  tvectors.append( vector )

  run_test_vector_sim( GradientVRTL(3), tvectors, dump_vcd, test_verilog )

def test_random_large_neg( dump_vcd, test_verilog ):
  nvectors = 100                     #numer of the random vectors
  side     = 3
  bits_type = mk_bits(32)
  width   =side+2

  hd_str  = ' '.join( [ f"en"])
  hd_str += ' '
  hd_str += ' '.join( [ f"current_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"next_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Ix[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Iy[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"It[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [f"valid*"])

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    vector.append(1)                        #en=1
    for j in range(width*width):
      vector.append( bits_type(random.randint(INTMIN, INTMIN+255)) )        #generate current frame
    for j in range(width*width):
      vector.append( bits_type(random.randint(INTMIN, INTMIN+255)))         #generate next frame
    # Add output data
    for k in range(0,side):                #check Ix results
      for l in range(0,side):
        vector.append (vector[width*(k+1)+l+3] - vector[width*(k+1)+l+1])
    for k in range(0,side):                #check Iy results
      for l in range(0,side):
        vector.append(vector[(k+2)*width+l+1+1] -vector[k*width+l+1+1] )
    for k in range(0,side):
      for l in range(0,side):
        vector.append(vector[width*width+(k+1)*width+l+1+1]-vector[(k+1)*width+l+1+1])

    vector.append(1)                       #valid=1


  tvectors.append( vector )

  run_test_vector_sim( GradientVRTL(3), tvectors, dump_vcd, test_verilog )

def test_random_neg_pos_small( dump_vcd, test_verilog ):
  nvectors = 100                     #numer of the random vectors
  side     = 3
  bits_type = mk_bits(32)
  width   =side+2

  hd_str  = ' '.join( [ f"en"])
  hd_str += ' '
  hd_str += ' '.join( [ f"current_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"next_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Ix[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Iy[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"It[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [f"valid*"])

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    vector.append(1)                        #en=1
    for j in range(width*width):
      vector.append( bits_type(random.randint(0, 255)) )        #generate current frame
    for j in range(width*width):
      vector.append( bits_type(random.randint(-255, 0)))         #generate next frame
    # Add output data
    for k in range(0,side):                #check Ix results
      for l in range(0,side):
        vector.append (vector[width*(k+1)+l+3] - vector[width*(k+1)+l+1])
    for k in range(0,side):                #check Iy results
      for l in range(0,side):
        vector.append(vector[(k+2)*width+l+1+1] -vector[k*width+l+1+1] )
    for k in range(0,side):
      for l in range(0,side):
        vector.append(vector[width*width+(k+1)*width+l+1+1]-vector[(k+1)*width+l+1+1])

    vector.append(1)                       #valid=1


  tvectors.append( vector )

  run_test_vector_sim( GradientVRTL(3), tvectors, dump_vcd, test_verilog )

def test_random_neg_pos_large( dump_vcd, test_verilog ):
  nvectors = 100                     #numer of the random vectors
  side     = 3
  bits_type = mk_bits(32)
  width   =side+2

  hd_str  = ' '.join( [ f"en"])
  hd_str += ' '
  hd_str += ' '.join( [ f"current_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"next_frame[{i}]" for i in range(width*width) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Ix[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"Iy[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [ f"It[{i}]*" for i in range(side*side) ] )
  hd_str += ' '
  hd_str += ' '.join( [f"valid*"])

  # Generate test vectors
  tvectors = [ hd_str ]
  for i in range(nvectors):
    vector = []
    # Add input data
    vector.append(1)                        #en=1
    for j in range(width*width):
      vector.append( bits_type(random.randint(INTMAX-255, INTMAX)) )        #generate current frame
    for j in range(width*width):
      vector.append( bits_type(random.randint(INTMIN, INTMIN+255)))         #generate next frame
    # Add output data
    for k in range(0,side):                #check Ix results
      for l in range(0,side):
        vector.append (vector[width*(k+1)+l+3] - vector[width*(k+1)+l+1])
    for k in range(0,side):                #check Iy results
      for l in range(0,side):
        vector.append(vector[(k+2)*width+l+1+1] -vector[k*width+l+1+1] )
    for k in range(0,side):
      for l in range(0,side):
        vector.append(vector[width*width+(k+1)*width+l+1+1]-vector[(k+1)*width+l+1+1])

    vector.append(1)                       #valid=1


  tvectors.append( vector )

  run_test_vector_sim( GradientVRTL(3), tvectors, dump_vcd, test_verilog )