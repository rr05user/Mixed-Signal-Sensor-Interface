`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/01/2025 01:48:25 PM
// Design Name: 
// Module Name: sr_latch
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


// sr_latch.v
module sr_latch(
    input  wire set,
    input  wire reset,
    output reg  q
);
    always @(*) begin
        if (reset)
            q = 1'b0;
        else if (set)
            q = 1'b1;
    end
endmodule

