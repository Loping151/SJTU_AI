### 任务要求
- 直接使用生成式大模型进行**口语语义理解**或/和**语义三元组解析**
- 大语言模型平台使用不限，可以使用网页版对话框、Huggingface Demo、或对应调用的API
- 至少使用三个不同的Setting来测试，包含但不限于
  - LLM模型（开源/闭源/国外/国内）
  - 模型大小
  - 提示词
  - Zero/One/Few-shot
  - 中文/英文输入
- 推荐使用`data/test_llm_subset.json`中的样例进行测试，也可以使用其他的数据

### 推荐使用的模型
+ [文心一言](https://yiyan.baidu.com/)
+ [通义千问](https://qianwen.aliyun.com/)
+ [ChatGPT](https://chat.openai.com/)
+ [ChatGLM2](https://chatglm.cn/)
+ [Poe机器人平台(LLaMA/Claude/PaLM)](https://poe.com/)
+ [Huggingface Space(huggingface部署的一些开源模型的在线Demo)](https://huggingface.co/spaces)

### 推荐参考的网页
+ [Awesome ChatGPT Prompts](https://github.com/f/awesome-chatgpt-prompts)
+ [Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

### 提示
我们提供了几个思考和探索的方向
- Prompt优化
- Few-shot learning 或者 CoT 技术
- 不同模型生成效果对比
- 结构化输出(进阶)
- 工具使用(进阶)
- 大模型幻觉(进阶)
- 拒绝回答(进阶)

### 评分
- 没有性能要求，要求熟悉大模型提示工程并分析对比结果，在报告中汇报了符合实验设定的结果，并对实验结果进行分析
- 结果报告：包含Prompt、大模型输出，对于每一组输出都请给出对应的setting
- 分析与讨论：开放式，分析对比实验结果，简单探讨大模型时代下口语语义理解现状以及未来可能的研究方向，1000字以内，注意列出参考文献