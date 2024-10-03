close all;
clear;

[y, Fs] = audioread('audio/audio_raw.wav');

fc = [30 60 120 240 480 960 1920 3840 7680 15360];  % 尽可能涵盖人耳频率，依据梅尔刻度设计指数级间隔
gain = [-3 -1 1 1 3 3 3 1 1 1]; % 增益设定 用户核心
num_bands = length(fc);

B = cell(num_bands, 1);
A = cell(num_bands, 1);
for i = 1:num_bands
    [B{i}, A{i}] = butter(2, [fc(i)*(2^(-1/6))*0.9, fc(i)*(2^(1/6))*1.1]/(Fs/2), 'bandpass');
end

y_eq = zeros(size(y));
for i = 1:num_bands
    y_eq = y_eq + gain(i)*filter(B{i}, A{i}, y);
end
y_eq = y_eq/mean(abs(y_eq))*mean(abs(y));

audiowrite('audio/audio_eq.wav', y_eq, Fs);

p = figure;
subplot(2,1,1);
plot((1:length(y))/Fs, y, 'b');
hold on;
plot((1:length(y_eq))/Fs, y_eq, 'r');
hold off;
xlabel('Time (s)');
ylabel('Amplitude');
title('Audio and Equalized Audio - Time Domain');
legend('Channel 1 - Original', 'Channel 1 - Equalized');
subplot(2,1,2);
stft(y_eq)
title('Equalized Audio - STFT Spectrogram');
saveas(p, '../figures/audio_eq_stft.png');