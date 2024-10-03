clc;
clear;
[~,y2,~,Fs]=load_lineup();

% 试听信号
% sound(y2,Fs);

% 利用自相关函数确定延时
t=1:length(y2);
Rt=Relation(y2,t);
figure(1);
plot(t,Rt)
[~,T]=max(Rt(5:end));
T=T+4;
fprintf("T=%d\n", T);

% 尝试寻找自相关规律未果
Ralpha=zeros(1,100);
for i=1:100
    tmp=y2;
    for j=1:double(int32(7000/T))+1
        tmp(1+(T*j):7000)=tmp(1+(T*j):7000)+(-0.01*i)^j*y2(1:7000-T*j);
        Ralpha(i)=Relation(tmp,T);
    end
end
figure(2);
plot(0.01*(1:100),Ralpha)

% 寻找alpha
[my2,m]=max(y2(1:501));
syms a;
funcx=@(a)y2(m+T)-a*y2(m);
for i=2:12
    funcx=y2(m+i*T)-a*funcx;
end
% 认为信号结束时大约是0
alpha=double(solve(funcx==0));
alpha=alpha(alpha>0.6 & alpha<1);
fprintf('alpha=%f\n', alpha);

% 消除回声
x2=y2;
for i=1:15
    x2(1+(T*i):7000)=x2(1+(T*i):7000)+(-alpha)^i*y2(1:7000-T*i);
end
% sound(x2,Fs);
audiowrite("sound/x2.wav" , x2, Fs);
figure(3);
plot(y2);
hold on;
plot(x2);