[y,y1,y2,Fs]=load_lineup();

x=zeros(45000,1);
save('hear.mat','x')

c2;
pause(1);
close all;
load('hear.mat')
x(1:7000)=x1(1:end);
save('hear.mat','x')

c3;
pause(2.5);
close all;
load('hear.mat')
x(15001:22000)=x2(1:end);
save('hear.mat','x')

c4;
pause(3.5);
close all;
load('hear.mat')
x(30001:37000)=x3(1:end);

sound(x,Fs);