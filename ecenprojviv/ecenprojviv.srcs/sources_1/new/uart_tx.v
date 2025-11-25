// uart_tx.v - Correct 8N1 UART (start bit first, LSB first)
`timescale 1ns / 1ps

module uart_tx #(
    parameter CLK_HZ = 10_000_000,
    parameter BAUD   = 115200
)(
    input  wire clk,
    input  wire rst,
    input  wire tx_start,
    input  wire [7:0] tx_data,
    output reg  tx,
    output reg  busy
);

    localparam integer DIV = CLK_HZ / BAUD;

    reg [15:0] divcnt = 0;
    reg [3:0]  bitpos = 0;
    reg [9:0]  frame;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            tx     <= 1'b1;
            busy   <= 1'b0;
            divcnt <= 0;
            bitpos <= 0;
            frame  <= 10'b1111111111;
        end else begin

            if (tx_start && !busy) begin
                // Correct frame ordering
                // frame[0] = start = 0
                // frame[1] = data bit 0
                // ...
                // frame[8] = data bit 7
                // frame[9] = stop = 1
                frame  <= {1'b1, tx_data, 1'b0};
                busy   <= 1'b1;
                bitpos <= 0;
                divcnt <= 0;
                tx     <= 1'b0;  // start bit
            end
            else if (busy) begin
                if (divcnt == DIV-1) begin
                    divcnt <= 0;
                    bitpos <= bitpos + 1;

                    // send next bit
                    tx <= frame[bitpos];

                    if (bitpos == 9) begin
                        busy <= 1'b0; // done
                        tx   <= 1'b1; // idle
                    end
                    
                end else begin
                    divcnt <= divcnt + 1;
                end
            end
        end
    end

endmodule

