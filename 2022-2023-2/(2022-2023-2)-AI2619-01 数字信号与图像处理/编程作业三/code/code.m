clear *
close all
% init
start_power = 4;
end_power = 1000; % auto modified according to memory
step = 2;
powers = start_power:step:end_power;
lengths = 2 .^ powers;
times = zeros(4, numel(lengths));

% check device
if gpuDeviceCount > 0
    % get gpu name
    gpu_info = gpuDevice;
    gpu_name = gpu_info.Name;
else
    disp('No GPU found.');
    gpu_name = 'cpu';
end
num_gpus = gpuDeviceCount();
if num_gpus > 1
    parpool('local', num_gpus);
end

% seed
rng(1)

TLE = zeros(1, 4);
tl = 4;

% for all cases
for e2i = 1:numel(lengths)
    clear x X1 X2 X3 X4 W x_gpu X4_gpu x_half1 x_half2
    N = lengths(e2i);
    x = randn(1, N);
    try
        if TLE(1, 1) == 0        
            % e2i 1：by definition of DFT，use for to DFT
            tic;
            X1 = zeros(1, N);
            for k = 1:N
                for n = 1:N
                    X1(k) = X1(k) + x(n) * exp(-1i * 2 * pi * (k - 1) * (n - 1) / N);
                end
            end
            times(1, e2i) = toc;
            if toc > tl
                TLE(1, 1) = 1;
                fprintf('TLE');    
            end
        else
            times(1, e2i) = NaN;
        end

    catch exception
        % memory?
        times(1, e2i) = NaN;
        TLE(1, 1) = 1;
        fprintf('MLE');
    end

    try
        if TLE(1, 2) == 0
            % e2i 2：use the matrix form of DFT
            tic;
            k = 0:N-1;
            n = k';
            W = exp(-1i * 2 * pi * k .* n / N);
            X2 = x * W;
            times(2, e2i) = toc;
            if toc > tl
                TLE(1, 2) = 1;
            end
        else
            times(2, e2i) = NaN;
        end

    catch exception
        % memory?
        times(2, e2i) = NaN;
        TLE(1, 2) = 1;
        fprintf('MLE');
    end
    
    try
        if TLE(1, 3) == 0
            % e2i 3：use fft function in MATLAB：fft(x)
            tic;
            X3 = fft(x);
            times(3, e2i) = toc;
            if toc > tl
                TLE(1, 3) = 1;
                fprintf('TLE');
            end
        else
            times(3, e2i) = NaN;
        end

    catch exception
        % memory?
        times(3, e2i) = NaN;
        TLE(1, 3) = 1;
        fprintf('MLE');
    end
    
    try
        if TLE(1, 4) == 0
            % 方法4：use GPU tool in MATLAB：fft(gpuArray(x))
            if num_gpus == 1
                x_gpu = gpuArray(x);
                tic;
                X4_gpu = fft(x_gpu);
                X4 = gather(X4_gpu);
                times(4, e2i) = toc;
            else
                x_half1 = x(1:end/2);
                x_half2 = x(end/2+1:end);
                spmd
                    my_gpu = gpuDevice();
                    fprintf('using GPU %d\n', my_gpu.Index);
                    if spmdIndex == 1
                        x_gpu = gpuArray(x_half1);
                    else
                        x_gpu = gpuArray(x_half2);
                    end
                    tic;
                    X_gpu = fft(x_gpu);
                    X_local = gather(X_gpu);
                    times(4, e2i) = toc;
                end
                times = times(1);
                times = times{:};
            end
            if times(4, e2i) > tl
                TLE(1, 4) = 1;
                fprintf('TLE');
            end
        else
            times(4, e2i) = NaN;
        end
            
    catch exception
        % memory?
        try
            times(4, e2i) = NaN;
        catch exception
                times = times(1);
                times = times{:};
                times(4, e2i) = NaN;
        end
        TLE(1, 4) = 1;
        fprintf('MLE');
     end

    disp(times(:,e2i));

    if all(isnan(times(:, e2i)))
        end_power = e2i;
        break
    end
end

% plot
p = figure;
plot(powers(1:end_power), log(1+times(1, 1:end_power)), '-o', ...
     powers(1:end_power), log(1+times(2, 1:end_power)), '-x', ...
     powers(1:end_power), log(1+times(3, 1:end_power)), '-s', ...
     powers(1:end_power), log(1+times(4, 1:end_power)), '-d');
xlabel('序列长度 (指数)');
ylim([-0.1, 1.6])
ylabel('计算时间 (log 秒)');
legend('DFT定义', '矩阵形式', 'fft函数', 'GPU工具', 'Location', 'northwest');
title('不同方法计算DFT的程序运行时间');
% saveas(p, [gpu_name,'.png'])
