load('lineup.mat')
Fs=8192;
c2;
d1=[];
d2=[];
t3=y3-we;
for i=1:6999
    d1(i)=we(i+1)/we(i);
    d2(i)=t3(i+1)/t3(i);
end
plot(d1);
hold on;
plot(d2);
y3(752:7000)=y3(752:7000)-0.75*we(1:7000-751);
figure()
plot(t3);
hold on;
plot(we)
y3(2253:7000)=y3(2253:7000)-0.6*we(1:7000-2252);
pause(1);
sound([0.15*y3;zeros(5000,1)],Fs);
we=y3;
plot(y3);