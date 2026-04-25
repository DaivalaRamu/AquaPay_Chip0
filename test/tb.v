`default_nettype none
`timescale 1ns / 1ps

module tb ();

  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;

  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

`ifdef GL_TEST
  wire VPWR = 1'b1;
  wire VGND = 1'b0;
`endif

  // IMPORTANT: module name stays same
  tt_um_aquapay_chip user_project (

`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif

      .ui_in(ui_in),
      .uo_out(uo_out),
      .uio_in(uio_in),
      .uio_out(uio_out),
      .uio_oe(uio_oe),
      .ena(ena),
      .clk(clk),
      .rst_n(rst_n)
  );

  initial begin
    clk = 0;
    forever #5 clk = ~clk;
  end

  initial begin
    ena = 1;
    rst_n = 0;
    ui_in = 0;
    uio_in = 0;

    #20 rst_n = 1;

    // ₹1 test
    #10 ui_in[0] = 1;
    #10 ui_in[0] = 0;

    repeat(2) begin
      #10 ui_in[4] = 1;
      #10 ui_in[4] = 0;
    end

    #200 $finish;
  end

endmodule
