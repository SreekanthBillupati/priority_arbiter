`timescale 1ns/1ps
module priority_arbiter (
    input  wire         clk_i,
    input  wire         rstn_i,
    input  wire [4-1:0] req_i,
    output wire [4-1:0] gnt_o   // One-hot grant signal
);

  //internal logic
  //output assignment
  assign gnt_o = 4'd0000 ;

endmodule