#! /usr/bin/env python
#=========================================================================
# flow.py
#=========================================================================
# Flow setup for fixed-latency iterative integer multiplier
#
# Author : Khalid Al-Hawaj
# Date   : Feb 12, 2020
#

import os
import sys

from mflowgen.components import Graph, Step

def construct():

  g = Graph()

  #-----------------------------------------------------------------------
  # Parameters
  #-----------------------------------------------------------------------

  adk_name = 'freepdk-45nm'
  adk_view = 'view-standard'

  parameters = {
    'construct_path'         : __file__,
    'design_name'            : 'SRAM_64x64_1P',
    'clock_period'           : 6.0,
    'flatten_effort'         : 0,
    'adk'                    : adk_name,
    'adk_view'               : adk_view,
    'topographical'          : True,
    'sim_directory'          : '../../../sim/build',
    'rtl'                    : 'SRAM_64x64_1P.v',
    'vcd'                    : '''
                               ''',
    'openram_cfgs_directory' : '../../../sim/sram',
    'openram_cfgs'           : '''
                                 "SRAM_64x64_1P-cfg.py"
                               ''',
  }

  #-----------------------------------------------------------------------
  # Create nodes
  #-----------------------------------------------------------------------

  this_dir = os.path.dirname( os.path.abspath( __file__ ) )

  # ADK step

  g.set_adk( adk_name )
  adk = g.get_adk_step()

  # Custom steps

  rtl = Step( this_dir + '/rtl' )

  # Default steps

  info         = Step( 'info',                          default=True )
  constraints  = Step( 'constraints',                   default=True )

  vcd          = Step( 'vcd',                           default=True )

  vcd2saif     = Step( 'vcd2saif',                      default=True )

  # OpenRAM steps

  openram_cfg  = Step( 'openram-configs',               default=True )
  openram_gen  = Step( 'openram-generate',              default=True )
  openram_db   = Step( 'openram-generate-db',           default=True )

  dc           = Step( 'synopsys-dc-synthesis',         default=True )
  iflow        = Step( 'cadence-innovus-flowsetup',     default=True )
  placeroute   = Step( 'cadence-innovus-place-route',   default=True )
  genlibdb     = Step( 'synopsys-ptpx-genlibdb',        default=True )
  gdsmerge     = Step( 'mentor-calibre-gdsmerge',       default=True )
  #drc          = Step( 'mentor-calibre-drc',            default=True )
  #lvs          = Step( 'mentor-calibre-lvs',            default=True )
  ptpwr        = Step( 'synopsys-pt-pwr',               default=True )
  summary      = Step( 'summarize-results',             default=True )

  #-----------------------------------------------------------------------
  # Graph -- Add nodes
  #-----------------------------------------------------------------------

  g.add_step( info         )
  g.add_step( constraints  )
  g.add_step( rtl          )
  g.add_step( vcd          )
  g.add_step( vcd2saif     )
  g.add_step( openram_cfg  )
  g.add_step( openram_gen  )
  g.add_step( openram_db   )
  g.add_step( dc           )
  g.add_step( iflow        )
  g.add_step( placeroute   )
  g.add_step( genlibdb     )
  g.add_step( gdsmerge     )
  #g.add_step( drc          )
  #g.add_step( lvs          )
  g.add_step( ptpwr        )
  g.add_step( summary      )

  #-----------------------------------------------------------------------
  # Graph -- Add edges
  #-----------------------------------------------------------------------

  # Connect by name

  g.connect_by_name( vcd,         vcd2saif     )

  g.connect_by_name( openram_cfg, openram_gen  )
  g.connect_by_name( openram_gen, openram_db   )

  g.connect_by_name( openram_db,  dc           )
  g.connect_by_name( vcd2saif,    dc           )
  g.connect_by_name( rtl,         dc           )
  g.connect_by_name( adk,         dc           )
  g.connect_by_name( constraints, dc           )

  g.connect_by_name( adk,         iflow        )
  g.connect_by_name( dc,          iflow        )
  g.connect_by_name( openram_gen, iflow        )
  g.connect_by_name( openram_db,  iflow        )


  g.connect_by_name( adk,         placeroute   )
  g.connect_by_name( dc,          placeroute   )
  g.connect_by_name( iflow,       placeroute   )
  g.connect_by_name( openram_gen, placeroute   )
  g.connect_by_name( openram_db,  placeroute   )

  g.connect_by_name( placeroute,  genlibdb     )
  g.connect_by_name( adk,         genlibdb     )

  #g.connect_by_name( adk,         drc          )
  #g.connect_by_name( placeroute,  drc          )

  #g.connect_by_name( adk,         lvs          )
  #g.connect_by_name( placeroute,  lvs          )

  g.connect_by_name( adk,         gdsmerge     )
  g.connect_by_name( placeroute,  gdsmerge     )
  g.connect_by_name( openram_gen, gdsmerge     )

  #g.connect_by_name( gdsmerge,    drc          )
  #g.connect_by_name( gdsmerge,    lvs          )

  g.connect_by_name( adk,         ptpwr        )
  g.connect_by_name( vcd2saif,    ptpwr        )
  g.connect_by_name( dc,          ptpwr        )
  g.connect_by_name( placeroute,  ptpwr        )

  g.connect_by_name( adk,         summary      )
  g.connect_by_name( dc,          summary      )
  g.connect_by_name( iflow,       summary      )
  g.connect_by_name( placeroute,  summary      )
  g.connect_by_name( ptpwr,       summary      )
  #g.connect_by_name( genlibdb,    summary      )
  #g.connect_by_name( gdsmerge,    summary      )

  #-----------------------------------------------------------------------
  # Parameterize
  #-----------------------------------------------------------------------

  g.update_params( parameters )

  return g

if __name__ == '__main__':
  g = construct()
#  g.plot()

