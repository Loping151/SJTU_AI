load('lineup.mat')
Fs=8192;
sound(y,Fs);
we=y;
T=1000;
for i=1:6
    we(1+T*i:7000)=we(1+T*i:7000)+(-0.5)^i*y(1:7000-T*i);
end


plot(we);
pause(1);
sound(0.15*we,Fs);