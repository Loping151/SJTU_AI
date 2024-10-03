t=-5:0.01:5;
figure(1)
plot(t,x(t));

function y=x(t)
    y=0;
    for n=-1000:1000
        y=y+exp(-abs(t-2*n));
    end
end