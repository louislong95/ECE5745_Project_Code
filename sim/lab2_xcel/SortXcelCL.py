#=========================================================================
# Sort Unit CL Model
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

from pymtl3     import *

from copy       import deepcopy

from pymtl3.stdlib.ifcs.xcel_ifcs import XcelMinionIfcCL
from pymtl3.stdlib.ifcs.mem_ifcs  import MemMasterIfcCL, mk_mem_msg, MemMsgType
from pymtl3.stdlib.cl  import PipeQueueCL

from proc.XcelMsg import *

class SortXcelCL( Component ):

  # Constructor

  def construct( s ):

    MemReqMsg, MemRespMsg = mk_mem_msg( 8,32,32 )

    # Interface

    s.xcel = XcelMinionIfcCL( XcelReqMsg, XcelRespMsg )

    s.mem  = MemMasterIfcCL( *mk_mem_msg(8,32,32) )

    # ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Create CL model for sorting xcel
    # '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

    # Components

    s.xcelreq_q = PipeQueueCL( num_entries=1 )( enq = s.xcel.req )
    s.memresp_q = PipeQueueCL( num_entries=1 )( enq = s.mem.resp )

    # Internal state

    s.base_addr   = 0
    s.size        = 0
    s.inner_count = 0
    s.outer_count = 0
    s.a           = b32(0)
    s.b           = b32(0)

    # State

    s.STATE_XCFG    = 0
    s.STATE_FIRST0  = 1
    s.STATE_FIRST1  = 2
    s.STATE_BUBBLE0 = 3
    s.STATE_BUBBLE1 = 4
    s.STATE_LAST    = 5
    s.state         = s.STATE_XCFG

    # Line tracing

    s.prev_state = 0
    s.xcfg_trace = "  "

    # logic

    @s.update
    def block():

      # Line tracing string

      s.prev_state = s.state

      #-------------------------------------------------------------------
      # STATE: XCFG
      #-------------------------------------------------------------------
      # In this state we handle the accelerator configuration protocol,
      # where we write the base address, size, and then tell the
      # accelerator to start. We also handle responding when the
      # accelerator is done.

      if s.state == s.STATE_XCFG:
        s.xcfg_trace = "  "
        if s.xcelreq_q.deq.rdy() and s.xcel.resp.rdy():

          xcelreq_msg = s.xcelreq_q.deq()

          if xcelreq_msg.type_ == XCEL_TYPE_WRITE:

            assert xcelreq_msg.addr in [0,1,2], \
              "Only reg writes to 0,1,2 allowed during setup!"

            if   xcelreq_msg.addr == 0:
              s.xcfg_trace = "X0"
              s.outer_count = 0
              s.state = s.STATE_FIRST0

            elif xcelreq_msg.addr == 1:
              s.xcfg_trace = "X1"
              s.base_addr = xcelreq_msg.data.uint()

            elif xcelreq_msg.addr == 2:
              s.xcfg_trace = "X2"
              s.size = xcelreq_msg.data.uint()

            # Send xcel response message

            s.xcel.resp( XcelRespMsg(XCEL_TYPE_WRITE, 0) )

          else:

            s.xcfg_trace = "x0"

            assert xcelreq_msg.addr == 0

            # Send xcel response message, obviously you only want to
            # send the response message when accelerator is done

            s.xcel.resp( XcelRespMsg(XCEL_TYPE_READ, 1) )

      #-------------------------------------------------------------------
      # STATE: FIRST0
      #-------------------------------------------------------------------
      # Send the first memory read request for the very first
      # element in the array.

      elif s.state == s.STATE_FIRST0:
        if s.mem.req.rdy():
          s.mem.req( MemReqMsg( MemMsgType.READ, 0, s.base_addr, 0 ) )
          s.inner_count = 1
          s.state = s.STATE_FIRST1

      #-------------------------------------------------------------------
      # STATE: FIRST1
      #-------------------------------------------------------------------
      # Wait for the memory response for the first element in the array,
      # and once it arrives store this element in a, and send the memory
      # read request for the second element.

      elif s.state == s.STATE_FIRST1:
        if s.mem.req.rdy() and s.memresp_q.deq.rdy():
          s.a = s.memresp_q.deq().data
          addr = s.base_addr + 4*s.inner_count
          s.mem.req( MemReqMsg( MemMsgType.READ, 4, addr, 0 ) )
          s.state = s.STATE_BUBBLE0

      #-------------------------------------------------------------------
      # STATE: BUBBLE0
      #-------------------------------------------------------------------
      # Wait for the memory read response to get the next element,
      # compare the new value to the previous max value, update b with
      # the new max value, and send a memory request to store the new min
      # value. Notice how we decrement the write address by four since we
      # want to store to the new min value _previous_ element.

      elif s.state == s.STATE_BUBBLE0:
        if s.mem.req.rdy() and s.memresp_q.deq.rdy():
          s.b = deepcopy( s.memresp_q.deq().data )
          max_value = max( s.a, s.b )
          min_value = min( s.a, s.b )
          s.a = max_value
          addr = s.base_addr + 4*s.inner_count
          s.mem.req( MemReqMsg( MemMsgType.WRITE, 4, addr-4, 0, min_value ) )
          s.state = s.STATE_BUBBLE1

      #-------------------------------------------------------------------
      # STATE: BUBBLE1
      #-------------------------------------------------------------------
      # Wait for the memory write response, and then check to see if we
      # have reached the end of the array. If we have not reached the end
      # of the array, then make a new memory read request for the next
      # element; if we have reached the end of the array, then make a
      # final write request (with value from a) to update the final
      # element in the array.

      elif s.state == s.STATE_BUBBLE1:
        if s.mem.req.rdy() and s.memresp_q.deq.rdy():
          s.memresp_q.deq()
          s.inner_count += 1
          if s.inner_count < s.size:

            addr = s.base_addr + 4*s.inner_count
            s.mem.req( MemReqMsg( MemMsgType.READ, 4, addr, 0 ) )
            s.state = s.STATE_BUBBLE0

          else:

            addr = s.base_addr + 4*s.inner_count
            s.mem.req( MemReqMsg( MemMsgType.WRITE, 4, addr-4, 0, s.a ) )
            s.state = s.STATE_LAST

      #-------------------------------------------------------------------
      # STATE: LAST
      #-------------------------------------------------------------------
      # Wait for the last response, and then check to see if we need to
      # go through the array again. If we do need to go through array
      # again, then make a new memory read request for the very first
      # element in the array; if we do not need to go through the array
      # again, then we are all done and we can go back to accelerator
      # configuration.

      elif s.state == s.STATE_LAST:
        if s.mem.req.rdy() and s.memresp_q.deq.rdy():
          s.memresp_q.deq()
          s.outer_count += 1
          if s.outer_count < s.size:

            s.mem.req( MemReqMsg( MemMsgType.READ, 4, s.base_addr, 0 ) )
            s.inner_count = 1
            s.state = s.STATE_FIRST1

          else:
            s.state = s.STATE_XCFG

    # '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\

  # Line tracing

  def line_trace( s ):

    s.trace = ""

    # ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Define line trace here.
    # '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

    state2char = {
      s.STATE_XCFG    : "X",
      s.STATE_FIRST0  : "F0",
      s.STATE_FIRST1  : "F1",
      s.STATE_BUBBLE0 : "B0",
      s.STATE_BUBBLE1 : "B1",
      s.STATE_LAST    : "L ",
    }

    if s.prev_state == s.STATE_XCFG:
      s.state_str = s.xcfg_trace
    else:
      s.state_str = state2char[s.prev_state]

    s.trace = "({:2}:{:2}:{}|{}:{})".format(
      s.outer_count, s.inner_count,
      s.state_str,
      s.a, s.b
    )

    # '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\

    return s.trace

