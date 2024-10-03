close all;
clear;

%% task1
roman = imread('../figures/roman.jpg');
r_channel = roman(:, :, 1);
imwrite(r_channel, '../figures/r.jpg');
equ_r = histeq(r_channel);
figure();
imshowpair(r_channel,equ_r,'montage');

%% task2
mu = mean(r_channel, "all");
sigma = sqrt(var(double(r_channel),0, "all"));

exph = exprnd(mu, 900, 1440);
exph = exph(exph<255);
exph = uint8(exph);

normh = normrnd(mu, sigma, 900, 1440);
normh = normh(normh<255);
normh = normh(normh>0);
normh = uint8(normh);

figure();
subplot(2,3,1);
histogram(r_channel);
title('R Channel');

subplot(2,3,2);  
histogram(exph);  
title('Exponential');   

subplot(2,3,3);
histogram(normh);
title('Normal');

subplot(2,3,4);
histogram(equ_r);
title('Equalized');

exp_r = imhistmatch(r_channel, exph);

subplot(2,3,5);
histogram(exp_r);
title('Matched Exponential');

gauss_r = imhistmatch(r_channel, normh);

subplot(2,3,6);
histogram(gauss_r);
title('Matched Normal');

figure();
imshowpair(r_channel,exp_r,'montage');

figure();
imshowpair(r_channel,gauss_r,'montage');

%% task3
factor = 30;
myhist = cat(1, exprnd(mu, 9*factor, 1440), normrnd(mu*1.5, sigma, 9*(100-factor), 1440));
myhist = myhist(myhist<255);
myhist = myhist(myhist>0);
myhist = uint8(myhist);
my_r = imhistmatch(r_channel, myhist);
figure();
imshowpair(r_channel,my_r,'montage');
figure();
subplot(1,2,1);
histogram(myhist);
title('My Hist');
subplot(1,2,2);
histogram(my_r);
title('My Matched');
%% task4
new_roman = imread('../figures/roman.jpg');
r_channel = new_roman(:, :, 1);
g_channel = new_roman(:, :, 2);
b_channel = new_roman(:, :, 3);
equ_r = histeq(r_channel);
equ_g = histeq(g_channel);
equ_b = histeq(b_channel);
new_roman(:, :, 1) = equ_r;
new_roman(:, :, 2) = equ_g;
new_roman(:, :, 3) = equ_b;
figure();
imshowpair(roman,new_roman,'montage');
figure();
subplot(1,2,1);
histogram(new_roman);
title('Eq');

%% task5
new_roman = imread('../figures/roman.jpg');

mu = mean(new_roman, "all");
sigma = sqrt(var(double(new_roman),0, "all"));

factor = 30;
myhist = cat(1, exprnd(mu, 9*factor, 1440), normrnd(mu*1.5, sigma, 9*(100-factor), 1440));
myhist = myhist(myhist<255);
myhist = myhist(myhist>0);
myhist = uint8(myhist);

r_channel = new_roman(:, :, 1);
g_channel = new_roman(:, :, 2);
b_channel = new_roman(:, :, 3);
equ_r = imhistmatch(r_channel, myhist);
equ_g = imhistmatch(g_channel, myhist);
equ_b = imhistmatch(b_channel, myhist);
new_roman(:, :, 1) = equ_r;
new_roman(:, :, 2) = equ_g;
new_roman(:, :, 3) = equ_b;
subplot(1,2,2);
histogram(new_roman);
title('My');
figure();
imshowpair(roman,new_roman,'montage');

new_roman = imread('../figures/roman.jpg');
equ = imhistmatch(new_roman, myhist);
figure();
imshowpair(roman,equ,'montage');

