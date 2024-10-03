%所求离散函数
x=@(n)exp(-1*abs(n/10)).*sin(2*pi*n/4);
%先确定合理定义域
dom1=-10:10;
figure(1)
plot(dom1,x(dom1))
%发现两端并未收敛
%%
dom2=-100:100;
figure(2)
plot(dom2,x(dom2))
disp(energy(x,100,200))
%发现两端已经收敛，可以计算
%%
%计算
disp(energy(x,-100,100))
%%
% 计算公式
function E = energy(f,t1,t2)
    E=0;
    for i=t1:t2
        E=E+f(i)^2;
    end
end