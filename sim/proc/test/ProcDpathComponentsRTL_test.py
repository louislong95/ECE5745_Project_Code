#=========================================================================
# ProcDpathComponentsRTL_test.py
#=========================================================================

from pymtl3     import *
from pymtl3.stdlib.test import run_test_vector_sim, config_model

from proc.ProcDpathComponentsRTL import ImmGenRTL
from proc.ProcDpathComponentsRTL import AluRTL

#-------------------------------------------------------------------------
# ImmGenRTL
#-------------------------------------------------------------------------

def test_immgen( dump_vcd, test_verilog ):
  dut = ImmGenRTL()

  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    ('imm_type inst                                imm*'),
    [ 0,       0b11111111111100000000000000000000, 0b11111111111111111111111111111111], # I-imm
    [ 0,       0b00000000000011111111111111111111, 0b00000000000000000000000000000000], # I-imm
    [ 0,       0b01111111111100000000000000000000, 0b00000000000000000000011111111111], # I-imm
    [ 0,       0b11111111111000000000000000000000, 0b11111111111111111111111111111110], # I-imm
    [ 1,       0b11111110000000000000111110000000, 0b11111111111111111111111111111111], # S-imm
    [ 1,       0b00000001111111111111000001111111, 0b00000000000000000000000000000000], # S-imm
    [ 1,       0b01111110000000000000111110000000, 0b00000000000000000000011111111111], # S-imm
    [ 1,       0b11111110000000000000111100000000, 0b11111111111111111111111111111110], # S-imm
    [ 2,       0b11111110000000000000111110000000, 0b11111111111111111111111111111110], # B-imm
    [ 2,       0b00000001111111111111000001111111, 0b00000000000000000000000000000000], # B-imm
    [ 2,       0b11000000000000000000111100000000, 0b11111111111111111111010000011110], # B-imm
    [ 3,       0b11111111111111111111000000000000, 0b11111111111111111111000000000000], # U-imm
    [ 3,       0b00000000000000000000111111111111, 0b00000000000000000000000000000000], # U-imm
    [ 4,       0b11111111111111111111000000000000, 0b11111111111111111111111111111110], # J-imm
    [ 4,       0b00000000000000000001111111111111, 0b00000000000000000001000000000000], # J-imm
    [ 4,       0b01000000000010011001000000000000, 0b00000000000010011001010000000000], # J-imm
  ] )

#-------------------------------------------------------------------------
# AluRTL
#-------------------------------------------------------------------------

def test_alu_add( dump_vcd, test_verilog ):
  dut = AluRTL()
  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   0,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,   0,  0x0ffbc964,   '?',      '?',       '?'      ],
    #pos-neg
    [ 0x00132050,   0xd6620040,   0,  0xd6752090,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,   0,  0xfff0e890,   '?',      '?',       '?'      ],
    # neg-neg
    [ 0xfeeeeaa3,   0xf4650000,   0,  0xf353eaa3,   '?',      '?',       '?'      ],
  ] )

def test_alu_sub( dump_vcd, test_verilog ):
  dut = AluRTL()
  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   1,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,   1,  0x0ff9835c,   '?',      '?',       '?'      ],
    # pos-neg
    [ 0x00132050,   0xd6620040,   1,  0x29b12010,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,   1,  0xfff05ff0,   '?',      '?',       '?'      ],
    # neg-neg
    [ 0xfeeeeaa3,   0xf4650000,   1,  0x0a89eaa3,   '?',      '?',       '?'      ],
  ] )

def test_alu_sll( dump_vcd, test_verilog ):
  dut = AluRTL()
  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   2,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x05050505,   0x00000001,   2,  0x0a0a0a0a,   '?',      '?',       '?'      ],
    [ 0x05050505,   0x00000002,   2,  0x14141414,   '?',      '?',       '?'      ],
    [ 0x05050505,   0x00000004,   2,  0x50505050,   '?',      '?',       '?'      ],
    [ 0x50505050,   0x00000008,   2,  0x50505000,   '?',      '?',       '?'      ],
    [ 0x50505050,   0x0000000f,   2,  0x28280000,   '?',      '?',       '?'      ],
    [ 0x50505050,   0x00000010,   2,  0x50500000,   '?',      '?',       '?'      ],
    [ 0x50505050,   0x0000001f,   2,  0x00000000,   '?',      '?',       '?'      ],
  ] )

def test_alu_or( dump_vcd, test_verilog ):
  dut = AluRTL()
  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   3,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,   3,  0x0ffba764,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,   3,  0xd6732050,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,   3,  0xfff0e450,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,   3,  0xfeefeaa3,   '?',      '?',       '?'      ],
  ] )

