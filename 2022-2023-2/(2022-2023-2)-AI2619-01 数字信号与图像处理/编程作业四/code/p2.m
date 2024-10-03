close all;
clear;

[y, Fs] = audioread('audio/audio_raw.wav');
fs_downsample = [5000, 10000, 15000];

naive_downsample = 0; % experimental option

for i = fs_downsample
    % trial for naive downsample
    if naive_downsample
        factor = round(Fs/i);
        y_downsample = y(1:factor:end);
        Fs_downsample = Fs/factor;
    else
        y_downsample = resample(y, i, Fs);
        Fs_downsample = i;
    end

    f = figure;
    subplot(2,1,1);
    plot((1:length(y_downsample))/Fs_downsample, y_downsample);
    xlabel('Time (s)');
    ylabel('Amplitude');
    ylim([-1, 1]);
    title(['Downsampled Audio (', num2str(i), ' Hz) - Time Domain']);
    subplot(2,1,2);
    % try spectrogram
    if naive_downsample
        spectrogram(y_downsample, hamming(1024), 512, [], Fs_downsample, 'yaxis');
    else
        stft(y_downsample);
    end
    plotname = ['../figures/ds', num2str(i), '.png'];
    title(['Downsampled Audio (', num2str(i), ' Hz) - STFT Spectrogram']);
    saveas(f, plotname);
    filename = ['audio/audio_', num2str(i), 'kHz.wav'];
    audiowrite(filename, y_downsample, Fs_downsample);
end
