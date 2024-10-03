clc;
clear;
[~,~,y3,Fs]=load_lineup();

% 试听信号
% sound(y3,Fs);

% 利用自相关函数确定延时
t=1:length(y3);
Rt=Relation(y3,t);
figure(1);
plot(t,Rt)
[~,T1]=max(Rt(100:end));
T1=T1+99;
[~,T2]=max(Rt(T1+100:end));
T2=T2+T1+99;
fprintf("T1=%d, T2=%d\n", T1, T2);

% 递推方程计算alpha
s1=19;
s2=190;
syms a1 a2;
equ1=Recursion(6250,T1,T2,y3,a1,a2);
equ2=Recursion(6750,T1,T2,y3,a1,a2);
sol=solve(equ1==0,equ2==0);
alpha1=double(sol.a1);
alpha1=alpha1(alpha1==real(alpha1));
alpha1=alpha1(alpha1<0.8 & alpha1>0.6);
alpha2=double(sol.a2);
alpha2=alpha2(alpha2==real(alpha2));
alpha2=alpha2(alpha2<0.8 & alpha2>0.5);
fprintf('alpha1=%f, alpha2=%f\n', alpha1, alpha2);

% 消除回声
x3=y3;
for i=T1+1:7000
    x3(i)=x3(i)-alpha1*x3(i-T1);
    if i>T2
        x3(i)=x3(i)-alpha2*x3(i-T2);
    end
end

% sound(x3,Fs);
audiowrite("sound/x3.wav" , x3, Fs);
figure(2);
plot(y3);
hold on;
plot(x3);
