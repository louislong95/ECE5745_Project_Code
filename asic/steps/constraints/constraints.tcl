#=========================================================================
# Design Constraints File
#=========================================================================

# This constraint sets the target clock period for the chip in
# nanoseconds. Note that the first parameter is the name of the clock
# signal in your verlog design. If you called it something different than
# clk you will need to change this. You should set this constraint
# carefully. If the period is unrealistically small then the tools will
# spend forever trying to meet timing and ultimately fail. If the period
# is too large the tools will have no trouble but you will get a very
# conservative implementation.

set clock_net  clk
set clock_name ideal_clock

create_clock -name ${clock_name} \
             -period ${dc_clock_period} \
             [get_ports ${clock_net}]



# This constraint sets the load capacitance in picofarads of the
# output pins of your design.

set_load -pin_load $ADK_TYPICAL_ON_CHIP_LOAD [all_outputs]

# This constraint sets the input drive strength of the input pins of
# your design. We specifiy a specific standard cell which models what
# would be driving the inputs. This should usually be a small inverter
# which is reasonable if another block of on-chip logic is driving
# your inputs.

set_driving_cell -no_design_rule \
  -lib_cell $ADK_DRIVING_CELL [all_inputs]

# Get lists of inputs and filtered inputs

set inputs_list         [all_inputs]
set inputs_no_clk       [remove_from_collection $inputs_list   [get_attribute [get_clocks] sources]]
set inputs_no_clk_reset [remove_from_collection $inputs_no_clk [get_ports     reset               ]]

set input_delay  [expr ${dc_clock_period} * 0.05]
set output_delay 0

# set_input_delay constraints for input ports
#
# - make this non-zero to avoid hold buffers on input-registered designs

set_input_delay -clock ${clock_name} $input_delay $inputs_no_clk_reset

# set_output_delay constraints for output ports

set_output_delay -clock ${clock_name} 0 [all_outputs]

# Give DC a harder time

if {"${dc_max_delay}" != "" && "${dc_max_delay}" != "None" && "${dc_max_delay}" != "NONE" && "${dc_max_delay}" != "undefined"} {
  puts "INFO: Constrainting DC paths to [expr ${dc_max_delay} * 100]% of the ${dc_clock_period}ns clock period."
  puts "INFO: max_delay = [expr ${dc_clock_period} * ${dc_max_delay}]ns."

  set_max_delay [expr ${dc_clock_period} * ${dc_max_delay}] -from [all_inputs]
  set_max_delay [expr ${dc_clock_period} * ${dc_max_delay}] -to   [all_outputs]
  set_max_delay [expr ${dc_clock_period} * ${dc_max_delay}] -to   [all_registers]
  set_max_delay [expr ${dc_clock_period} * ${dc_max_delay}] -from [all_registers]
}

# Make all signals limit their fanout

set_max_fanout 20 $dc_design_name

# Make all signals meet good slew

set_max_transition [expr 0.25*${dc_clock_period}] $dc_design_name

#set_input_transition 1 [all_inputs]
#set_max_transition 10 [all_outputs]

