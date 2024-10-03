function  [y_norm, y2_norm, y3_norm, fs]=load_lineup()
fs=8192;

data=load('-mat', "lineup.mat");
y=data.y;
y2=data.y2;
y3=data.y3;

y_norm=y/max(abs(y));
y2_norm=y2/max(abs(y2));
y3_norm=y3/max(abs(y3));
audiowrite("sound/y.wav", y_norm, fs);
audiowrite("sound/y2.wav", y2_norm, fs);
audiowrite("sound/y3.wav", y3_norm, fs);