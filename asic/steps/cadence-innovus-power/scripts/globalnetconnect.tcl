#=========================================================================
# globalnetconnect.tcl
#=========================================================================
# Author : Christopher Torng
# Date   : January 13, 2020

#-------------------------------------------------------------------------
# Global net connections for PG pins
#-------------------------------------------------------------------------

globalNetConnect VDD    -type pgpin -pin VDD    -inst * -verbose
globalNetConnect VSS    -type pgpin -pin VSS    -inst * -verbose

# Connect VNW / VPW if any cells have these pins

#if { [ lindex [dbGet top.insts.cell.pgterms.name VNW] 0 ] != 0x0 } {
#  globalNetConnect VDD    -type pgpin -pin VNW    -inst * -verbose
#  globalNetConnect VSS    -type pgpin -pin VPW    -inst * -verbose
#}

# Connect PGPins if any cells have these pins

foreach net $vars(power_nets) {
  globalNetConnect VDD -type pgpin -pin $net -inst * -verbose
}

foreach net $vars(ground_nets) {
  globalNetConnect VSS -type pgpin -pin $net -inst * -verbose
}
