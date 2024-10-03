`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/09/26 18:55:33
// Design Name: 
// Module Name: shumaguan1
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
input [3:0] SW_num, // 4位开关输入显示的数值 
 input [3:0] SW_DIP, //4位开关决定数码管是否显示  
output reg [6:0] a_to_g , //输出7数码管的字形段码组合Ca~Cg  
output [3:0] led_bits //输出4位数码管的位控使能端 
 );   
assign led_bits = SW_DIP ; //位控开关的状态赋值给数码管的位控使能端   //SW_DIP的左到右依次对应板上的左到右片数码管（虽然它的标号从左到右是1234）
always @(*)  
    begin  
        case(SW_num) //判断要显示的字形，赋值给段码变量相应数值  //Ca-Cg依次对应7'b的左到右
        0:a_to_g=7'b1111110; //显示字形"0"  
        1:a_to_g=7'b0110000; //1 
        2:a_to_g=7'b1101101; //2
        3:a_to_g=7'b1111001; //3 
        4:a_to_g=7'b0110011; //4 
        5:a_to_g=7'b1011011; //5 
        6:a_to_g=7'b1011111; //6 
        7:a_to_g=7'b1110000; //7 
        8:a_to_g=7'b1111111; //8 
        9:a_to_g=7'b1111011; //9 
        'hA: a_to_g=7'b1110111; //10,A 
        'hB: a_to_g=7'b0011111; //11,b
        'hC: a_to_g=7'b1001110; //12,C 
        'hD: a_to_g=7'b0111101; //13,d
        'hE: a_to_g=7'b1001111; //14,E 
        'hF: a_to_g=7'b1000111; //显示字形"F"  
        default: a_to_g=7'b1111110;  // 0
        endcase  
    end 
endmodule
