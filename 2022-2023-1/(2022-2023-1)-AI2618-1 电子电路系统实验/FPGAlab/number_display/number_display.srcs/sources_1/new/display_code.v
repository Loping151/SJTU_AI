`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/21 18:39:37
// Design Name: 
// Module Name: display_code
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


module Static_0_F(
 input [3:0] SW_num, // 4 位开关输入显示的数值
 input [3:0] SW_DIP, //4 位开关决定数码管是否显示
 output reg [6:0] a_to_g , //输出数码管的字形段码组合 Ca~Cg
 output [3:0] led_bits //输出 4 位数码管的位控使能端
 );
 
 assign led_bits = SW_DIP ; //位控开关的状态赋值给数码管的位控使能端
 
 always @(*) 
 begin 
 case(SW_num) //判断要显示的字形，赋值给段码变量相应数值 
 0:a_to_g=7'b1111110; //显示字形"0"
 1:a_to_g=7'b0110000;
 2:a_to_g=7'b1101101;
 3:a_to_g=7'b1111001;
 4:a_to_g=7'b0110011;
 5:a_to_g=7'b1011011;
 6:a_to_g=7'b1011111;
 7:a_to_g=7'b1110000;
 8:a_to_g=7'b1111111;
 9:a_to_g=7'b1111011;
 'hA: a_to_g=7'b1110111;
 'hB: a_to_g=7'b0011111;
 'hC: a_to_g=7'b1001110;
 'hD: a_to_g=7'b0111101;
 'hE: a_to_g=7'b1001111;
 'hF: a_to_g=7'b1000111; //显示字形"F"
 default: a_to_g=7'b1111110;
 endcase
 end
endmodule

