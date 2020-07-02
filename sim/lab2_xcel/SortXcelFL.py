#=========================================================================
# Sort Unit FL Model
#=========================================================================
# Sort array in memory containing positive integers.
# Accelerator register interface:
#
#  xr0 : go/done
#  xr1 : base address of array
#  xr2 : number of elements in array
#
# Accelerator protocol involves the following steps:
#  1. Write the base address of array via xr1
#  2. Write the number of elements in array via xr2
#  3. Tell accelerator to go by writing xr0
#  4. Wait for accelerator to finish by reading xr0, result will be 1
#

from pymtl3      import *
from pymtl3.stdlib.ifcs.xcel_ifcs import XcelMinionIfcFL
from pymtl3.stdlib.ifcs.mem_ifcs  import MemMasterIfcFL

class SortXcelFL( Component ):

  def read( s, addr ):
    return s.xr[addr]

  def write( s, addr, data ):

    if addr == 0:
      s.xr[addr] = b32(1)
      arr = []
      for i in range( s.xr[2] ):
        arr.append( s.mem.read( s.xr[1] + i*4, nbytes=4 ) )

      arr = sorted(arr)

      for i in range( s.xr[2] ):
        s.mem.write( s.xr[1] + i*4, nbytes=4, data=arr[i] )

    else:
      s.xr[addr] = b32(data)

  # Constructor

  def construct( s ):

    # Interface

    s.xcel = XcelMinionIfcFL( read=s.read, write=s.write )
    s.mem  = MemMasterIfcFL()

    # Storage

    s.xr = [ b32(0) for _ in range(3) ]

    # Explicitly tell PyMTL3 than s.read calls s.mem.read

    s.add_constraints(
      M(s.read)  == M(s.mem.read),
      M(s.write) == M(s.mem.write),
    )

  # Line tracing

  def line_trace( s ):
    return f"{s.xcel}|{s.mem}"

