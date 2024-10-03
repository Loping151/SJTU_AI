x = linspace(-1, 1, 1001);
y = linspace(-1, 1, 1001);
[X, Y] = meshgrid(x, y);
Z = X .* Y;
mesh(X, Y, Z)
xlabel('x')
ylabel('y')
zlabel('z')
title('z = xy')

saveas(gcf, 'z_xy.png')
