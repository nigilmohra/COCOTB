/* ----------------------------------------------------------  
SEQUENTIAL CIRCUIT | D FLIP FLOP
------------------------------------------------------------- */

module dff_rtl
(
    input clk,
    input d,
    output reg q
);

always @(posedge clk)
begin
    q <= d;
end

initial
begin
    $dumpfile("dump.vcd");
    $dumpvars(0, dff_rtl); // Assuming 0 specifies the VCD file handle
end
endmodule

/* -------------------------------------------------------------  
                        2024 NIGIL M R
---------------------------------------------------------------- */