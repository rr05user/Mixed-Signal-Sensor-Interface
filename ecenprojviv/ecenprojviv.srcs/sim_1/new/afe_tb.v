// afe_tb.v : UART-capable mixed-signal testbench
// High-resolution logging for UART (100 ns resolution)
// 10 MHz clock (100 ns period)

`timescale 1ns / 1ps

module afe_tb;

    // --------------------------
    // DUT I/O
    // --------------------------
    reg         clk;
    reg         reset;
    reg  [11:0] vin;

    wire        logic_out;
    wire        cmp_out;
    wire        uart_tx;

    // Instantiate DUT
    afe_top dut (
        .clk       (clk),
        .reset     (reset),
        .vin       (vin),
        .logic_out (logic_out),
        .cmp_out   (cmp_out),
        .uart_tx   (uart_tx)
    );

    // --------------------------
    // 10 MHz Clock
    // --------------------------
    initial clk = 0;
    always #10 clk = ~clk;   // 20 ns period (50 MHz)
 // 100 ns period = 10 MHz


    // --------------------------
    // Hysteresis measurement
    // --------------------------
    integer rise_code, fall_code;
    reg     seen_rise, seen_fall;
    reg     armed;
    real    rise_v, fall_v;

    integer fd;

    function real code_to_volt;
        input integer code;
        code_to_volt = 3.3 * code / 4095.0;
    endfunction


    // --------------------------
    // Test Sequence
    // --------------------------
    initial begin
        reset     = 1;
        vin       = 12'd0;
        seen_rise = 0;
        seen_fall = 0;
        rise_code = 0;
        fall_code = 0;
        armed     = 0;

        // Open CSV
        fd = $fopen("afe_sim.csv", "w");
        if (fd)
            $fwrite(fd, "time_ns,vin_code,cmp_out,logic_out,uart_tx\n");

        // Reset settle
        #300;
        reset = 0;
        #200;
        armed = 1;

        // --------------------------
        // Up-sweep ADC input
        // --------------------------
        repeat (200) begin
    vin = vin + 12'd20;
    #500;   // faster sweep
end


        #500000;     // hold 0.5 ms (UART visible)

        // --------------------------
        // Down-sweep ADC input
        // --------------------------
        repeat (200) begin
            vin = vin - 12'd20;
            #1000;
        end

        // Reset latch after sweep
        #200000;
        reset = 1; #200; reset = 0;

        // Convert codes to voltage
        rise_v = code_to_volt(rise_code);
        fall_v = code_to_volt(fall_code);

        // Report summary
        $display("---- SUMMARY ----");
        $display("Rise code: %0d   Rise V=%.4f",  rise_code, rise_v);
        $display("Fall code: %0d   Fall V=%.4f", fall_code, fall_v);

        // allow UART to finish
        #1_000_000;

        if (fd) $fclose(fd);
        $finish;
    end


    // --------------------------
    // High-resolution logging (100 ns)
    // --------------------------
    always #1000 begin
        if (fd)
            $fwrite(fd, "%0t,%0d,%0d,%0d,%0d\n",
                $time, vin, cmp_out, logic_out, uart_tx);
    end


    // --------------------------
    // Rising edge capture
    // --------------------------
    always @(posedge cmp_out) begin
        if (armed && !seen_rise) begin
            rise_code <= vin;
            seen_rise <= 1;
            $display("%0t ns: RISE detected vin=%0d", $time, vin);
        end
    end

    // --------------------------
    // Falling edge capture
    // --------------------------
    always @(negedge cmp_out) begin
        if (armed && !seen_fall) begin
            fall_code <= vin;
            seen_fall <= 1;
            $display("%0t ns: FALL detected vin=%0d", $time, vin);
        end
    end

endmodule


