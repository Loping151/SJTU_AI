clc 
clear *
close all


f1 = @(k) (1-exp(-1i*62*pi*k/3001))/(1-exp(-1i*2*pi*k/3001));
    f2 = @(k) exp(-1i*2*pi/3001)*(1-exp(-1i*60*pi*k/3001))/(1-exp(-1i*2*pi*k/3001));
k = -1:0.001:1;

x1 = zeros(1,2001);
x2 = zeros(1,2001);
for i = 1:2001
    x1(i) = f1(k(i)*1000);
    x2(i) = f2(k(i)*1000);
end

p114 = figure(114);
hold on
plot(k, abs(x1), 'k-');
plot(k, abs(x2), 'b-');
xlim([-0.5,0.5]);
xlabel('freq(Hz)');
legend('公式3', '公式4')
saveas(p114, 'figures/p14.png');
