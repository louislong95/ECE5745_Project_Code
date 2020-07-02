rtl_language = 'verilog'

#-------------------------------------------------------------------------
# Do not edit below this line
#-------------------------------------------------------------------------

# This is the PyMTL wrapper for the corresponding Verilog RTL model.

from pymtl3 import *
from pymtl3.passes.backends.verilog import \
    VerilogPlaceholderConfigs, VerilatorImportConfigs, TranslationConfigs

class matrix_operaVRTL( Placeholder, Component ):

    # Constructor

  def construct( s ):

    # Interface
    s.req_go = InPort(mk_bits(1))
    s.in_x =[InPort(mk_bits(32))for _ in range(9)]
    s.in_y =[InPort(mk_bits(32))for _ in range(9)]
    s.in_t =[InPort(mk_bits(32))for _ in range(9)]
    s.vx  =OutPort(mk_bits(32))
    s.vy  =OutPort(mk_bits(32))
    s.de  =OutPort(mk_bits(32))
    s.result_ok  =OutPort(mk_bits(32))
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
        src_file = path.dirname(__file__) + '/matrix_operaVRTL.v',
        #src_file = path.dirname(__file__) + '/IntMulVarLatCalcShamtVRTL.v',
        # Name of the Verilog top level module
        top_module = 'matrix_operaVRTL',
        #top_module = 'lab1_imul_IntMulVarLatCalcShamtVRTL',
        # Step unit does not have clk and reset pins
        params={

        },
        has_clk   = True,
        has_reset = True,
        )
        #edit here
    s.config_verilog_translate = TranslationConfigs(
            # You can leave this option unset if your rtl_language is Verilog
            translate = False,
            # Use the xRTL module name instead of xVRTL
            explicit_module_name = f'matrix_opera',
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
    _cls = matrix_operaVRTL
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
