`timescale 1ns / 1ps
module afe_top(
    input  wire        clk,
    input  wire        reset,
    input  wire [11:0] vin,
    output wire        logic_out,
    output wire        cmp_out,
    output wire        uart_tx
);

    // Comparator
    schmitt_comparator u_cmp (
        .vin  (vin),
        .vout (cmp_out)
    );

    // SR latch
    sr_latch u_latch (
        .set   (cmp_out),
        .reset (reset),
        .q     (logic_out)
    );

    // EDGE DETECTOR
    reg logic_prev;
    always @(posedge clk or posedge reset) begin
        if (reset)
            logic_prev <= 0;
        else
            logic_prev <= logic_out;
    end

    wire rise_edge = (logic_out == 1 && logic_prev == 0);
    wire fall_edge = (logic_out == 0 && logic_prev == 1);

    // UART interface
    reg        tx_start;
    reg [7:0]  tx_data;
    wire       tx_busy;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            tx_start <= 0;
            tx_data  <= 8'h00;
        end else begin
            tx_start <= 0;  // default low

            if (!tx_busy) begin
                if (rise_edge) begin
                    tx_data  <= 8'hA5;
                    tx_start <= 1;
                end else if (fall_edge) begin
                    tx_data  <= 8'h5A;
                    tx_start <= 1;
                end
            end
        end
    end

    // UART module
    uart_tx #(
        .CLK_HZ(10_000_000),
        .BAUD(115200)
    ) UTX (
        .clk(clk),
        .rst(reset),
        .tx_start(tx_start),
        .tx_data(tx_data),
        .tx(uart_tx),
        .busy(tx_busy)
    );

endmodule

