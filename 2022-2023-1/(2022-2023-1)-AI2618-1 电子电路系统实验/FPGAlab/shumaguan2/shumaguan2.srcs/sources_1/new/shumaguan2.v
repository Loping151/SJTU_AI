`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/09/26 19:39:19
// Design Name: 
// Module Name: shumaguan2
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


module D0_display( //封装字形显示及位控的子模块 
input [3:0] D0_bits ,  //位控，点亮哪个数码管
input [3:0] D0_NUM ,  //要显示的数值，4位二进制数
output reg [7:0] D0_a_to_g ,  //输出字形
output [3:0] D0_led_bits
 );  //输出位控。**数码管的前期功能不论多复杂，最后本质都是要落在字形和位控这两项上
assign D0_led_bits = D0_bits ;  //位控是直接赋给，字形需要经过下面的case判断
always @(*)  //在任意条件下执行这里面的语句
    begin  
        case(D0_NUM)              //verilog里可以把4位二进制数与十进制数对应起来
        0:D0_a_to_g=8'b01111110;  //字形0
        1:D0_a_to_g=8'b10110000;  //字形1
        2:D0_a_to_g=8'b01101101;  
        3:D0_a_to_g=8'b11111001;  
        4:D0_a_to_g=8'b00110011;  
        5:D0_a_to_g=8'b11011011;  
        6:D0_a_to_g=8'b01011111;  
        7:D0_a_to_g=8'b11110000;  
        8:D0_a_to_g=8'b01111111;  
        9:D0_a_to_g=8'b11111011;  
        'hA: D0_a_to_g=8'b01110111;  
        'hB: D0_a_to_g=8'b10011111;  
        'hC: D0_a_to_g=8'b01001110;  
        'hD: D0_a_to_g=8'b10111101;  
        'hE: D0_a_to_g=8'b01001111;  
        'hF: D0_a_to_g=8'b11000111;  
        default: D0_a_to_g=8'b01111110;  
        endcase  
    end 
endmodule 
 
module Coun_0_F( //顶层模块  
input clk, //100MHz时钟源  
input clr, //清零按钮  
input stop, //暂停按钮
input fast, //加快按钮
input slow, //减速按钮
input [3:0] SW_DIP, //位控开关  ，顶层模块的位控输入，因为功能需求里要求开关控制位控
output [7:0] a_to_g , //字形段码  ，顶层模块的输出字形
output [3:0] led_bits //数码管位控端  ，顶层模块的输出位控
);  
reg [3:0] num ; //中间变量，存储数码管显示数值  
reg [31:0] clk_cnt ; //中间变量，存储时钟源计数结果 

always@(posedge clk) //100MHz时钟频率下的每一上升沿  
    begin  
    if(clr) //判断清零按钮是否有效  
    clk_cnt = 0 ; //若清零按钮被按下，则计数变量清零  
    else if(! stop) //暂停开关打开 
    clk_cnt = clk_cnt + 1 ; //否则，正常计数  
    end  

always@(posedge clk)  
begin
    num = clk_cnt[29:26]; //取计数变量中的4位作为数码管显示数值，该值计数频 //率为100MHz/2^24  
    if(fast)
    num = clk_cnt[28:25];
    else if(slow)
    num = clk_cnt[30:27];
    end
    D0_display myD0_display(.D0_bits(SW_DIP),.D0_NUM(num),.D0_a_to_g(a_to_g),.D0_led_bits(led_bits) ) ; //实例化(调用)数码管子模块，信息流动方向：输入——从顶层模块给被调用模块，输出——从被调用模块到顶层模块
    //被调用模块的4个变量名需要各自对应的变量值，D0_bits取自顶层模块的输入SW_DIP拨码开关，D0_NUM取自（顶层模块中的一个变量）计数器中间的某4位（不同位对应不同的变化频率）
    //D0_a_to_g和D0_led_bits对应顶层模块的两个输出，字形和位控
endmodule 