def test_alu_slt( dump_vcd, test_verilog ):
  dut = AluRTL()
  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   4,  0x00000000,   '?',       0,       '?'      ],
    [ 0x0ffaa660,   0x00012304,   4,  0x00000000,   '?',       0,       '?'      ],
    [ 0x00132050,   0xd6620040,   4,  0x00000000,   '?',       0,       '?'      ],
    [ 0xfff0a440,   0x00004450,   4,  0x00000001,   '?',       1,       '?'      ],
    [ 0xffffffff,   0xf4650000,   4,  0x00000000,   '?',       0,       '?'      ],
    [ 0xfeeeeaa3,   0xffffffff,   4,  0x00000001,   '?',       1,       '?'      ],
    [ 0x80000000,   0x7fffffff,   4,  0x00000001,   '?',       1,       '?'      ],
    [ 0x7fffffff,   0x80000000,   4,  0x00000000,   '?',       0,       '?'      ],
  ] )

def test_alu_sltu( dump_vcd, test_verilog ):
  dut = AluRTL()
  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   5,  0x00000000,   '?',      '?',       0       ],
    [ 0x0ffaa660,   0x00012304,   5,  0x00000000,   '?',      '?',       0       ],
    [ 0x00132050,   0xd6620040,   5,  0x00000001,   '?',      '?',       1       ],
    [ 0xfff0a440,   0x00004450,   5,  0x00000000,   '?',      '?',       0       ],
    [ 0xffffffff,   0xf4650000,   5,  0x00000000,   '?',      '?',       0       ],
    [ 0xfeeeeaa3,   0xffffffff,   5,  0x00000001,   '?',      '?',       1       ],
  ] )

def test_alu_and( dump_vcd, test_verilog ):
  dut = AluRTL()
  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   6,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,   6,  0x00002200,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,   6,  0x00020040,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,   6,  0x00000440,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,   6,  0xf4640000,   '?',      '?',       '?'      ],
  ] )

def test_alu_xor( dump_vcd, test_verilog ):
  dut = AluRTL()
  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   7,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,   7,  0x0ffb8564,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,   7,  0xd6712010,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,   7,  0xfff0e010,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,   7,  0x0a8beaa3,   '?',      '?',       '?'      ],
  ] )

def test_alu_nor( dump_vcd, test_verilog ):
  dut = AluRTL()
  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   8,  0xffffffff,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,   8,  0xf004589b,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,   8,  0x298cdfaf,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,   8,  0x000f1baf,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,   8,  0x0110155c,   '?',      '?',       '?'      ],
  ] )

def test_alu_srl( dump_vcd, test_verilog ):
  dut = AluRTL()
  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   9,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x05050505,   0x00000001,   9,  0x02828282,   '?',      '?',       '?'      ],
    [ 0x05050505,   0x00000002,   9,  0x01414141,   '?',      '?',       '?'      ],
    [ 0x05050505,   0x00000004,   9,  0x00505050,   '?',      '?',       '?'      ],
    [ 0x50505050,   0x00000008,   9,  0x00505050,   '?',      '?',       '?'      ],
    [ 0x50505050,   0x0000000f,   9,  0x0000a0a0,   '?',      '?',       '?'      ],
    [ 0x50505050,   0x00000010,   9,  0x00005050,   '?',      '?',       '?'      ],
    [ 0x50505050,   0x0000001f,   9,  0x00000000,   '?',      '?',       '?'      ],
  ] )

def test_alu_sra( dump_vcd, test_verilog ):
  dut = AluRTL()
  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   10,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x05050505,   0x00000001,   10,  0x02828282,   '?',      '?',       '?'      ],
    [ 0x05050505,   0x00000002,   10,  0x01414141,   '?',      '?',       '?'      ],
    [ 0x05050505,   0xffffff01,   10,  0x02828282,   '?',      '?',       '?'      ],
    [ 0x05050505,   0xffffff02,   10,  0x01414141,   '?',      '?',       '?'      ],
    [ 0x05050505,   0x00000004,   10,  0x00505050,   '?',      '?',       '?'      ],
    [ 0x80808080,   0x00000008,   10,  0xff808080,   '?',      '?',       '?'      ],
    [ 0x80808080,   0x0000000f,   10,  0xffff0101,   '?',      '?',       '?'      ],
    [ 0x80808080,   0x00000010,   10,  0xffff8080,   '?',      '?',       '?'      ],
    [ 0x80808080,   0x0000001f,   10,  0xffffffff,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0x0000001f,   10,  0xffffffff,   '?',      '?',       '?'      ],
  ] )

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\

def test_alu_cp_op0( dump_vcd, test_verilog ):
  dut = AluRTL()
  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  11,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  11,  0x0ffaa660,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  11,  0x00132050,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  11,  0xfff0a440,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  11,  0xfeeeeaa3,   '?',      '?',       '?'      ],
  ] )

def test_alu_cp_op1( dump_vcd, test_verilog ):
  dut = AluRTL()
  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  12,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  12,  0x00012304,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  12,  0xd6620040,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  12,  0x00004450,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  12,  0xf4650000,   '?',      '?',       '?'      ],
  ] )

def test_alu_fn_equality( dump_vcd, test_verilog ):
  dut = AluRTL()
  config_model( dut, dump_vcd, test_verilog )

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  14,  0x00000000,   1,        '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  14,  0x00000000,   0,        '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  14,  0x00000000,   0,        '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  14,  0x00000000,   0,        '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  14,  0x00000000,   0,        '?',       '?'      ],
  ] )
