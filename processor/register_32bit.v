// synopsys translate_off
`timescale 1 ps / 1 ps
// synopsys translate_on
module register_32bit (
	aclr,
	clock,
	data,
	enable,
	q0, q1, q2, q3);

	input	  aclr;
	input	  clock;
	input	[31:0]  data;
	input	  enable;
	output reg	[7:0]  q0, q1, q2, q3;
	
	always @(posedge clock, posedge aclr)
	begin
		if (aclr) begin
			q0 <= 8'b0;
			q1 <= 8'b0;
			q2 <= 8'b0;
			q3 <= 8'b0;
		end
		else if (enable) begin
			q0 <= data[7:0];
			q1 <= data[15:8];
			q2 <= data[23:16];
			q3 <= data[31:24];
		end
	end

endmodule