clc;
clear;
[y,~,~,Fs]=load_lineup();
% sound(y,Fs);

figure(1);
plot(y);
hold on;
x1=y;
T=1000;
alpha=0.5;

for i=1:6
    x1(1+T*i:7000)=x1(1+T*i:7000)+(-alpha)^i*y(1:7000-T*i);
end

plot(x1);
pause(2);
% sound(x1,Fs);
audiowrite("sound/x1.wav" , x1, Fs);