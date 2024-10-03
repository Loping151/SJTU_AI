`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/09/26 20:29:46
// Design Name: 
// Module Name: shumaguan3
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


module D0_display( //封装字形显示和位控的子模块，与第二个例程的一样  
input [3:0] D0_bits ,  //位控
input [3:0] D0_NUM ,  //要显示的数值，4位二进制数
output reg [6:0] D0_a_to_g ,  
output reg [6:0] D0_a_to_g2 ,  
output [3:0] D0_led_bits, 
output [3:0] D0_led_bits2 
 );  
assign D0_led_bits = D0_bits ; 
assign D0_led_bits2 = D0_bits ; 
always @(*)  
    begin  
        case(D0_NUM)  
        0:D0_a_to_g=7'b1111110;  
        1:D0_a_to_g=7'b0110000;  
        2:D0_a_to_g=7'b1101101;  
        3:D0_a_to_g=7'b1111001;  
        4:D0_a_to_g=7'b0110011;  
        5:D0_a_to_g=7'b1011011;  
        6:D0_a_to_g=7'b1011111;  
        7:D0_a_to_g=7'b1110000;  
        8:D0_a_to_g=7'b1111111;  
        9:D0_a_to_g=7'b1111011;  
        'hA: D0_a_to_g=7'b1110111;  
        'hB: D0_a_to_g=7'b0011111;  
        'hC: D0_a_to_g=7'b1001110;  
        'hD: D0_a_to_g=7'b0111101;  
        'hE: D0_a_to_g=7'b1001111;  
        'hF: D0_a_to_g=7'b1000111;  
        default: D0_a_to_g=7'b1111110;  
        endcase  
        case(D0_NUM)  
        0:D0_a_to_g2=7'b1111110;  
        1:D0_a_to_g2=7'b0110000;  
        2:D0_a_to_g2=7'b1101101;  
        3:D0_a_to_g2=7'b1111001;  
        4:D0_a_to_g2=7'b0110011;  
        5:D0_a_to_g2=7'b1011011;  
        6:D0_a_to_g2=7'b1011111;  
        7:D0_a_to_g2=7'b1110000;  
        8:D0_a_to_g2=7'b1111111;  
        9:D0_a_to_g2=7'b1111011;  
        'hA: D0_a_to_g2=7'b1110111;  
        'hB: D0_a_to_g2=7'b0011111;  
        'hC: D0_a_to_g2=7'b1001110;  
        'hD: D0_a_to_g2=7'b0111101;  
        'hE: D0_a_to_g2=7'b1001111;  
        'hF: D0_a_to_g2=7'b1000111;  
        default: D0_a_to_g2=7'b1111110;  
        endcase  
    end 
endmodule 


 module Count_FFFF( //X4X3X2X1 ，Xi是从0~F，总体从右侧最低位依次向左高位进位  
input clk,  
input clr,  
output [6:0] a_to_g ,  //顶层模块输出字形
output [3:0] led_bits  //顶层模块输出位控
); 
reg [3:0] num ;  
reg [35:0] clk_cnt ;    //num取自其中的若干位
reg [3:0] t_led_bits ; //中间变量，存储数码管复用切换位控信息 

always@(posedge clk)  
    begin  
    if(clr)  
    clk_cnt = 0 ;  
    else  
    clk_cnt = clk_cnt + 1 ;  
    end  
     
always@(*) //取计数变量的高16位组成要显示的1个4位十六进制数   //思考为何取高16位[35:20],——所取的位置影响Xi从0~F变化的快慢，最低4位如果太靠近右边，变化频率太高，肉眼看不清他的变化过程。轻微右移一两位整体应该问题不大
    case(clk_cnt[15:14]) //取计数变量的较低2位(频率高)数值，作为4位数码管扫描复位切换频率   //这里取的位置决定了在case0~3之间切换的速度，需要满足视觉暂留的需求
    0:begin num <= clk_cnt[23:20];t_led_bits <= 4'b0001;end //数码管1有效，且显示数值为最低4位  //思考为何要连续且不相重叠的4位4位？——每4位二进制数形成1位16进制数，X4X3X2X1 ，Xi是从0~F，总体从右侧最低位依次向左高位进位
    1:begin num <= clk_cnt[27:24];t_led_bits <= 4'b0010;end //数码管2有效，且显示数值为次低4位  
    2:begin num <= clk_cnt[31:28];t_led_bits <= 4'b0100;end //数码管3有效，且显示数值为次高4位  
    3:begin num <= clk_cnt[35:32];t_led_bits <= 4'b1000;end //数码管4有效，且显示数值为最高4位  
    endcase   

D0_display myD0_display(.D0_bits(t_led_bits),.D0_NUM(num),.D0_a_to_g(a_to_g),.D0_a_to_g2(a_to_g),.D0_led_bits(led_bits),.D0_led_bits2(led_bits)) ;  
endmodule
