//This is a module to calculate Iy derivative
`include "vc/trace.v"

module IyVRTL
#(
  parameter side =3
)
(
  input  logic [31:0] image_in  [0:(side+2)*(side+2)-1],
  output logic [31:0] image_out [0:side*side-1]
);
localparam width= side+2;

always_comb begin
  for (int i=0;i<side;i=i+1)begin
    for (int j=0;j<side;j=j+1)begin
      image_out[i*side+j]= image_in[(i+2)*width+j+1]-image_in[i*width+j+1];
    end
  end
end
endmodule 