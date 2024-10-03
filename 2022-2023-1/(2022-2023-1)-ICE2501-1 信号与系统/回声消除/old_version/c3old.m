load('lineup.mat')
Fs=8192;
sound(y2,Fs);
loss=zeros(100,90);

for T=200:10:1200
    for alpha=0.1:0.01:1
        we=atp(T,alpha,y2);
        we(1+T:7000)=we(1+T:7000)+alpha*we(1:7000-T);
        loss(T/10-19,int32(100*alpha)-9)=sum(abs(y2-we));
    end
end

figure(1);
mesh(loss);

T=501;
lossa=zeros(100,1);
for alpha=0.01:0.01:1
    we=atp(T,alpha,y2);
    we(1+T:7000)=we(1+T:7000)+alpha*we(1:7000-T);
    lossa(int32(100*alpha))=sum(abs(y2-we));
end

figure(2);
plot(lossa);

we=atp(T,0.7,y2);

pause(1);
sound(we,Fs)

function we=atp(T,alpha,y2)
    we=y2;
    for i=1:7000/T
        we(1+T*i:7000)=we(1+T*i:7000)+(-alpha)^i*y2(1:7000-T*i);
    end
end