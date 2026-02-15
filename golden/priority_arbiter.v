// Priority arbiter
// port[0] - highest priority

`timescale 1ns/1ps
module priority_arbiter (
    input  wire         clk_i,
    input  wire         rstn_i,
    input  wire [4-1:0] req_i,
    output wire [4-1:0] gnt_o   // One-hot grant signal
);

  wire [4-1 : 0] gnt_w ;
  reg  [4-1 : 0] gnt_r ;

  //register assignment
  always@(posedge clk_i or negedge rstn_i) begin
    if(!rstn_i) begin
      gnt_r <= 4'b0000 ;
    end
    else begin
      gnt_r <= gnt_w   ;
    end
  end


  //logic 
  assign gnt_w[0] = req_i[0];
  genvar i;
  for (i=1; i<4; i=i+1) begin
    assign gnt_w[i] = req_i[i] & ~(|gnt_w[i-1:0]);
  end

  //output assignment
  assign gnt_o = gnt_r ;

endmodule