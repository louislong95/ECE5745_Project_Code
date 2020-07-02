#=========================================================================
# Primetime Power Analysis
#=========================================================================

#-------------------------------------------------------------------------
# Interface to the build system
#-------------------------------------------------------------------------

set design_name             $::env(design_name)
set saif_filename           $::env(saif_filename)

set pt_extra_link_libraries [glob -nocomplain inputs/*.db]

#-------------------------------------------------------------------------
# commands
#-------------------------------------------------------------------------

set_app_var target_library "inputs/adk/stdcells.db"
set_app_var link_library   "* inputs/adk/stdcells.db $pt_extra_link_libraries"

set power_enable_analysis true
set power_analysis_mode   averaged

read_verilog "inputs/design.vcs.v"

current_design ${design_name}

link_design

source outputs/design.mapped.saif.namemap

# The "Annotating RTL Activity in PrimeTime PX" said on Page 9: "When
# annotating netlists from IC Compiler, users should set the variables
# to disable exact-name matching to prevent annotation of RTL activity
# on same-name nets and hierarchical ports." Not quite sure what these
# variables do though.

set power_disable_exact_name_matching_to_nets      true
set power_disable_exact_name_matching_to_hier_pins true

read_saif "${saif_filename}" -strip_path "TOP/${design_name}"

read_parasitics -format spef "inputs/design.spef.gz"

report_annotated_parasitics -check

read_sdc "inputs/design.mapped.sdc"
source clk-def.tcl
set_propagated_clock [all_clocks]

update_timing -full

check_power
update_power

report_switching_activity

report_power -nosplit            > reports/power-summary.rpt
report_power -nosplit -hierarchy > reports/power-hierarchy.rpt

exit
