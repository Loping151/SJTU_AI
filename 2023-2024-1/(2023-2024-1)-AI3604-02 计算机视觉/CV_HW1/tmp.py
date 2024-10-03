import numpy as np
import matplotlib.pyplot as plt
import cv2

# 读取图像
image = cv2.imread('output/coins_edge_raw.png', cv2.IMREAD_GRAYSCALE)

# 计算直方图
hist, bins = np.histogram(image, bins=np.arange(0, 782), range=(0, 781))

# 显示直方图
plt.bar(bins[:-1], hist, width=1)
plt.xlim(0, 781)
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')
plt.title('Histogram')
plt.show()

# 显示原始图像
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
