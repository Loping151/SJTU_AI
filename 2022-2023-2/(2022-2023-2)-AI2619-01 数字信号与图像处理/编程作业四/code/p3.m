close all;
clear;

[y, Fs] = audioread('audio/audio_raw.wav');
y = reshape(y, [1, length(y)]);
fs_downsample = [5000, 10000, 15000];

for i=fs_downsample
    filename = ['audio/audio_', num2str(i), 'kHz.wav'];
    [y_downsample, Fs_downsample] = audioread(filename);
    
    y_interp = interp1(y_downsample, 1:(i/Fs):length(y_downsample));
    Fs_interp = i;
    
    f = figure;
    subplot(3,1,1);
    plot((1:length(y_interp))/Fs_interp, y_interp);
    xlabel('Time (s)');
    ylabel('Amplitude');
    title(['Interpolated Audio (', num2str(i), ' Hz) - Time Domain']);
    subplot(3,1,2);
    plot((1:length(y_interp)+4), ([y_interp 0 0 0 0]+[0 y_interp 0 0 0]+[0 0 y_interp 0 0]+[0 0 0 y_interp 0]+[0 0 0 0 y_interp]-[y(1:length(y_interp)) 0 0 0 0]-[0 y(1:length(y_interp)) 0 0 0]-[0 0 y(1:length(y_interp)) 0 0]-[0 0 0 y(1:length(y_interp)) 0]-[0 0 0 0 y(1:length(y_interp))])/5);
    ylim([min(y_interp), max(y_interp)]);
    xlabel('Time (s)');
    ylabel('Amplitude');
    title('Difference');
    subplot(3,1,3);
    stft(y_interp);
    plotname = ['../figures/in', num2str(i), '.png'];
    title(['Interpolated Audio (', num2str(i), ' Hz) - STFT Spectrogram']);
    saveas(f, plotname);
    filename = ['audio/audio_', num2str(i), 'kHz_interp.wav'];
    audiowrite(filename, y_interp, Fs_interp);
end
