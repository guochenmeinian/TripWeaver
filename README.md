# TripWeaver 🌍

**TripWeaver** 是一个基于 Google ADK (Agent Development Kit) 构建的智能旅行规划助手。通过自然语言交互，帮助用户发现梦想假期、规划行程、预订航班和酒店。

## ✨ 主要功能

- **智能对话**：通过自然语言理解用户需求
- **多代理协作**：多个专业代理协同工作，提供全面服务
- **行程管理**：创建、修改和跟踪旅行计划
- **个性化推荐**：基于用户偏好的智能推荐
- **状态感知**：记住对话上下文和用户偏好

## 🔧 技术栈

- **Google ADK**：多智能体架构和编排
- **Gemini API**：自然语言处理和生成
- **Python 3.12.9**：后端逻辑
- **Pydantic**：数据验证和设置管理
- **Poetry**：依赖管理

## 🧠 系统架构

```
用户输入 → 根代理 (Root Agent) → 专业子代理
                  ↓
          行程规划/预订/建议
```

### 主要组件

- **根代理 (Root Agent)**：路由用户请求到适当的子代理
- **行程规划代理**：处理行程创建和修改
- **预订代理**：管理航班和酒店预订
- **建议代理**：提供个性化旅行建议
- **记忆模块**：管理会话状态和用户偏好

## 🚀 快速开始

### 前提条件

- Python 3.12.9
- Google Cloud 账户和 API 密钥
- Poetry (推荐) 或 pip

### 安装

1. 克隆仓库
```bash
git clone https://github.com/yourusername/tripweaver.git
cd tripweaver
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
创建 `.env` 文件并添加您的 API 密钥：
```
GOOGLE_API_KEY=your_google_api_key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

4. 运行应用
```bash
adk web
```

## 📁 项目结构

```
TripWeaver/
├── TripWeaver/
│   ├── __init__.py
│   ├── agent.py           # 根代理定义
│   ├── prompt.py          # 提示词模板
│   ├── tools/             # 工具函数
│   │   ├── __init__.py
│   │   └── memory.py      # 记忆管理
│   ├── sub_agents/        # 子代理
│   │   ├── __init__.py
│   │   ├── planner.py     # 行程规划
│   │   └── booker.py      # 预订管理
│   └── shared_libraries/  # 共享工具
│       └── constants.py   # 常量定义
├── tests/                 # 测试代码
├── .env.example          # 环境变量示例
├── pyproject.toml        # Poetry 配置
└── README.md
```

## 🛠️ 开发

### 添加新功能

1. 创建新的子代理或工具
2. 在 `agent.py` 中注册新代理
3. 更新提示词模板（如需要）
4. 添加单元测试

### 测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_agent.py
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT

## 📞 联系方式

- 项目链接: [TripWeaver](https://github.com/yourusername/tripweaver)
- 问题追踪: [Issues](https://github.com/yourusername/tripweaver/issues)
