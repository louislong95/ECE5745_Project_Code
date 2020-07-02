rtl_language = 'verilog'

#-------------------------------------------------------------------------
# Do not edit below this line
#-------------------------------------------------------------------------

# This is the PyMTL wrapper for the corresponding Verilog RTL model.

from pymtl3 import *
from pymtl3.passes.backends.verilog import \
    VerilogPlaceholderConfigs, VerilatorImportConfigs, TranslationConfigs

class ItVRTL( Placeholder, Component ):

  # Constructor

  def construct( s ,side):

    # Interface
    s.current_frame =[InPort(mk_bits(32))for _ in range((side+2)*(side+2))]
    s.next_frame    =[InPort(mk_bits(32))for _ in range((side+2)*(side+2))]
    s.out           =[OutPort(mk_bits(32))for _ in range(side*side)]
    #s.req_msg_a=InPort(Bits32)
    #s.req_msg_b=InPort(Bits1)
    #s.presum   =InPort(Bits32)
    #s.resp_msg =OutPort(Bits32)
    #s.a_shift  =OutPort(Bits32) 
    
  
    #s.in_ = InPort  (Bits8)
    #s.out = OutPort (Bits4)

    # Configurations

    from os import path
    s.config_placeholder = VerilogPlaceholderConfigs(
      # Path to the Verilog source file
      src_file = path.dirname(__file__) + '/ItVRTL.v',
      #src_file = path.dirname(__file__) + '/IntMulVarLatCalcShamtVRTL.v',
      # Name of the Verilog top level module
      top_module = 'ItVRTL',
      #top_module = 'lab1_imul_IntMulVarLatCalcShamtVRTL',
      # Step unit does not have clk and reset pins
      params={
       'side':side,
      },
      has_clk   = False,
      has_reset = False,
    )
    #edit here
    s.config_verilog_translate = TranslationConfigs(
        # You can leave this option unset if your rtl_language is Verilog
        translate = False,
        # Use the xRTL module name instead of xVRTL
        explicit_module_name = f'It',
    )

# See if the course staff want to force testing a specific RTL language
# for their own testing.

import sys
if hasattr( sys, '_called_from_test' ):
  if sys._pymtl_rtl_override:
    rtl_language = sys._pymtl_rtl_override

# Import the appropriate version based on the rtl_language variable

if rtl_language == 'pymtl':
  from .IntMulVarLatCalcShamtPRTL import IntMulVarLatCalcShamtPRTL as _cls
elif rtl_language == 'verilog':
  #_cls = IntMulVarLatCalcShamtVRTL
  _cls = ItVRTL
else:
  raise Exception("Invalid RTL language!")

#class Ix( _cls ):
#  def construct( s,size ):
#    super().construct()
#    # The translated Verilog must be xRTL.v instead of xPRTL.v
#    s.config_verilog_translate = TranslationConfigs(
#      translate=False,
      #explicit_module_name = f'lab1_imul_IntMulVarLatCalcShamtRTL',
#      explicit_module_name = f'Ix',
#   )