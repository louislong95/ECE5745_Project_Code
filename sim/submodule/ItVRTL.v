//this is a module to calculate the It derivative
//frame at T+1 minus T 
`include "vc/trace.v"

module ItVRTL
#(
  parameter side =3                      //This is the window size, the acually size for Ix will be 3*5
)
(
  input  logic  [31:0] current_frame [0:(side+2)*(side+2)-1],
  input  logic  [31:0] next_frame    [0:(side+2)*(side+2)-1], 
  output logic  [31:0] out [0:side*side-1]  
);

localparam width=side+2;

always_comb begin
  for (int i=0;i<side;i=i+1)begin
    for (int j=0;j<side;j=j+1)begin
      out[i*side+j]  = next_frame[(i+1)*width+j+1] - current_frame[(i+1)*width+j+1];
      //image_out[i*side+j]= image_in[(i+2)*width+j+1]-image_in[i*width+j+1];
    end
  end 
end
endmodule 