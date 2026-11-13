// fabricgate/hello: the six on-board LEDs count up in binary, about one step per second.
// 27 MHz crystal. The LEDs are active low.
module top (input clk, output [5:0] led);
    reg [29:0] cnt = 0;
    always @(posedge clk) cnt <= cnt + 1'b1;
    assign led = ~cnt[29:24];   // bit 24 toggles every 2^24 / 27e6 = 0.62 s
endmodule
