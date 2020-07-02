#! /usr/bin/env python
#=========================================================================
# flow.py
#=========================================================================
# Flow setup for pipelined integer multiplier with 8 stages
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
    'construct_path' : __file__,
    'design_name'    : 'lab1_imul_IntMulNstageRTL_8stages',
    'clock_period'   : 6.0,
    'flatten_effort' : 0,
    'adk'            : adk_name,
    'adk_view'       : adk_view,
    'topographical'  : True,
    'sim_directory'  : '../../../sim/build',
    'rtl'            : 'lab1_imul_IntMulNstageRTL_8stages.v',
    'vcd'            : '''
                          "imul-rtl-8stage-small.vcd"
                          "imul-rtl-8stage-large.vcd"
                          "imul-rtl-8stage-lomask.vcd"
                          "imul-rtl-8stage-himask.vcd"
                          "imul-rtl-8stage-lohimask.vcd"
                          "imul-rtl-8stage-sparse.vcd"
                       ''',
  }

  #-----------------------------------------------------------------------
  # Create nodes
  #-----------------------------------------------------------------------

  this_dir = os.path.dirname( os.path.abspath( __file__ ) )

  # ADK step

  g.set_adk( adk_name )
  adk = g.get_adk_step()

  # Default steps

  rtl          = Step( 'rtl',                           default=True )
  vcd          = Step( 'vcd',                           default=True )
  info         = Step( 'info',                          default=True )
  vcd2saif     = Step( 'vcd2saif',                      default=True )
  constraints  = Step( 'constraints',                   default=True )
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
  g.add_step( vcd2saif     )
  g.add_step( rtl          )
  g.add_step( vcd          )
  g.add_step( constraints  )
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

  g.connect_by_name( vcd2saif,    dc           )
  g.connect_by_name( rtl,         dc           )
  g.connect_by_name( adk,         dc           )
  g.connect_by_name( constraints, dc           )

  g.connect_by_name( adk,         iflow        )
  g.connect_by_name( dc,          iflow        )

  g.connect_by_name( adk,         placeroute   )
  g.connect_by_name( dc,          placeroute   )
  g.connect_by_name( iflow,       placeroute   )

  g.connect_by_name( placeroute,  genlibdb     )
  g.connect_by_name( adk,         genlibdb     )

  #g.connect_by_name( adk,         drc          )
  #g.connect_by_name( placeroute,  drc          )

  #g.connect_by_name( adk,         lvs          )
  #g.connect_by_name( placeroute,  lvs          )

  g.connect_by_name( adk,         gdsmerge     )
  g.connect_by_name( placeroute,  gdsmerge     )

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

