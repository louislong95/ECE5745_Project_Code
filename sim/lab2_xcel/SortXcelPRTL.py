#=========================================================================
# Sort Unit RTL Model
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

from pymtl3.stdlib.ifcs.xcel_ifcs import XcelMinionIfcRTL
from pymtl3.stdlib.ifcs.mem_ifcs  import MemMasterIfcRTL, mk_mem_msg, MemMsgType
from pymtl3.stdlib.rtl  import BypassQueueRTL, PipeQueueRTL, Reg

from proc.XcelMsg import *

class SortXcelPRTL( Component ):

  # Constructor

  def construct( s ):

    MemReqMsg, MemRespMsg = mk_mem_msg( 8,32,32 )
    MEM_TYPE_READ  = b4(MemMsgType.READ)
    MEM_TYPE_WRITE = b4(MemMsgType.WRITE)

    # Interface

    s.xcel = XcelMinionIfcRTL( XcelReqMsg, XcelRespMsg )

    s.mem  = MemMasterIfcRTL( *mk_mem_msg(8,32,32) )

    # ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Create RTL model for sorting xcel
    # '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

    # Queues

    s.xcelreq_q = PipeQueueRTL( XcelReqMsg, 1 )( enq = s.xcel.req )
    s.memresp_q = PipeQueueRTL( MemRespMsg, 1 )( enq = s.mem.resp )

    # Internal state

    s.base_addr   = Reg( Bits32 )
    s.size        = Reg( Bits32 )
    s.inner_count = Reg( Bits32 )
    s.outer_count = Reg( Bits32 )
    s.a           = Reg( Bits32 )

    # Line tracing

    s.prev_state = 0
    s.xcfg_trace = "  "

    #=====================================================================
    # State Update
    #=====================================================================

    s.STATE_XCFG    = b8(0)
    s.STATE_FIRST0  = b8(1)
    s.STATE_FIRST1  = b8(2)
    s.STATE_BUBBLE0 = b8(3)
    s.STATE_BUBBLE1 = b8(4)
    s.STATE_LAST    = b8(5)

    s.state         = Wire(Bits8)
    s.go            = Wire()

    @s.update_ff
    def block0():

      if s.reset:
        s.state <<= s.STATE_XCFG

      elif s.state == s.STATE_XCFG:
        if s.go & s.xcel.resp.rdy:
          s.state <<= s.STATE_FIRST0

      elif s.state == s.STATE_FIRST0:
        if s.mem.req.rdy:
          s.state <<= s.STATE_FIRST1

      elif s.state == s.STATE_FIRST1:
        if s.mem.req.rdy and s.memresp_q.deq.rdy:
          s.state <<= s.STATE_BUBBLE0

      elif s.state == s.STATE_BUBBLE0:
        if s.mem.req.rdy and s.memresp_q.deq.rdy:
          s.state <<= s.STATE_BUBBLE1

      elif s.state == s.STATE_BUBBLE1:
        if s.mem.req.rdy and s.memresp_q.deq.rdy:
          if s.inner_count.out+1 < s.size.out:
            s.state <<= s.STATE_BUBBLE0
          else:
            s.state <<= s.STATE_LAST

      elif s.state == s.STATE_LAST:
        if s.mem.req.rdy and s.memresp_q.deq.rdy:
          if s.outer_count.out+1 < s.size.out:
            s.state <<= s.STATE_FIRST1
          else:
            s.state <<= s.STATE_XCFG

    #=====================================================================
    # State Outputs
    #=====================================================================

    @s.update
    def block1():

      s.xcelreq_q.deq.en = b1(0)
      s.xcel.resp.en     = b1(0)
      s.mem.req.en       = b1(0)
      s.mem.req.msg      = MemReqMsg()
      s.memresp_q.deq.en = b1(0)
      s.go               = b1(0)

      s.outer_count.in_ = s.outer_count.out
      s.inner_count.in_ = s.inner_count.out
      s.a.in_           = s.a.out
      s.size.in_        = s.size.out
      s.base_addr.in_   = s.base_addr.out

      #-------------------------------------------------------------------
      # STATE: XCFG
      #-------------------------------------------------------------------

      if s.state == s.STATE_XCFG:

        if s.xcelreq_q.deq.rdy & s.xcel.resp.rdy:
          s.xcelreq_q.deq.en = b1(1)
          s.xcel.resp.en     = b1(1)

          if s.xcelreq_q.deq.ret.type_ == XCEL_TYPE_WRITE:

            if   s.xcelreq_q.deq.ret.addr == b5(0):
              s.outer_count.in_ = b32(0)
              s.inner_count.in_ = b32(0)
              s.go              = b1(1)

            elif s.xcelreq_q.deq.ret.addr == b5(1):
              s.base_addr.in_ = s.xcelreq_q.deq.ret.data

            elif s.xcelreq_q.deq.ret.addr == b5(2):
              s.size.in_ = s.xcelreq_q.deq.ret.data

            # Send xcel response message

            s.xcel.resp.msg = XcelRespMsg( XCEL_TYPE_WRITE, b32(0) )

          else:

            # Send xcel response message, obviously you only want to
            # send the response message when accelerator is done

            s.xcel.resp.msg = XcelRespMsg( XCEL_TYPE_READ, b32(1) )

      #-------------------------------------------------------------------
      # STATE: FIRST0
      #-------------------------------------------------------------------
      # Send the first memory read request for the very first
      # element in the array.

      elif s.state == s.STATE_FIRST0:
        if s.mem.req.rdy:
          s.mem.req.en      = s.mem.req.rdy
          s.mem.req.msg     = MemReqMsg( MEM_TYPE_READ, b8(0), s.base_addr.out + 4*s.inner_count.out, b2(0), b32(0) )
          s.inner_count.in_ = b32(1)

      #-------------------------------------------------------------------
      # STATE: FIRST1
      #-------------------------------------------------------------------
      # Wait for the memory response for the first element in the array,
      # and once it arrives store this element in a, and send the memory
      # read request for the second element.

      elif s.state == s.STATE_FIRST1:

        if s.mem.req.rdy and s.memresp_q.deq.rdy:
          s.memresp_q.deq.en = b1(1)
          s.mem.req.en       = b1(1)

          s.a.in_ = s.memresp_q.deq.ret.data

          s.mem.req.msg = MemReqMsg( MEM_TYPE_READ, b8(0), s.base_addr.out + 4*s.inner_count.out, b2(0), b32(0) )

      #-------------------------------------------------------------------
      # STATE: BUBBLE0
      #-------------------------------------------------------------------
      # Wait for the memory read response to get the next element,
      # compare the new value to the previous max value, update b with
      # the new max value, and send a memory request to store the new min
      # value. Notice how we decrement the write address by four since we
      # want to store to the new min value _previous_ element.

      elif s.state == s.STATE_BUBBLE0:
        if s.mem.req.rdy and s.memresp_q.deq.rdy:
          s.memresp_q.deq.en = b1(1)
          s.mem.req.en       = b1(1)

          if s.a.out > s.memresp_q.deq.ret.data:
            s.a.in_ = s.a.out
            s.mem.req.msg = MemReqMsg( MEM_TYPE_WRITE, b8(0),
                                       s.base_addr.out + 4*(s.inner_count.out-1), b2(0),
                                       s.memresp_q.deq.ret.data )
          else:
            s.a.in_ = s.memresp_q.deq.ret.data
            s.mem.req.msg = MemReqMsg( MEM_TYPE_WRITE, b8(0),
                                       s.base_addr.out + 4*(s.inner_count.out-1), b2(0),
                                       s.a.out )

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
        if s.mem.req.rdy and s.memresp_q.deq.rdy:
          s.memresp_q.deq.en = b1(1)
          s.mem.req.en       = b1(1)

          s.inner_count.in_ = s.inner_count.out + 1

          if s.inner_count.out+1 < s.size.out:
            s.mem.req.msg = MemReqMsg( MEM_TYPE_READ, b8(0),
                                       s.base_addr.out + 4*(s.inner_count.out+1), b2(0), b32(0) )

          else:
            s.mem.req.msg = MemReqMsg( MEM_TYPE_WRITE, b8(0),
                                       s.base_addr.out + 4*s.inner_count.out, b2(0),
                                       s.a.out )

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
        if s.mem.req.rdy and s.memresp_q.deq.rdy:
          s.memresp_q.deq.en = b1(1)

          s.outer_count.in_ = s.outer_count.out + b32(1)

          if s.outer_count.out + b32(1) < s.size.out:

            s.mem.req.en      = b1(1)
            s.mem.req.msg     = MemReqMsg( MEM_TYPE_READ, b8(0), s.base_addr.out, b2(0), b32(0) )
            s.inner_count.in_ = b32(1)

    # '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\

  # Line tracing

  def line_trace( s ):

    s.trace = ""

    # ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Define line trace here
    # '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

    state2char = {
      s.STATE_XCFG    : "X ",
      s.STATE_FIRST0  : "F0",
      s.STATE_FIRST1  : "F1",
      s.STATE_BUBBLE0 : "B0",
      s.STATE_BUBBLE1 : "B1",
      s.STATE_LAST    : "L ",
    }

    s.state_str = state2char[s.state]

    s.trace = "({!s:2}:{!s:2}:{})".format(
      s.outer_count.out, s.inner_count.out,
      s.state_str
    )

    # '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\

    return s.trace

