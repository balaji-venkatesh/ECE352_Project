/* A Vector Register File (VRF) with 4 4x8b registers V0 through V1. The register file has two read ports. The read ports are (vreg1, vdata1) and (vreg2, vdata2) where vreg1 and vreg2 register numbers (2b) and vdata1 and vdata2 are 4x8b values. The read ports are combinatorial, no clock is needed. There is a single write port (vregw,vdataw,VRFWrite) where vregw a 2b register number, vdataw a 4x8b data values, and VRFwrite the write enable signal. This is edge triggered. */

module VRF
(
clock, vreg1, vreg2, vregw,
vdataw, VRFWrite, vdata1, vdata2,
//v0, v1, v2, v3, 
reset
);

// ------------------------ PORT declaration ------------------------ //
input clock;
input [1:0] vreg1, vreg2, vregw;
input [31:0] vdataw;
input VRFWrite;
input reset;
output [31:0] vdata1, vdata2;
//output [31:0] v0, v1, v2, v3;

// ------------------------- Registers/Wires ------------------------ //
reg [31:0] k0, k1, k2, k3;
reg [31:0] data1_tmp, data2_tmp;

// Asynchronously read data from two registers
always @(*)
begin
	case (vreg1)
		0: data1_tmp = k0;
		1: data1_tmp = k1;
		2: data1_tmp = k2;
		3: data1_tmp = k3;
	endcase
	case (vreg2)
		0: data2_tmp = k0;
		1: data2_tmp = k1;
		2: data2_tmp = k2;
		3: data2_tmp = k3;
	endcase
end

// Synchronously write data to the register file;
// also supports an asynchronous reset, which clears all registers
always @(posedge clock or posedge reset)
begin
	if (reset) begin
		k0 = 0;
		k1 = 0;
		k2 = 0;
		k3 = 0;
	end	else begin
		if (VRFWrite) begin
			case (vregw)
				0: k0 = vdataw;
				1: k1 = vdataw;
				2: k2 = vdataw;
				3: k3 = vdataw;
			endcase
		end
	end
end

// Assign temporary values to the outputs
assign vdata1 = data1_tmp;
assign vdata2 = data2_tmp;

/* assign v0 = k0;
assign v1 = k1;
assign v2 = k2;
assign v3 = k3; */

endmodule
