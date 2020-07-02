`ifndef MATRIX_OPERATION_V
`define MATRIX_OPERATION_V

`include "vc/regs.v"
`include "vc/muxes.v"
`include "vc/trace.v"


module matrix_operaRTL_datapath
(
  input   logic                    clk,
  input   logic                    reset,
  input   logic   signed  [31:0]  in_x [0:8],
  input   logic   signed  [31:0]  in_y [0:8],
  input   logic   signed  [31:0]  in_t [0:8],
  input   logic   stage2_sel,
  input   logic   stage2_reg_reset,
  input   logic   stage2_reg_en,
  input   logic   stage3_reg_reset,
  input   logic   stage3_reg_en,
  input   logic   result_ok,
  input   logic           [3:0]    initial_mux_sel,
  output  logic   signed  [31:0]   vx,
  output  logic   signed  [31:0]   vy,
  output  logic   signed  [31:0]   de
  );

  logic signed [31:0]   in_x_out;
  logic signed [31:0]   in_y_out;
  logic signed [31:0]   in_t_out;
  logic signed [31:0]   stage2_in_x;
  logic signed [31:0]   stage2_in_y;
  logic signed [31:0]   stage2_in_t;
  logic signed [31:0]   stage2_add_in       [0:4];
  logic signed [31:0]   stage2_add_out      [0:4];
  logic signed [31:0]   stage2_reg_out      [4:0];
  logic signed [31:0]   stage2_mux_out      [0:4];
  logic signed [31:0]   stage3_reg_out      [0:4];

  vc_Mux10#(32)  initial_mux_x
  (
    .in0(32'd0  ),
    .in1(in_x[0]),
    .in2(in_x[1]),
    .in3(in_x[2]),
    .in4(in_x[3]),
    .in5(in_x[4]),
    .in6(in_x[5]),
    .in7(in_x[6]),
    .in8(in_x[7]),
    .in9(in_x[8]),
    .sel(initial_mux_sel),
    .out(in_x_out)
    );

  vc_Mux10#(32)  initial_mux_y
  (
    .in0(32'd0  ),
    .in1(in_y[0]),
    .in2(in_y[1]),
    .in3(in_y[2]),
    .in4(in_y[3]),
    .in5(in_y[4]),
    .in6(in_y[5]),
    .in7(in_y[6]),
    .in8(in_y[7]),
    .in9(in_y[8]),
    .sel(initial_mux_sel),
    .out(in_y_out)
    );

  vc_Mux10#(32)  initial_mux_t
  (
    .in0(32'd0  ),
    .in1(in_t[0]),
    .in2(in_t[1]),
    .in3(in_t[2]),
    .in4(in_t[3]),
    .in5(in_t[4]),
    .in6(in_t[5]),
    .in7(in_t[6]),
    .in8(in_t[7]),
    .in9(in_t[8]),
    .sel(initial_mux_sel),
    .out(in_t_out)
    );

  assign stage2_add_in[0]  = in_x_out * in_x_out;
  assign stage2_add_in[1]  = in_x_out * in_y_out;
  assign stage2_add_in[2]  = in_y_out * in_y_out;
  assign stage2_add_in[3]  = in_t_out * in_x_out;
  assign stage2_add_in[4]  = in_t_out * in_y_out;

  genvar i;
  generate

  for (i = 0; i< 5; i = i + 1) begin: cal_path

  vc_EnReg#(32) stage2_reg_x
  (
    .clk(clk),
    .reset(stage2_reg_reset),
    .en(stage2_reg_en),
    .q(stage2_reg_out[i]),
    .d(stage2_add_in[i])
    );

    assign stage2_add_out[i]  = stage2_reg_out[i] + stage2_mux_out[i];

    vc_Mux2#(32)  stage2_mux
    (
      .in0(32'd0),
      .in1(stage3_reg_out[i]),
      .sel(stage2_sel),
      .out(stage2_mux_out[i])
      );

    vc_EnReg#(32) stage3_reg
    (
      .clk(clk),
      .reset(stage3_reg_reset),
      .en(stage3_reg_en),
      .q(stage3_reg_out[i]),
      .d(stage2_add_out[i])
      );
    end
  endgenerate

    always_comb begin
      if (result_ok) begin
        vx = (stage3_reg_out[1] >>> 5) * (stage3_reg_out[4] >>> 5) - (stage3_reg_out[2] >>> 5) * (stage3_reg_out[3] >>> 5);
        vy = (stage3_reg_out[1] >>> 5) * (stage3_reg_out[3] >>> 5) - (stage3_reg_out[0] >>> 5) * (stage3_reg_out[4] >>> 5);
        de = (stage3_reg_out[0] >>> 5) * (stage3_reg_out[2] >>> 5) - (stage3_reg_out[1] >>> 5) * (stage3_reg_out[1] >>> 5);
      end
      else begin
        vx = vx;
        vy = vy;
        de = de;
      end
    end
endmodule

module matrix_operaRTL_control
(
  input   logic                   clk,
  input   logic                   reset,
  input   logic                   req_go,
  output  logic                   stage2_sel,
  output  logic                   stage2_reg_en,
  output  logic                   stage2_reg_reset,
  output  logic                   stage3_reg_reset,
  output  logic                   stage3_reg_en,
  output  logic                   result_ok,
  output  logic  [3:0]            initial_mux_sel
  );
  localparam  IDLE_STATE          = 2'b00;
  localparam  WRITE_STATE         = 2'b01;
  localparam  COMPONENT_SUM_STATE = 2'b10;
  localparam  FINAL_RESULT_STATE  = 2'b11;

  logic   [1:0]   current_state;
  logic   [1:0]   next_state;

  logic   [3:0]   cnt;

  always_ff @( posedge clk ) begin
    if ( reset ) begin
      current_state <= IDLE_STATE;
    end
    else begin
      current_state <= next_state;
    end
  end

  always_comb begin
    case (current_state)

      IDLE_STATE:
        if (req_go) begin
          next_state = WRITE_STATE;
        end
        else begin
          next_state = IDLE_STATE;
        end
      WRITE_STATE:
        next_state = COMPONENT_SUM_STATE;

      COMPONENT_SUM_STATE:
        if (cnt < 10)
          next_state = COMPONENT_SUM_STATE;
        else
          next_state = FINAL_RESULT_STATE;

      FINAL_RESULT_STATE:
        next_state = IDLE_STATE;

      default:
        next_state = IDLE_STATE;
    endcase
  end

  always_comb begin
    if(current_state == IDLE_STATE) begin
      result_ok = 0;
      stage2_reg_en           = 1;
      stage2_reg_reset        = 1;
      stage2_sel              = 0;
      stage3_reg_reset        = 1;
      stage3_reg_en           = 0;
    end
    else if (current_state == WRITE_STATE) begin
      stage2_reg_en           = 1;
      stage2_reg_reset        = 0;
      stage2_sel              = 1;
      stage3_reg_reset        = 0;
      stage3_reg_en           = 1;
    end
    else if (current_state == COMPONENT_SUM_STATE) begin
        stage2_reg_en          = 1;
        stage2_reg_reset       = 0;
        stage2_sel             = 1;
        stage3_reg_reset       = 0;
        stage3_reg_en          = 1;
    end
    else if (current_state == FINAL_RESULT_STATE) begin
      result_ok = 1;
      stage2_reg_en            = 1;
      stage2_reg_reset         = 0;
      stage2_sel               = 0;
      stage3_reg_reset         = 0;
      stage3_reg_en            = 1;
    end
  end

  always_ff @( posedge clk ) begin
    if(reset)
      cnt <= 0;
    else if( current_state == COMPONENT_SUM_STATE || current_state == WRITE_STATE) begin
      if (cnt == 4'd10)
        cnt <= 0;
      else
        cnt <= cnt + 4'd1;
    end
    else
        cnt <= cnt;
  end

  always_comb begin
    case (cnt)
      4'd0:
        initial_mux_sel = 4'd0;
      4'd1:
        initial_mux_sel = 4'd1;
      4'd2:
        initial_mux_sel = 4'd2;
      4'd3:
        initial_mux_sel = 4'd3;
      4'd4:
        initial_mux_sel = 4'd4;
      4'd5:
        initial_mux_sel = 4'd5;
      4'd6:
        initial_mux_sel = 4'd6;
      4'd7:
        initial_mux_sel = 4'd7;
      4'd8:
        initial_mux_sel = 4'd8;
      4'd9:
        initial_mux_sel = 4'd9;
      default:
        initial_mux_sel = 4'd0;
    endcase
  end

endmodule

module matrix_operaVRTL
(
  input   logic                   clk,
  input   logic                   reset,
  input   logic                   req_go,
  input   logic   signed  [31:0]  in_x [0:8],
  input   logic   signed  [31:0]  in_y [0:8],
  input   logic   signed  [31:0]  in_t [0:8],
  output  logic   signed  [31:0]  vx,
  output  logic   signed  [31:0]  vy,
  output  logic   signed  [31:0]  de,
  output  logic                   result_ok
);

  logic   stage2_sel;
  logic   stage2_reg_en;
  logic   stage2_reg_reset;
  logic   stage3_reg_reset;
  logic   stage3_reg_en;
  logic   [3:0]  initial_mux_sel;
  logic   result_ok_in;
  logic   signed  [31:0]   vx_out;
  logic   signed  [31:0]   vy_out;
  logic   signed  [31:0]   de_out;

  assign vx = vx_out;
  assign vy = vy_out;
  assign de = de_out;
  assign result_ok = result_ok_in;

  matrix_operaRTL_datapath datapath
  (
    .clk(clk),
    .reset(reset),
    .in_x(in_x),
    .in_y(in_y),
    .in_t(in_t),
    .stage2_sel(stage2_sel),
    .stage2_reg_en(stage2_reg_en),
    .stage2_reg_reset(stage2_reg_reset),
    .stage3_reg_reset(stage3_reg_reset),
    .stage3_reg_en(stage3_reg_en),
    .result_ok(result_ok_in),
    .initial_mux_sel(initial_mux_sel),
    .vx(vx_out),
    .vy(vy_out),
    .de(de_out)
    );
  matrix_operaRTL_control control
  (
    .clk(clk),
    .reset(reset),
    .req_go(req_go),
    .stage2_sel(stage2_sel),
    .stage2_reg_en(stage2_reg_en),
    .stage2_reg_reset(stage2_reg_reset),
    .stage3_reg_reset(stage3_reg_reset),
    .stage3_reg_en(stage3_reg_en),
    .result_ok(result_ok_in),
    .initial_mux_sel(initial_mux_sel)
    );

endmodule

`endif
