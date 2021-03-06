// This is a wrapper module that wraps PyMTL placeholder IxVRTL__size_3
// This file was generated by PyMTL VerilogPlaceholderPass
`ifndef IXVRTL_WRAPPER
`define IXVRTL_WRAPPER

`line 1 "submodule/IxVRTL.v" 0
//this is a module to calculate the Ix derivative 
module IxVRTL
	#(
      parameter size =3                      //This is the window size, the acually size for Ix will be 3*5
    )
    (
		//input  logic  [31:0] image_in  [0:14],     //need to figure out exact number
		input  logic  [31:0] image_in  [0:size*(size+2)-1],  
		output logic  [31:0] image_out [0:size*size-1]  
	);

always_comb begin
	//for (int i=0;i<3;i=i+1) begin
	for (int i=0;i<size;i=i+1)begin
		//for (int j=0;j<3;j=j+1)begin
		for (int j=0;j<size;j=j+1)begin
		//image_out[j+i*3]   =image_in[j+i*5+2]-image_in[j+i*5];
		image_out[j+i*size]=image_in[j+i*(size+2)+2]-image_in[j+(size+2)*i];
	    end
	end 
end
endmodule 
module IxVRTL_wrapper
(
  input logic reset,
  input logic clk,
  input logic [32-1:0] image_in [0:14],
  output logic [32-1:0] image_out [0:8]
);
  IxVRTL
  #(
    .size( 3 )
  ) v
  (
    .image_in( image_in ),
    .image_out( image_out )
  );
endmodule

`endif /* IXVRTL_WRAPPER */
