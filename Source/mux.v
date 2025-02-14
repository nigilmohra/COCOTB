// Multiplexer 

module mux_2x1 
(
	input a, b, sel,
	output y
);
	assign y = sel ? a : b;
	initial begin
		$dumpfile("dump.vcd");
		$dumpvars(0, mux_2x1);	
	end
endmodule
