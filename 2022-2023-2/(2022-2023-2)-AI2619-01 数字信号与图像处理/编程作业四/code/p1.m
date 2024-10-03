close all;
clear;
[y, Fs] = audioread('audio/audio_raw.wav');

tsp = figure;
subplot(2,1,1);
t = (0:length(y)-1)/Fs;
plot(t, y);
xlabel('Time (s)');
ylabel('Amplitude');
title('Time Domain Plot');

subplot(2,1,2);
stft(y);
title('STFT Spectrogram');
saveas(tsp, '../figures/stftp.png');