baboon = imread("baboon.bmp");
psf = fspecial('average',5);
baboon_blur = conv2(baboon, psf);
% or alternatively
% baboon_blur = imfilter(baboon, psf, 'conv');
baboon_blur = baboon_blur(3:514,3:514);
imwrite(uint8(baboon_blur), 'baboon_blur.bmp')
baboon_10 = awgn(baboon_blur, 10, 'measured');
% or to use imnoise:
% sigp = sum(abs(baboon(:)).^2)/numel(baboon)
% calculate power of noise noip(not NOIP) according to the gaussian
% distribution, sigp and SNR
% noise = imnoise(baboon, noip)
baboon_20 = awgn(baboon_blur, 20, 'measured');
baboon_30 = awgn(baboon_blur, 30, 'measured');
imwrite(uint8(baboon_10), 'baboon_10.bmp')
imwrite(uint8(baboon_20), 'baboon_20.bmp')
imwrite(uint8(baboon_30), 'baboon_30.bmp')
% f is fourier, r is restore, d is direct, w is wiener 
rd_baboon_10 = deconvwnr(baboon_10, psf);
% or use fft
% f_psf = fft2(psf, 512, 512);
% rd_baboon_10 = ifft2(fft2(baboon_blur)./f_psf);
% imshow(uint8(rd_baboon_10))
rd_baboon_20 = deconvwnr(baboon_20, psf);
rd_baboon_30 = deconvwnr(baboon_30, psf);
imwrite(uint8(rd_baboon_10), 'rd_baboon_10.bmp')
imwrite(uint8(rd_baboon_20), 'rd_baboon_20.bmp')
imwrite(uint8(rd_baboon_30), 'rd_baboon_30.bmp')

rw_baboon_10 = deconvwnr(baboon_10, psf, 1/10);
rw_baboon_20 = deconvwnr(baboon_20, psf, 1/20);
rw_baboon_30 = deconvwnr(baboon_30, psf, 1/30);
imwrite(uint8(rw_baboon_10), 'rw_baboon_10.bmp')
imwrite(uint8(rw_baboon_20), 'rw_baboon_20.bmp')
imwrite(uint8(rw_baboon_30), 'rw_baboon_30.bmp')