# README.md

# TripWeaver 🌍

**TripWeaver** 是为 Google ADK Hackathon 构建的一个多智能体旅行规划系统。用户只需自然语言输入旅行想法，系统就能解析偏好、生成行程并估算预算。

## 🔧 技术栈
- **ADK (Google Agent Developer Kit)**: 多智能体架构
- **Streamlit**: 快速构建前端 UI
- **Google Maps API**（可选）: 路线和景点信息
- **Gemini / OpenAI**: NLP（意图提取）

## 🧠 Agent 架构
```
User Query
   ↓
PreferenceParserAgent → ItineraryPlannerAgent → BudgetEstimatorAgent
   ↓
            Streamlit UI 展示
```

## ✨ 示例输入
> 我想6月10号到6月18号从纽约出发去波士顿周边自驾游，最好有一些自然和文化景点。

## 🚀 快速开始
```bash
# 安装依赖
pip install streamlit adk

# 运行前端
streamlit run app/streamlit_app.py
```

## 📁 项目结构
```
tripweaver/
├── agents/
│   ├── parser_agent.py
│   ├── itinerary_agent.py
│   └── budget_agent.py
├── app/
│   └── streamlit_app.py
├── main.py
└── README.md
```

## 📌 后续开发
- 接入 Google Maps 生成真实路线和地点打分
- 多种风格（城市/自然/文化）行程对比
- 预算图表化展示（使用 Chart.js 或 Plotly）
- 保存结果到 Google Drive / Airtable
