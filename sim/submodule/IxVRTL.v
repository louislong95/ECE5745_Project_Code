//this is a module to calculate the Ix derivative 
`include "vc/trace.v"

module IxVRTL
#(
  parameter side =3                      //This is the window size, the acually size for Ix will be 3*5
)
(
  input  logic  [31:0] image_in  [0:side*(side+2)-1],  
  output logic  [31:0] image_out [0:side*side-1]  
);

always_comb begin
  for (int i=0;i<side;i=i+1)begin
    for (int j=0;j<side;j=j+1)begin
      image_out[j+i*side]=image_in[j+i*(side+2)+2]-image_in[j+(side+2)*i];
    end
  end 
end
endmodule 