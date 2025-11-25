`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/01/2025 02:20:34 PM
// Design Name: 
// Module Name: edge_counter
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


module edge_counter(
    input  wire clk,         // free-running sim clock (or FPGA clock later)
    input  wire rst_n,       // active-low reset
    input  wire cmp_out,
    output reg  [15:0] count
);
    reg cmp_d;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count <= 16'd0;
            cmp_d <= 1'b0;
        end else begin
            cmp_d <= cmp_out;
            if (cmp_out & ~cmp_d)  // rising edge
                count <= count + 16'd1;
        end
    end
endmodule
