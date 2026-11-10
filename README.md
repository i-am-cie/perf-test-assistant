# Perf Test Assistant

> 本地AI性能测试助手，基于 Ollama 大模型，完全离线运行。

## ✨ 功能特性

- **Locust脚本生成**：输入接口信息，自动生成Locust性能测试Python脚本
- **JMeter方案设计**：AI生成完整的JMeter负载测试计划和参数配置
- **测试策略建议**：根据业务场景推荐合适的并发数、压测时长、阶梯加压策略
- **结果分析**：输入压测数据，AI分析瓶颈点和优化建议
- **性能指标解释**：TPS、响应时间、错误率等指标的含义和优化方向
- **完全本地**：所有数据都在你的电脑上

## 🚀 快速开始

### 前置要求

1. 安装 [Ollama](https://ollama.com/)
2. 拉取模型：
   ```bash
   ollama pull qwen2.5:7b
   ```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动 Web 界面

```bash
python app.py
```

打开浏览器访问 http://localhost:5005

### 命令行模式

```bash
# 生成Locust脚本
python tester.py --api "https://api.example.com/login POST username password" --users 100

# 生成测试策略
python tester.py --strategy "电商首页，预计峰值QPS 500"

# 分析压测结果
python tester.py --analyze "TPS: 300, P95: 800ms, 错误率: 2%"
```

## 📦 项目结构

```
perf-test-assistant/
├── app.py              # Flask Web 界面
├── tester.py           # 核心性能测试逻辑
├── requirements.txt    # Python 依赖
└── README.md
```

## 🛠️ 技术栈

- **后端**：Python + Flask
- **LLM**：Ollama (Qwen2.5)
- **前端**：HTML + 原生 JS

## 📝 License

MIT