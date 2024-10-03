%% mdl_puma560
% clear;
% figure(1);
% mdl_puma560
% p560.plot([0, 0, 0, 0, 0, 0])
% view(40, 30);

%% definition of PUMA560
clc;
clear;

theta = [0, 0, 0, 0, 0, 0];
d = [0, 0, 20, 100, 0, 0];
a = [0, 0, 100, 10, 0, 0];
alpha = [0, -pi/2, 0, -pi/2, pi/2, -pi/2];

L1 = Link([theta(1), d(1), a(1), alpha(1)], 'modified');
L2 = Link([theta(2), d(2), a(2), alpha(2)], 'modified');
L3 = Link([theta(3), d(3), a(3), alpha(3)], 'modified');
L4 = Link([theta(4), d(4), a(4), alpha(4)], 'modified');
L5 = Link([theta(5), d(5), a(5), alpha(5)], 'modified');
L6 = Link([theta(6), d(6), a(6), alpha(6)], 'modified');

p560 = SerialLink([L1, L2, L3, L4, L5, L6], 'name', 'PUMA560');
p560.display

figure(2);
p560.plot([0, 0, 0, 0, 0, 0])
view(40, 30);
%% workspace in all

total = 10000;
sampled_poses = zeros(total, 4, 4);
param_list = zeros(total, 6);

for sample = 1:total
    q = ([rand(), rand(), rand(), rand(), rand(), rand()] - 0.5) * 2 * pi;
    param_list(sample, :) = q;
    sampled_poses(sample, :, :) = p560.fkine(q);
end

figure(3);
scatter3(sampled_poses(:, 1, 4), sampled_poses(:, 2, 4), sampled_poses(:, 3, 4), 3, [0 0.4470 0.7410], 'MarkerEdgeAlpha', 0.5, 'MarkerFaceAlpha', 0.5);
xlabel('X');
ylabel('Y');
zlabel('Z');
title('PUMA 560 workspace');
grid on;
axis equal;
p560.plot([0, 0, 0, 0, 0, 0])
view(40, 30);
%% workspace for 180 range
sampled_poses = zeros(total, 4, 4);
param_list = zeros(total, 6);

for sample = 1:total
    q = ([rand(), rand(), rand(), rand(), rand(), rand()] - 0.5) * pi;
    param_list(sample, :) = q;
    sampled_poses(sample, :, :) = p560.fkine(q);
end

figure(4);
scatter3(sampled_poses(:, 1, 4), sampled_poses(:, 2, 4), sampled_poses(:, 3, 4), 3, [0 0.4470 0.7410], 'MarkerEdgeAlpha', 0.5, 'MarkerFaceAlpha', 0.5);
xlabel('X');
ylabel('Y');
zlabel('Z');
title('PUMA 560 workspace');
grid on;
axis equal;
view(40, 30);
%% Problem 2
figure(5);
p560.base = transl(0, 0, -75);
p560.plot([0, 0, 0, 0, 0, 0])
hold on;

cx = 100; cy = 0; cz = 50;
lx = 200; ly = 30; lz = 150;

vertices = [cx-lx/2, cy-ly/2, cz-lz/2;
            cx+lx/2, cy-ly/2, cz-lz/2;
            cx+lx/2, cy+ly/2, cz-lz/2;
            cx-lx/2, cy+ly/2, cz-lz/2;
            cx-lx/2, cy-ly/2, cz+lz/2;
            cx+lx/2, cy-ly/2, cz+lz/2;
            cx+lx/2, cy+ly/2, cz+lz/2;
            cx-lx/2, cy+ly/2, cz+lz/2];

faces = [1 2 6 5;
         2 3 7 6;
         3 4 8 7;
         4 1 5 8;
         1 2 3 4;
         5 6 7 8];
patch('Vertices', vertices, 'Faces', faces, 'FaceColor', 'r', 'FaceAlpha', 0.5);
axis equal;
xlabel('X');
ylabel('Y');
zlabel('Z');
view(40, 30);
grid on;
%% movement
Tstart = transl(100, 100, 10);
Tend = transl(100, -100, 10);

Tmid = transl(150, 0, -75);

qstart = p560.ikine(Tstart, 'q0', [0 0 pi 0 0 0], 'mask', [1 1 1 0 0 0]);
qmid = p560.ikine(Tmid, 'q0', qstart, 'mask', [1 1 1 0 0 0]);
qend = p560.ikine(Tend, 'q0', qmid, 'mask', [1 1 1 0 0 0]);

t = 0:0.05:2;

[Q1, Qd1, Qdd1] = jtraj(qstart, qmid, t);
[Q2, Qd2, Qdd2] = jtraj(qmid, qend, t);
patch('Vertices', vertices, 'Faces', faces, 'FaceColor', 'r', 'FaceAlpha', 0.5);
Q = [Q1; Q2];
p560.plot(Q, 'trail', 'r-');
%% Plotting the joint angles
time_vector = 0:0.05:4.05;
time_vector = transpose(time_vector);

figure;
subplot(3,2,1);
plot(time_vector, Q(:,1));
title('Joint 1 Angle vs Time');
xlabel('Time [s]');
ylabel('Angle [rad]');

subplot(3,2,2);
plot(time_vector, Q(:,2));
title('Joint 2 Angle vs Time');
xlabel('Time [s]');
ylabel('Angle [rad]');

subplot(3,2,3);
plot(time_vector, Q(:,3));
title('Joint 3 Angle vs Time');
xlabel('Time [s]');
ylabel('Angle [rad]');

subplot(3,2,4);
plot(time_vector, Q(:,4));
title('Joint 4 Angle vs Time');
xlabel('Time [s]');
ylabel('Angle [rad]');

subplot(3,2,5);
plot(time_vector, Q(:,5));
title('Joint 5 Angle vs Time');
xlabel('Time [s]');
ylabel('Angle [rad]');

subplot(3,2,6);
plot(time_vector, Q(:,6));
title('Joint 6 Angle vs Time');
xlabel('Time [s]');
ylabel('Angle [rad]');
%% save gif
filename = 'p560_animation.gif';
h = figure; 
for i = 1:size(Q, 1)
    clf;
    p560.plot(Q(i,:), 'trail', 'r-', 'noarrow');
    patch('Vertices', vertices, 'Faces', faces, 'FaceColor', 'r', 'FaceAlpha', 0.5);
    pause(0.05);
    frame = getframe(h);
    im = frame2im(frame);
    [imind,cm] = rgb2ind(im,256);
    if i == 1
        imwrite(imind, cm, filename, 'gif', 'Loopcount', inf, 'DelayTime', 0.05);
    else
        imwrite(imind, cm, filename, 'gif', 'WriteMode', 'append', 'DelayTime', 0.05);
    end
end
%% test joint 4
q = [0 0 0 0 0 0];

total_time = 5;
time_step = 0.1;
num_steps = total_time / time_step;

figure;

for k = 1:num_steps
    q(4) = 2*pi*(k-1)/num_steps;
    p560.plot(q);
    
    pause(time_step);
end