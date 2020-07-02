#!/bin/env python
#======================================================================
# gen_wrapper.py
#======================================================================
# 
#   Generate wrapper for SRAM configuration
#
# Author: Khalid Al-Hawaj
# Date  : March 3, 2020
#

# Imports

import sys
import os
import math
import importlib.util

# Template

template = \
'''//-----------------------------------------------------------------------------
// SRAM
//-----------------------------------------------------------------------------
module SRAM_{word_size}x{num_words}_1P
(
  input wire           clk,
  input wire           reset,
  input wire           CE1,
  input wire           OEB1,
  input wire           CSB1,
  input wire  [   {addr_size_p}:0] A1,
  input wire  [  {word_size_p}:0] I1,
  input wire           WEB1,
  output reg  [  {word_size_p}:0] O1
);
  parameter DATA_WIDTH = {word_size} ;
  parameter ADDR_WIDTH = {addr_size} ;

  // Internal wires
  wire [DATA_WIDTH-1:0] DATA;

  // Registers
  reg  [DATA_WIDTH-1:0] dataout;
  reg                   read;

  // Assigns
  assign DATA    = (!CSB1 && !WEB1) ?  I1 : 'bz  ;

  always_ff @(negedge CE1) begin
    read <= (!CSB1 &&  WEB1);

    if (read) begin
      dataout <= DATA;
    end
  end

  // Output ports
  assign O1   = dataout;

  // Actual RAM
  SRAM_{word_size}x{num_words}_1P_inner sram ( .DATA(DATA),
       {spaces}                  .ADDR(A1  ),
       {spaces}                  .CSb (CSB1),
       {spaces}                  .WEb (WEB1),
       {spaces}                  .OEb (OEB1),
       {spaces}                  .clk (~CE1)
       {spaces}                );
endmodule
\
'''

# Get the arguments

nargs = len(sys.argv)
argsv = sys.argv

# If no arguments, exit

if nargs < 2:
  exit(0)

# Config file

config_path = argsv[1]

# Let's magic

config_file = os.path.basename(config_path)
config_dir  = os.path.dirname(config_path)

if config_file.endswith('.py'):
  config_file = config_file[:-3]

try:
  sys.path.append(config_dir)
  config = __import__(config_file)
except:
  config = None

if config == None:
  exit(1)

# Process

sram_module_name = config.output_name
instance_name    = config.instance_name
sram_word_size   = config.word_size
sram_num_words   = config.num_words

# Parameters

word_size   = sram_word_size
num_words   = sram_num_words
addr_size   = int(round(math.log2(num_words), 0))
addr_size_p = addr_size - 1
word_size_p = word_size - 1
num_words_p = num_words - 1

# Aesthetics

word_size_len = len(str(word_size))
num_words_len = len(str(num_words))
spaces        = ' ' * (word_size_len + num_words_len)

# Create the template

wrapper = template.format(**locals())

# Print the wrapper

print(wrapper)
