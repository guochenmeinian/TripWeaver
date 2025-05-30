import streamlit as st
from sub_agents.parser_agent import PreferenceParserAgent
from adk.runtime import ADKRuntime

# 创建 ADK 组件
runtime = ADKRuntime()

# 注册代理
parser_agent = PreferenceParserAgent()
runtime.register("parser", parser_agent)

# 创建输入界面
query = st.text_area(
    "请输入您的旅行计划：",
    "我想6月10号到6月18号从纽约出发去波士顿周边自驾游，最好有一些自然和文化景点",
    height=200
)

if st.button("解析旅行意图"):
    # 使用 ADK 运行时执行解析
    result = runtime.run("parser", {"query": query})
    st.write("解析结果：", result)
