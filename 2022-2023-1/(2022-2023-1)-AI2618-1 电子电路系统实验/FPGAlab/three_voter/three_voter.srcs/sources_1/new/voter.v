`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/21 18:14:15
// Design Name: 
// Module Name: voter
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


module voter(
    input A,
    input B,
    input C,
    output Y
    );
    assign Y = (A&B)|(B&C)|(A&C);
endmodule
