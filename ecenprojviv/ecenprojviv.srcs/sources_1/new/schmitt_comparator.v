`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/01/2025 01:38:36 PM
// Design Name: 
// Module Name: schmitt_comparator
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


module schmitt_comparator(
    input  wire [11:0] vin,   // simulated ADC input (0-4095 ? 0-3.3V)
    output reg  vout
);
    // Define high/low thresholds (1.20V ± 0.02V ? 1486 ± 25 counts)
    parameter HIGH_TH = 12'd1510; // ? 1.22 V
    parameter LOW_TH  = 12'd1460; // ? 1.18 V

    always @(*) begin
        if (vin >= HIGH_TH)
            vout = 1'b1;
        else if (vin <= LOW_TH)
            vout = 1'b0;
        // retains last value when vin is between thresholds (hysteresis)
    end
endmodule
