//this is a module to calculate the dradient with resoect to x,y and t
`include "submodule/IxVRTL.v"
`include "submodule/IyVRTL.v"
`include "submodule/ItVRTL.v"

module GradientVRTL
#(
  parameter side =3                      //This is the window side, the acually size for Ix will be 3*5
)
(
  input  logic  en,
  input  logic  [31:0] current_frame [0:(side+2)*(side+2)-1],
  input  logic  [31:0] next_frame    [0:(side+2)*(side+2)-1],
  output logic  [31:0] Ix [0:side*side-1],  
  output logic  [31:0] Iy [0:side*side-1], 
  output logic  [31:0] It [0:side*side-1],
  output logic  valid
);

IxVRTL#(side) Ix_module
(
  .image_in  (current_frame[ side+2 : side+2+side*(side+2)-1]),
  .image_out (Ix)
);

IyVRTL#(side) Iy_module
(
  .image_in (current_frame),
  .image_out(Iy)
);

ItVRTL#(side) It_module
(
  .current_frame(current_frame),
  .next_frame(next_frame),
  .out(It)
);

assign valid=en;

endmodule
