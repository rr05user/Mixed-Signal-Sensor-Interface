`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/22/2025 04:23:31 PM
// Design Name: 
// Module Name: uart_tx_tb
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


`timescale 1ns / 1ps



module uart_tx_tb;

  reg clk = 0;
  reg rst = 1;
  reg tx_start = 0;
  reg [7:0] tx_data = 8'hA5;
  wire tx;
  wire busy;

  always #50 clk = ~clk;  // 10 MHz clock

  uart_tx #(
    .CLK_HZ(10_000_000),
    .BAUD(115200)
  ) dut (
    .clk(clk),
    .rst(rst),
    .tx_start(tx_start),
    .tx_data(tx_data),
    .tx(tx),
    .busy(busy)
  );

  initial begin
    #200 rst = 0;
    #300;

    // start transmit pulse
    tx_start = 1;
    #100;
    tx_start = 0;

    #2000000;
    $finish;
  end

endmodule
