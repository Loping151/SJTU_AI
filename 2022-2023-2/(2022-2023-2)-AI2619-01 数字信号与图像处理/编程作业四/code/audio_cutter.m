[y, Fs] = audioread('audio/我多想说再见啊.wav'); % 原声巨大就不放了

start_time = 0;
end_time = 105; % 听了下截到这不会太突兀
y_cut = y(round(start_time*Fs)+1:round(end_time*Fs), :);

audiowrite('audio/audio_raw.wav', y_cut, Fs);
