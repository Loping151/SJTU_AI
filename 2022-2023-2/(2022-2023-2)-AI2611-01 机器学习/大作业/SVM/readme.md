## 运行说明：

完全版本要求使用支持cuda12的设备，比如RTX40系显卡。在其他cuda设备上运行时，可以选择安装适合版本的cupy，如cupy-cuda11x。cupy也支持AMD显卡。MAC加速库支持未知，但代码支持cpu，未经过完整的功能测试，如出错只需微调报错的地方。

代码支持windows，linux设备，如需加速需要进行常规的cuda环境设置。

单独运行data_loader.py，将进行数据集下载和处理。此后可以运行config，如

*python main.py --config config/default.json*

## 代码说明：

cuda_acc.py中，主要使用了cupy进行cuda加速，对函数重新定义以增强可读性

data_loader.py中，对来自torchvision的数据集代码按照需求进行了修改，以统一数据格式为cupy.ndarray(on gpu)，np.ndarray(on cpu)

img_process.py中，有降为方法与特征处理。

SVM.py定义了所用的SVM和SVC类。

utils.py定义了数据处理和工具函数。

animation.py定义了效果。

train.py定义了训练测试过程。

main.py处理了随机种子固定、异常捕捉和config传入。