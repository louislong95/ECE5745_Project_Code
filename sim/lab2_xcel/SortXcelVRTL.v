//=========================================================================
// Sorting Accelerator Implementation
//=========================================================================
// Sort array in memory containing positive integers.
// Accelerator register interface:
//
//  xr0 : go/done
//  xr1 : base address of array
//  xr2 : number of elements in array
//
// Accelerator protocol involves the following steps:
//  1. Write the base address of array via xr1
//  2. Write the number of elements in array via xr2
//  3. Tell accelerator to go by writing xr0
//  4. Wait for accelerator to finish by reading xr0, result will be 1
//

`ifndef LAB2_SORT_SORT_XCEL_V
`define LAB2_SORT_SORT_XCEL_V

`include "vc/trace.v"

`include "vc/mem-msgs.v"
`include "vc/queues.v"
`include "proc/XcelMsg.v"

//=========================================================================
// Sorting Accelerator Implementation
//=========================================================================

module lab2_xcel_SortXcelVRTL
(
  input  logic         clk,
  input  logic         reset,

  // look at XcelMsg for bit definition
  output logic         xcelreq_rdy,
  input  logic         xcelreq_en,
  input  XcelReqMsg    xcelreq_msg,

  input  logic         xcelresp_rdy,
  output logic         xcelresp_en,
  output XcelRespMsg   xcelresp_msg,

  // look at MemMsg in stdlib.ifcs for bit definition
  input  logic         memreq_rdy,
  output logic         memreq_en,
  output mem_req_4B_t  memreq_msg,

  output logic         memresp_rdy,
  input  logic         memresp_en,
  input  mem_resp_4B_t memresp_msg
);

  // ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Create RTL model for sorting xcel
  // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  // Accelerator ports and queues

  logic        xcelreq_deq_en;
  logic        xcelreq_deq_rdy;
  XcelReqMsg   xcelreq_deq_ret;

  vc_Queue#(`VC_QUEUE_PIPE,$bits(xcelreq_msg),1) xcelreq_q
  (
    .clk     (clk),
    .reset   (reset),
    .num_free_entries(),
    .enq_en  (xcelreq_en),
    .enq_rdy (xcelreq_rdy),
    .enq_msg (xcelreq_msg),
    .deq_en  (xcelreq_deq_en),
    .deq_rdy (xcelreq_deq_rdy),
    .deq_ret (xcelreq_deq_ret)
  );

  // Memory ports and queues

  logic           memresp_deq_en;
  logic           memresp_deq_rdy;
  mem_resp_4B_t   memresp_deq_ret;

  vc_Queue#(`VC_QUEUE_PIPE,$bits(memresp_msg),1) memresp_q
  (
    .clk     (clk),
    .reset   (reset),
    .num_free_entries(),
    .enq_en  (memresp_en),
    .enq_rdy (memresp_rdy),
    .enq_msg (memresp_msg),
    .deq_en  (memresp_deq_en),
    .deq_rdy (memresp_deq_rdy),
    .deq_ret (memresp_deq_ret)
  );

  // Extra state registers

  logic [31:0] base_addr,   base_addr_in;
  logic [31:0] size,        size_in;
  logic [31:0] inner_count, inner_count_in;
  logic [31:0] outer_count, outer_count_in;
  logic [31:0] a,           a_in;

  always_ff @(posedge clk) begin
    outer_count <= outer_count_in;
    inner_count <= inner_count_in;
    base_addr   <= base_addr_in;
    size        <= size_in;
    a           <= a_in;
  end

  //======================================================================
  // State Update
  //======================================================================

  typedef enum logic [$clog2(6)-1:0] {
    STATE_XCFG,
    STATE_FIRST0,
    STATE_FIRST1,
    STATE_BUBBLE0,
    STATE_BUBBLE1,
    STATE_LAST
  } state_t;

  state_t state_reg;

  logic go;

  always_ff @(posedge clk) begin

    if ( reset )
      state_reg <= STATE_XCFG;
    else begin
      state_reg <= state_reg;

      case ( state_reg )

        STATE_XCFG:
          if ( go && xcelresp_rdy )
            state_reg <= STATE_FIRST0;

        STATE_FIRST0:
          if ( memreq_rdy )
            state_reg <= STATE_FIRST1;

        STATE_FIRST1:
          if ( memreq_rdy && memresp_deq_rdy )
            state_reg <= STATE_BUBBLE0;

        STATE_BUBBLE0:
          if ( memreq_rdy && memresp_deq_rdy )
            state_reg <= STATE_BUBBLE1;

        STATE_BUBBLE1:
          if ( memreq_rdy && memresp_deq_rdy )
            if ( inner_count+1 < size )
              state_reg <= STATE_BUBBLE0;
            else
              state_reg <= STATE_LAST;

        STATE_LAST:
          if ( memreq_rdy && memresp_deq_rdy )
            if ( outer_count+1 < size )
              state_reg <= STATE_FIRST1;
            else
              state_reg <= STATE_XCFG;

        default:
          state_reg <= STATE_XCFG;

      endcase
    end
  end

  //======================================================================
  // State Outputs
  //======================================================================

  always_comb begin

    xcelreq_deq_en = 0;
    xcelresp_en    = 0;
    memreq_en  = 0;
    memresp_deq_en = 0;
    go             = 0;

    a_in = a;
    outer_count_in = outer_count;
    inner_count_in = inner_count;
    base_addr_in = base_addr;
    size_in = size;

    //--------------------------------------------------------------------
    // STATE: XCFG
    //--------------------------------------------------------------------

    if ( state_reg == STATE_XCFG ) begin

      if ( xcelreq_deq_rdy & xcelresp_rdy ) begin
        xcelreq_deq_en = 1;
        xcelresp_en    = 1;

        // Send xcel response message, obviously you only want to
        // send the response message when accelerator is done

        if ( xcelreq_deq_ret.type_ == `XcelReqMsg_TYPE_READ ) begin
          xcelresp_msg.type_ = `XcelRespMsg_TYPE_READ;
          xcelresp_msg.data  = 1;
        end
        else begin
          if ( xcelreq_deq_ret.addr == 0 ) begin
            outer_count_in = 0;
            inner_count_in = 0;
            go             = 1;
          end
          else if ( xcelreq_deq_ret.addr == 1 )
            base_addr_in = xcelreq_deq_ret.data;

          else if ( xcelreq_deq_ret.addr == 2 )
            size_in = xcelreq_deq_ret.data;

          xcelresp_msg.type_ = `XcelRespMsg_TYPE_WRITE;
          xcelresp_msg.data  = 0;
        end
      end
    end

    //--------------------------------------------------------------------
    // STATE: FIRST0
    //--------------------------------------------------------------------
    // Send the first memory read request for the very first element in
    // the array.

    else if ( state_reg == STATE_FIRST0 ) begin
      if ( memreq_rdy ) begin
        memreq_en        = 1;

        memreq_msg.type_ = `VC_MEM_REQ_MSG_TYPE_READ;
        memreq_msg.addr  = base_addr + (inner_count << 2);
        memreq_msg.len   = 0;
        memreq_msg.data  = 0;

        inner_count_in = 1;

      end
    end

    //--------------------------------------------------------------------
    // STATE: FIRST1
    //--------------------------------------------------------------------
    // Wait for the memory response for the first element in the array,
    // and once it arrives store this element in a, and send the memory
    // read request for the second element.

    else if ( state_reg == STATE_FIRST1 ) begin

      if ( memreq_rdy && memresp_deq_rdy ) begin
        memresp_deq_en = 1;
        memreq_en      = 1;

        a_in = memresp_deq_ret.data;

        memreq_msg.type_ = `VC_MEM_REQ_MSG_TYPE_READ;
        memreq_msg.addr  = base_addr + (inner_count << 2);
        memreq_msg.len   = 0;
        memreq_msg.data  = 0;

      end
    end

    //--------------------------------------------------------------------
    // STATE: BUBBLE0
    //--------------------------------------------------------------------
    // Wait for the memory read response to get the next element, compare
    // the new value to the previous max value, update b with the new max
    // value, and send a memory request to store the new min value.
    // Notice how we decrement the write address by four since we want to
    // store to the new min value _previous_ element.

    else if ( state_reg == STATE_BUBBLE0 ) begin
      if ( memreq_rdy && memresp_deq_rdy ) begin
        memresp_deq_en = 1;
        memreq_en      = 1;

        if ( a > memresp_deq_ret.data ) begin
          a_in = a;
          memreq_msg.data = memresp_deq_ret.data;
        end
        else begin
          a_in = memresp_deq_ret.data;
          memreq_msg.data = a;
        end

        memreq_msg.type_ = `VC_MEM_REQ_MSG_TYPE_WRITE;
        memreq_msg.addr  = base_addr + ((inner_count-1) << 2);
        memreq_msg.len   = 0;

      end
    end

    //--------------------------------------------------------------------
    // STATE: BUBBLE1
    //--------------------------------------------------------------------
    // Wait for the memory write response, and then check to see if we
    // have reached the end of the array. If we have not reached the end
    // of the array, then make a new memory read request for the next
    // element; if we have reached the end of the array, then make a
    // final write request (with value from a) to update the final
    // element in the array.

    else if ( state_reg == STATE_BUBBLE1 ) begin
      if ( memreq_rdy && memresp_deq_rdy ) begin
        memresp_deq_en = 1;
        memreq_en      = 1;

        inner_count_in = inner_count + 1;
        if ( inner_count+1 < size ) begin

          memreq_msg.type_ = `VC_MEM_REQ_MSG_TYPE_READ;
          memreq_msg.addr  = base_addr + ((inner_count+1) << 2);
          memreq_msg.len   = 0;
          memreq_msg.data  = 0;

        end
        else begin

          memreq_msg.type_ = `VC_MEM_REQ_MSG_TYPE_WRITE;
          memreq_msg.addr  = base_addr + (inner_count << 2);
          memreq_msg.len   = 0;
          memreq_msg.data  = a;

        end

      end
    end

    //--------------------------------------------------------------------
    // STATE: LAST
    //--------------------------------------------------------------------
    // Wait for the last response, and then check to see if we need to go
    // through the array again. If we do need to go through array again,
    // then make a new memory read request for the very first element in
    // the array; if we do not need to go through the array again, then
    // we are all done and we can go back to accelerator configuration.

    else if ( state_reg == STATE_LAST ) begin
      if ( memreq_rdy && memresp_deq_rdy ) begin
        memresp_deq_en = 1;

        outer_count_in = outer_count + 1;
        if ( outer_count+1 < size ) begin

          memreq_en        = 1;
          memreq_msg.type_ = `VC_MEM_REQ_MSG_TYPE_READ;
          memreq_msg.addr  = base_addr;
          memreq_msg.len   = 0;
          memreq_msg.data  = 0;

          inner_count_in       = 1;

        end

      end

    end

  end

  // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\

  //----------------------------------------------------------------------
  // Line Tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    vc_trace.append_str( trace_str, "(" );

    // ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Define line trace here
    // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

    $sformat( str, "%x", outer_count );
    vc_trace.append_str( trace_str, str );
    vc_trace.append_str( trace_str, ":" );

    $sformat( str, "%x", inner_count );
    vc_trace.append_str( trace_str, str );
    vc_trace.append_str( trace_str, ":" );

    case ( state_reg )
      STATE_XCFG:      vc_trace.append_str( trace_str, "X " );
      STATE_FIRST0:    vc_trace.append_str( trace_str, "F0" );
      STATE_FIRST1:    vc_trace.append_str( trace_str, "F1" );
      STATE_BUBBLE0:   vc_trace.append_str( trace_str, "B0" );
      STATE_BUBBLE1:   vc_trace.append_str( trace_str, "B1" );
      STATE_LAST:      vc_trace.append_str( trace_str, "L " );
      default:         vc_trace.append_str( trace_str, "? " );
    endcase

    // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\

    vc_trace.append_str( trace_str, ")" );

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* LAB2_XCEL_SORT_XCEL_V */

