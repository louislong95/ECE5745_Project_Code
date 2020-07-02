
`ifndef OPTICAL_FLOW_PROJECT
`define OPTICAL_FLOW_PROJECT

`include "vc/trace.v"

`include "vc/mem-msgs.v"
`include "vc/queues.v"
`include "proc/XcelMsg.v"

`include "submodule/GradientVRTL.v"
`include "final_project/matrix_operaVRTL.v"

//=========================================================================
// Optical flow Accelerator Implementation
//=========================================================================

module Final_Project_Optical_flowVRTL
#(
  parameter image_column = 128,
  parameter image_row    = 96,
  parameter window_size  = 3,
  parameter window_size_ext = 5
)(
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

  logic           xcelreq_deq_en;
  logic           xcelreq_deq_rdy;
  XcelReqMsg      xcelreq_deq_ret;


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

  // =====================logic definition================
  logic go;
  // -------------address of inputted array-------------
  logic [31:0] base_image;
  logic [31:0] image_num,     corner_num;   // these are the inputted constant, not addr
  logic [31:0] base_corner_x, base_corner_y;
  logic [31:0] base_vx,       base_vy,   base_de;

  // ---------------internal flag signals-------------------
  logic x_sent_in         , x_sent;
  logic y_sent_in         , y_sent;
  logic x_done_in         , x_done;
  logic y_done_in         , y_done;
  logic current_im_done_in, current_im_done;
  logic next_im_done_in   , next_im_done;
  logic vx_done_in, vx_done;
  logic vy_done_in, vy_done;
  logic de_done_in, de_done;
  logic xcel_go;

  // ---------------internal counter signals----------------
  logic [31:0] image_counter_in,  image_counter;
  logic [31:0] corner_counter_in, corner_counter;
  logic [31:0] row_counter_in, row_counter;
  logic [31:0] column_counter_in, column_counter;

  // --------------internal FSM registers --------------------
  logic [31:0] corner_x;
  logic [31:0] corner_y;
  logic [31:0] current_im_addr;
  logic [31:0] next_im_addr;

  // ---------------submodule logic signals-----------------
  logic [31:0] window_pixel_current [0:window_size_ext*window_size_ext-1];
  logic [31:0] window_pixel_next    [0:window_size_ext*window_size_ext-1];
  logic [31:0] Ix                   [0:window_size*window_size-1];
  logic [31:0] Iy                   [0:window_size*window_size-1];
  logic [31:0] It                   [0:window_size*window_size-1];
  logic signed [31:0]  vx;
  logic signed [31:0]  vy;
  logic signed [31:0]  vx_result_in, vx_result;
  logic signed [31:0]  vy_result_in, vy_result;
  logic signed [31:0]  de_result_in, de_result;
  logic signed [31:0]  determinant;
  logic valid;
  logic gradient_en;
  logic result_ok;

  // =====================================================

  logic [31:0] read_window_address;  // for test
  logic [31:0] write_mem_addr;    // for test

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

  GradientVRTL#(window_size) Gradient
  (
     .en(gradient_en),
     .current_frame(window_pixel_current),
     .next_frame(window_pixel_next),
     .Ix(Ix),
     .Iy(Iy),
     .It(It),
     .valid(valid)
  );

  matrix_operaVRTL#() matrix_operation
  (
     .clk(clk),
     .reset(reset),
     .req_go(valid),
     .in_x(Ix),
     .in_y(Iy),
     .in_t(It),
     .vx(vx),
     .vy(vy),
     .de(determinant),
     .result_ok(result_ok)
   );

  always_ff @(posedge clk) begin

    image_counter   <= image_counter_in;
    corner_counter  <= corner_counter_in;
    row_counter     <= row_counter_in;
    column_counter  <= column_counter_in;

    x_sent          <= x_sent_in;
    y_sent          <= y_sent_in;
    x_done          <= x_done_in;
    y_done          <= y_done_in;
    vx_done         <= vx_done_in;
    vy_done         <= vy_done_in;
    de_done         <= de_done_in;
    current_im_done <= current_im_done_in;
    next_im_done    <= next_im_done_in;
    current_im_done <= current_im_done_in;
    next_im_done    <= next_im_done_in;

    vx_result       <= vx_result_in;
    vy_result       <= vy_result_in;
    de_result       <= de_result_in;
		

  end

  typedef enum logic [$clog2(6)-1:0] {
    STATE_XCFG,
    STATE_CAL_IMAGE, // read one image
    STATE_M_RD_CORNER_COORDINATE, // deq mem_resp, update counter, send the window pixel
    STATE_M_RD_WINDOW,
    STATE_M_DEQ_WINDOW,
    STATE_XCEL_GO,
    STATE_M_WR,
    STATE_WAIT

  } state_t;

  state_t state_reg;


  // =====================State Transition================
  always_ff @(posedge clk) begin

    if ( reset )
      state_reg <= STATE_XCFG;
    else begin
      state_reg <= state_reg;

      case ( state_reg )

        STATE_XCFG:
          if ( go && xcelresp_en && xcelresp_rdy )
            state_reg <= STATE_CAL_IMAGE;
          else
            state_reg <= STATE_XCFG;

        STATE_CAL_IMAGE:  // calculate the base address of current and next image, and read in the image
            state_reg <= STATE_M_RD_CORNER_COORDINATE;

        STATE_M_RD_CORNER_COORDINATE: // read in the coordinate of the corner and calculate the base address of the window, then load the window (3 * 3)
          if ( x_done_in && y_done_in && memresp_deq_rdy )
             state_reg <= STATE_M_RD_WINDOW;
          else
             state_reg <= STATE_M_RD_CORNER_COORDINATE;

        STATE_M_RD_WINDOW:
          if ( memreq_rdy ) begin
             state_reg <= STATE_M_DEQ_WINDOW;
          end
          else begin
             state_reg <= STATE_M_RD_WINDOW;
          end

        STATE_M_DEQ_WINDOW:
          if ( xcel_go && current_im_done_in && next_im_done_in && memresp_deq_rdy) begin
             state_reg <= STATE_XCEL_GO;
          end
          else if (!memresp_deq_rdy) begin
             state_reg <= STATE_M_DEQ_WINDOW;
          end
          else begin
             state_reg <= STATE_M_RD_WINDOW;
          end

        STATE_XCEL_GO:     // open the enable signal and wait for the result_ok signal
          if ( result_ok ) begin
             state_reg <= STATE_M_WR;
          end
          else begin
             state_reg <= STATE_XCEL_GO;
          end

        STATE_M_WR:        // wirte the vx, vy and determinant of one corner
          if ( memreq_rdy ) begin
             state_reg <= STATE_WAIT;
          end
          else begin
             state_reg <= STATE_M_WR;
          end

        STATE_WAIT:        // wait until the memory is writen, check the image counter and corner counter
          if (vx_done_in && vy_done_in && de_done_in && corner_counter < (corner_num - 1)) begin   // if vx, vy, determinant of one conrer are already writen into the memory, and the corner counter is less than the corner number in the current frame, it will transfer back again to the read corner coordinate state
             state_reg <= STATE_M_RD_CORNER_COORDINATE;
          end
          else if (vx_done_in && vy_done_in && de_done_in && (corner_counter == (corner_num - 1)) && (image_counter < (image_num - 1))) begin
             state_reg <= STATE_CAL_IMAGE; // if vx, vy, determinant of one conrer are already writen into the memory, and the corner counter euqals the corner number in the current frame, but the image counter less than the image number, it will transfer back again to the read image state
          end
          else if (vx_done_in && vy_done_in && de_done_in && (corner_counter == (corner_num - 1)) && (image_counter == (image_num - 1))) begin
             state_reg <= STATE_XCFG;      // if vx, vy, determinant of one conrer are already writen into the memory, the corner counter euqals the corner number in the current frame, the image counter equals the image number, it will transfer to the initial state to wait for another accelerator enable signal
          end
          else if (!memresp_deq_rdy) begin
             state_reg <= STATE_WAIT;
          end
          else if (!de_done_in) begin
             state_reg <= STATE_M_WR;
          end

          default:
             state_reg <= STATE_XCFG;
      endcase
    end
  end
// =================================================


// ====================state output===================
  always_comb begin

    go                  = 0;
    xcelreq_deq_en      = 0;
    xcelresp_en         = 0;
    memreq_en           = 0;
    memresp_deq_en      = 0;

    //--------------------------------------------------------------------
    // STATE: XCFG
    //--------------------------------------------------------------------
    // In this state we handle the accelerator configuration protocol,
    // where we write the base addresses, size, and then tell the
    // accelerator to start. We also handle responding when the
    // accelerator is done.

    if ( state_reg == STATE_XCFG ) begin

      image_counter_in   = 0;
      corner_counter_in  = 0;
      x_done_in          = 0;
      y_done_in          = 0;
      x_sent_in          = 0;
      y_sent_in          = 0;
      current_im_done_in = 0;
      next_im_done_in    = 0;
      row_counter_in     = 0;
      column_counter_in  = 0;
      gradient_en        = 0;
      vx_done_in = 0;
      vy_done_in = 0;
      de_done_in = 0;

      if ( xcelreq_deq_rdy & xcelresp_rdy ) begin  // when queue prepare to send data to consumer, and core is ready to receive the data
        xcelreq_deq_en = 1;                        // de-queue signal assertion
        xcelresp_en    = 1;                        // assert the resp enable, send data back to core

        if ( xcelreq_deq_ret.type_ == `XcelReqMsg_TYPE_READ ) begin   // if it is read
          xcelresp_msg.type_ = `XcelRespMsg_TYPE_READ;
          xcelresp_msg.data  = 1;
        end

        else begin
        // if it is write
          if ( xcelreq_deq_ret.addr == 0 ) begin  // if it is write to xr0
            go             = 1;                   // start xcel
          end

          else if ( xcelreq_deq_ret.addr == 1 ) begin  // write to xr1, wirte the image base address
            base_image = xcelreq_deq_ret.data;  // src0 -> xr1
          end

          else if ( xcelreq_deq_ret.addr == 2 ) begin  // write to xr1, wirte the image number
            image_num = xcelreq_deq_ret.data;  // src0 -> xr2
          end

          else if ( xcelreq_deq_ret.addr == 3 ) begin   // write to xr2, write the address of the corner number array
            corner_num = xcelreq_deq_ret.data;  // base_corner_num -> xr3
          end

          else if ( xcelreq_deq_ret.addr == 4 ) begin   // write to xr3, write the corner_x
            base_corner_x = xcelreq_deq_ret.data;  // base_corner_x_in -> xr4
          end

          else if ( xcelreq_deq_ret.addr == 5 ) begin   // write to xr4, write the corner_y
            base_corner_y = xcelreq_deq_ret.data;  // base_corner_x_in -> xr5
          end

          else if ( xcelreq_deq_ret.addr == 6 ) begin // write the base address of the result Vx
            base_vx       = xcelreq_deq_ret.data;
          end

          else if ( xcelreq_deq_ret.addr == 7 ) begin // write the base address of the result Vy
            base_vy       = xcelreq_deq_ret.data;
          end

          else if ( xcelreq_deq_ret.addr == 8 ) begin // write the base address of the result determinant
            base_de       = xcelreq_deq_ret.data;
          end

          xcelresp_msg.type_ = `XcelRespMsg_TYPE_WRITE;  // send the ack to the core
          xcelresp_msg.data  = 0;                 // send back 0, please see the test
        end
      end

    end

    //--------------------------------------------------------------------
    // STATE: M_RD
    //--------------------------------------------------------------------
    else if ( state_reg == STATE_CAL_IMAGE ) begin  // Calculate the base adress of the current frame and the next frame

      gradient_en = 0;
      vx_done_in = 0;
      vy_done_in = 0;
      de_done_in = 0;

      current_im_addr = base_image + image_counter       * image_column * image_row * 4;
      next_im_addr    = base_image + (image_counter + 1) * image_column * image_row * 4;

    end



    //--------------------------------------------------------------------
    // STATE: RD_CORNER_COORDINATE
    //--------------------------------------------------------------------

    else if (state_reg == STATE_M_RD_CORNER_COORDINATE) begin // Send the base address of the array that holds the corner point coordinates, and read in the corner point coordinates

      gradient_en = 0;
      vx_done_in = 0;
      vy_done_in = 0;
      de_done_in = 0;
      xcel_go = 0;

      if ( memreq_rdy && (!x_sent || !y_sent) )  begin                  // if memory is ready to receive message

        memreq_en = 1;                     // build the communication between memory
        memreq_msg.type_ = `VC_MEM_REQ_MSG_TYPE_READ;    // type is 'read'
        if (!x_sent && !y_sent ) begin  // x_done, y_done
          memreq_msg.addr = base_corner_x + (image_counter * corner_num + corner_counter) * 4;
          x_sent_in       = 1;
          y_sent_in       = 0;
        end
        else if (!y_sent && x_sent) begin
          memreq_msg.addr = base_corner_y + (image_counter * corner_num + corner_counter) * 4;
          y_sent_in       = 1;
          x_sent_in       = 1;
        end
        else begin
          x_sent_in = x_sent;
          y_sent_in = y_sent;
        end
        memreq_msg.len = 0;
      end
      else begin
        x_sent_in = x_sent;
        y_sent_in = y_sent; 
      end

      if (memresp_deq_rdy) begin // Wait for the memory to send back the corner coordinates

         memresp_deq_en = 1;
         if (!x_done) begin
            corner_x  = memresp_deq_ret.data - 1;
            x_done_in = 1;
         end
         else if (!y_done) begin
            corner_y  = memresp_deq_ret.data - 1;
            y_done_in = 1;
         end
      end
      else begin
         corner_counter_in = corner_counter;
      end

    end

    //--------------------------------------------------------------------
    // STATE: STATE_M_RD_WINDO
    //--------------------------------------------------------------------

    else if ( state_reg == STATE_M_RD_WINDOW ) begin // Send the base address of the window (5 * 5) that centers at the corner point (including the window in the current frame and the next frame)

      x_done_in = 0; 
      y_done_in = 0;
      x_sent_in = 0;
      y_sent_in = 0;
      gradient_en = 0; 

      if ( memreq_rdy && (!current_im_done || !next_im_done) )                    // if memory is ready to receive message
      begin

        memreq_en = 1;                     // build the communication between memory
        memreq_msg.type_ = `VC_MEM_REQ_MSG_TYPE_READ;    // type is 'read'
        if ( !current_im_done ) begin
          memreq_msg.addr = current_im_addr + (image_column * (corner_y - 2) + (corner_x - 2) + row_counter * image_column + column_counter) * 4;
          read_window_address = memreq_msg.addr;
        end
        else if ( !next_im_done ) begin
          memreq_msg.addr = next_im_addr    + (image_column * (corner_y - 2) + (corner_x - 2) + row_counter * image_column + column_counter) * 4;
        end

        memreq_msg.len = 0;
      end

    end
    
    // Memory responses
    else if ( state_reg == STATE_M_DEQ_WINDOW ) begin // Get the window pixels back from the memory, including the window pixels of both the window from the current image frame and the next image frame

      gradient_en = 0;

      if ( memresp_deq_rdy )
      begin
        memresp_deq_en = 1;

        if (!current_im_done) begin
           window_pixel_current[row_counter * window_size_ext + column_counter] = memresp_deq_ret.data;
        end
        else if (!next_im_done) begin
           window_pixel_next[row_counter * window_size_ext + column_counter] = memresp_deq_ret.data;
        end
        
        // Here we implement row counter and column counter to control the memory to sedn back 25 pixels back to the accelerator
        if ( row_counter < 5 ) begin
          if ( column_counter < 4 ) begin
            column_counter_in = column_counter + 1;
          end
          else begin
            column_counter_in = 0;
            row_counter_in = row_counter + 1;
          end
        end
        else begin
          row_counter_in    = 0;
          column_counter_in = 0;
          if (!current_im_done) begin
             current_im_done_in = 1;
          end
          else if (!next_im_done) begin
             next_im_done_in    = 1;
          end  
        end

        if ( (row_counter == 5) && current_im_done && next_im_done_in ) begin
          xcel_go = 1; // start the xcel
        end

      end
    
    end

    //--------------------------------------------------------------------
    // STATE: Accelerator start state, the enable signal will be send to the calculation module of the accelerator
    //--------------------------------------------------------------------

    else if ( state_reg == STATE_XCEL_GO ) begin
        current_im_done_in = 0;
        next_im_done_in    = 0;
        row_counter_in     = 0;
        column_counter_in  = 0;

        gradient_en = 1;                     // enable the xcel, connect to the Ix, Iy, It unit
        
        if (result_ok) begin
           vx_result_in = vx;
           vy_result_in = vy;
           de_result_in = determinant;
        end
        

     end

    //--------------------------------------------------------------------
    // STATE: M_WR Send the base address of the result (Vx, Vy, determinant) and the results (Vx, Vy, determinant) to the memory 
    //--------------------------------------------------------------------

    else if ( state_reg == STATE_M_WR ) begin
      gradient_en = 0;                       // disable the xcel unit
      xcel_go     = 0;

      if ( memreq_rdy ) begin           // if the memory is ready to receive the message
        memreq_en           = 1;
        memreq_msg.type_    = `VC_MEM_REQ_MSG_TYPE_WRITE;    // type is write
        memreq_msg.len      = 0;
        if (!vx_done) begin
           memreq_msg.addr  = base_vx + (image_counter * corner_num + corner_counter) * 4;     // select Vx, Vy, determinant , if not vx_done, that means vx has not been sent back to the memory
           write_mem_addr   = memreq_msg.addr;
           memreq_msg.data  = vx;
        end
        else if (!vy_done) begin
           memreq_msg.addr  = base_vy + (image_counter * corner_num + corner_counter) * 4;     // if not vy_done, that means vx has been sent back to memory, vy has not been sent back to the memory, so this time will send vy back to memory
           write_mem_addr   = memreq_msg.addr;
           memreq_msg.data  = vy;
        end
        else if (!de_done) begin
           memreq_msg.addr  = base_de + (image_counter * corner_num + corner_counter) * 4;     // if not de_done, that means vx and vy have been sent back to memory, de has not been sent back to the memory, so this time will send de back to memory
           write_mem_addr   = memreq_msg.addr;
           memreq_msg.data  = determinant;
        end
      end
    end

    //--------------------------------------------------------------------
    // STATE: WAIT, Wait for the memory to finish receiving the result data
    //--------------------------------------------------------------------

    else if ( state_reg == STATE_WAIT ) begin
      gradient_en              = 0;    // disable the xcel

      if ( memresp_deq_rdy ) begin
        memresp_deq_en = 1;

        if (!vx_done) begin
           vx_done_in = 1;
        end
        else if (!vy_done) begin
           vy_done_in = 1;
        end
        else if (!de_done) begin
           de_done_in = 1;
        end
      end

      if (vx_done_in && vy_done_in && de_done_in && (corner_counter < (corner_num - 1))) begin
         corner_counter_in = corner_counter + 1;
      end
      else if (vx_done_in && vy_done_in && de_done_in && (corner_counter == (corner_num - 1))) begin
         corner_counter_in = 0;
         image_counter_in  = image_counter + 1;
      end

    end


  end

  //======================================================================
  // Line Tracing
  //======================================================================

  `ifndef SYNTHESIS

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin
    $sformat( str, "xr%2x = %x", xcelreq_msg.addr, xcelreq_msg.data );
    vc_trace.append_en_rdy_str( trace_str, xcelreq_en, xcelreq_rdy, str );

    vc_trace.append_str( trace_str, "(" );

    case ( state_reg )
      STATE_XCFG     :                     vc_trace.append_str( trace_str, "X " );
      STATE_CAL_IMAGE:                     vc_trace.append_str( trace_str, "CA " );
      STATE_M_RD_CORNER_COORDINATE:        vc_trace.append_str( trace_str, "RC " );
      STATE_M_RD_WINDOW:                   vc_trace.append_str( trace_str, "RW " );
      STATE_M_DEQ_WINDOW:                  vc_trace.append_str( trace_str, "DW " );
      STATE_XCEL_GO:                       vc_trace.append_str( trace_str, "Go " );
      STATE_M_WR:                          vc_trace.append_str( trace_str, "WR " );
      STATE_WAIT:                          vc_trace.append_str( trace_str, "WA " );
      default:                             vc_trace.append_str( trace_str, "? " );
    endcase
    vc_trace.append_str( trace_str, " " );

    $sformat( str, "%x", state_reg );
    vc_trace.append_str( trace_str, str );
    vc_trace.append_str( trace_str, " " );

    $sformat( str, "%x", image_counter );
    vc_trace.append_str( trace_str, str );
    vc_trace.append_str( trace_str, " " );

    $sformat( str, "%x", corner_counter );
    vc_trace.append_str( trace_str, str );
    vc_trace.append_str( trace_str, " " );

    $sformat( str, "%x", corner_x );
    vc_trace.append_str( trace_str, str );
    vc_trace.append_str( trace_str, " " );

    $sformat( str, "%x", corner_y );
    vc_trace.append_str( trace_str, str );
    vc_trace.append_str( trace_str, " " );

    $sformat( str, "%x", gradient_en );
    vc_trace.append_str( trace_str, str );
    vc_trace.append_str( trace_str, " " );

    $sformat( str, "%x", result_ok );
    vc_trace.append_str( trace_str, str );
    vc_trace.append_str( trace_str, " " );

    $sformat( str, "%x", vx );
    vc_trace.append_str( trace_str, str );
    vc_trace.append_str( trace_str, " " );

    $sformat( str, "%x", vy );
    vc_trace.append_str( trace_str, str );
    vc_trace.append_str( trace_str, " " );

    $sformat( str, "%x", determinant );
    vc_trace.append_str( trace_str, str );
    vc_trace.append_str( trace_str, " " );

    vc_trace.append_str( trace_str, ")" );

    $sformat( str, "%x", memreq_msg.data );
    vc_trace.append_en_rdy_str( trace_str, memreq_en, memreq_rdy, str );

    vc_trace.append_str( trace_str, "||" );

    $sformat( str, "%x", memreq_msg.data );
    vc_trace.append_en_rdy_str( trace_str, memreq_en, memreq_rdy, str );

    vc_trace.append_str( trace_str, "::" );

    $sformat( str, "%x", xcelresp_msg.data );
    vc_trace.append_en_rdy_str( trace_str, xcelresp_en, xcelresp_rdy, str );

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif
