% the comments are added personally, not c-bro. So is the code.
clc
close all
clear *
% set init ts
ts = 1/3;

%% basic  
% define sampling positions and rect func
t = linspace(0, 1000, 1000/ts+1); % the +1 is a tree planting problem. 1000 is the inf I use here.
x = rectpuls(t-5, 10+1e-9); % sampled rect, 1e-9 is to match the definition(value 1 at 0 and 10). here use rectpuls to generate sequence.
total_t = linspace(0, 100, 1200);
original = rectpuls(linspace(0, 100, 1200)-5, 10+1e-9);
shifted = rectpuls(linspace(0, 100, 1200)-5-ts/2, 10+1e-9);

%% plot time
N = length(t);
p1 = figure(1);
hold on;
plot(total_t, original, 'k-', LineWidth=2); % plot the original signal
xlim([0,15]);
ylim([-0.15,1.2]);
stem(t(1:15/ts),x(1:15/ts),'b-', LineWidth=1.5);
scatter(t(1:15/ts),x(1:15/ts),'bo', LineWidth=1.5);
xlabel('time(s)');
saveas(p1, 'figures/p1.png')

%% fft and plot
p2 = figure(2);
hold on;
X = fftshift(fft(x, N)); % N given mamually
f = (-N/2:N/2-1)/ts/N; % frequency
plot(f,abs(X),'k-',LineWidth=1); % plot only low freq part
xlim([-0.5,0.5]);
xlabel('freq(Hz)');
saveas(p2, 'figures/p2.png')

%% shift and plot
x = rectpuls(t-5-ts/2, 10+1e-9);
p3 = figure(3);
hold on;
plot(total_t, shifted,'k-', LineWidth=2); % plot the original signal
xlim([0,15]);
ylim([-0.15,1.2]);
stem(t(1:15/ts),x(1:15/ts),'b-', LineWidth=1.5);
scatter(t(1:15/ts),x(1:15/ts),'bo', LineWidth=1.5);
xlabel('time(s)');
saveas(p3, 'figures/p3.png')

%% shift and fft
p4 = figure(2);
hold on;
X = fftshift(fft(x, N)); % N given mamually
f = (-N/2:N/2-1)/ts/N; % frequency
plot(f,abs(X),'b-',  LineWidth=1); % plot only low freq part
xlim([-0.5,0.5]);
xlabel('freq(Hz)');
legend('unshifted', 'shifted')
saveas(p4, 'figures/p4.png')

%% filter
% tiaocan takes hours
Wp = 0.1;
Rp = 1;
Ws = 0.12;
Rs = 5;
[n, Wn] = buttord(Wp, Ws, Rp, Rs);
[b, a] = butter(n, Wn, 'low');
filt = filtfilt(b, a, shifted);
y = filt(1:4:end);
p5 = figure(5);
hold on;
plot(total_t, filt, 'k-', LineWidth=2);
xlim([0,15]);
ylim([-0.15,1.2]);
stem(t(1:15/ts),y(1:15/ts),'b-', LineWidth=1.5);
scatter(t(1:15/ts),y(1:15/ts),'bo', LineWidth=1.5);
xlabel('time(s)');
saveas(p5, 'figures/p5.png')

%% filter and fft
p6 = figure(2);
hold on;
Y = fftshift(fft(y, N)); % N given mamually
f = (-N/2:N/2-1)/ts/N; % frequency
plot(f,abs(Y),'r-',  LineWidth=1); % plot only low freq part
xlim([-0.5,0.5]);
xlabel('freq(Hz)');
legend('原信号', '平移后', '滤波后')
saveas(p6, 'figures/p6.png')
xlim([0.4,1.2]);
saveas(p6, 'figures/p7.png')
